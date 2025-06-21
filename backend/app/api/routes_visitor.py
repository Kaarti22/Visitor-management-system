from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Employee, PreApproval, Approval, ApprovalStatus
from app.schemas.visitor import VisitorCreate, VisitorOut
from app.schemas.approval import ApprovalOut
from app.services.visitor_service import VisitorService
from app.core.config import SessionLocal
from app.utils.email import send_visitor_notification
from app.utils.qr_generator import generate_qr_and_upload
from app.logger_config import setup_logger

logger = setup_logger()
router = APIRouter(prefix="/visitors", tags=["Visitors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{visitor_id}", response_model=VisitorOut)
def get_visitor(visitor_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching visitor: {visitor_id}")
    service = VisitorService(db)
    visitor = service.fetch_visitor(visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    existing_approval = (
        db.query(Approval)
        .filter_by(visitor_id=visitor_id)
        .order_by(Approval.requested_at.desc())
        .first()
    )

    if existing_approval:
        logger.info(f"Existing approval status: {existing_approval.status}")
    
    if not existing_approval or existing_approval.status == ApprovalStatus.PENDING:
        now = datetime.utcnow()
        logger.info(f"Checking pre-approvals for visitor {visitor_id} at {now}")

        pre = (
            db.query(PreApproval)
            .filter(
                PreApproval.visitor_id == visitor_id,
                PreApproval.valid_from <= now,
                PreApproval.valid_to >= now
            )
            .first()
        )

        if pre:
            today = now.date()
            visits_today = (
                db.query(Approval)
                .filter(
                    Approval.visitor_id == visitor_id,
                    func.date(Approval.decision_at) == today,
                    Approval.status == ApprovalStatus.APPROVED
                )
                .count()
            )

            if visits_today < pre.max_visits_per_day:
                try:
                    logger.info("Pre-approval window and visit count valid. Proceeding to auto-approve...")

                    # ✅ Update existing PENDING approval if exists
                    if existing_approval:
                        existing_approval.status = ApprovalStatus.APPROVED
                        existing_approval.decision_at = datetime.utcnow()
                        logger.info("Updated existing PENDING approval to APPROVED")
                    else:
                        auto_approval = Approval(
                            visitor_id=visitor_id,
                            employee_id=pre.employee_id,
                            status=ApprovalStatus.APPROVED,
                            decision_at=datetime.utcnow(),
                            requested_at=datetime.utcnow()
                        )
                        db.add(auto_approval)
                        logger.info("Inserted new auto-approval record")

                    # ✅ Generate QR badge if not already present
                    if not visitor.badge_url:
                        badge_url = generate_qr_and_upload(str(visitor_id), filename=f"visitor_{visitor_id}")
                        visitor.badge_url = badge_url
                        logger.info(f"Generated QR badge for visitor {visitor_id}")

                    db.commit()
                    db.refresh(visitor)

                except Exception as e:
                    db.rollback()
                    logger.error(f"❌ Auto-approval or badge generation failed: {e}", exc_info=True)

    # 🧠 Fetch final approval for response
    latest_approval = (
        db.query(Approval)
        .filter_by(visitor_id=visitor_id, status=ApprovalStatus.APPROVED)
        .order_by(Approval.decision_at.desc().nullslast())
        .first()
    )

    visitor_data = VisitorOut.from_orm(visitor)
    if latest_approval:
        visitor_data.approval = ApprovalOut.from_orm(latest_approval)

    return visitor_data


@router.post("/register", response_model=VisitorOut, status_code=status.HTTP_201_CREATED)
def register_visitor(data: VisitorCreate, db: Session = Depends(get_db)):
    host = (
        db.query(Employee)
        .filter(
            Employee.name.ilike(data.host_employee_name.strip()),
            Employee.department.ilike(data.host_department.strip())
        )
        .first()
    )
    if not host:
        raise HTTPException(
            status_code=400,
            detail="Host employee not found in the specified department"
        )

    service = VisitorService(db)
    visitor = service.register_visitor(data.dict())

    if host.email:
        send_visitor_notification(
            to_email=host.email,
            visitor_name=data.full_name,
            purpose=data.purpose
        )

    return visitor


@router.patch("/{visitor_id}/checkout", response_model=VisitorOut)
def checkout_visitor(visitor_id: int, db: Session = Depends(get_db)):
    service = VisitorService(db)
    visitor = service.fetch_visitor(visitor_id)

    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    if visitor.check_out:
        raise HTTPException(status_code=400, detail="Visitor already checked out")

    visitor.check_out = datetime.utcnow()
    db.commit()
    db.refresh(visitor)

    return visitor
