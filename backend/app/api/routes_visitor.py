from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.visitor import VisitorCreate, VisitorOut
from app.schemas.approval import ApprovalOut
from app.services.visitor_service import VisitorService
from app.core.config import SessionLocal
from app.utils.email import send_visitor_notification
from app.utils.qr_generator import generate_qr_and_upload
from app.schemas.approval import ApprovalStatus
from app.models import Employee, PreApproval, Approval
from datetime import datetime
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

    # Check if already approved
    existing_approval = (
        db.query(Approval)
        .filter_by(visitor_id=visitor_id)
        .order_by(Approval.requested_at.desc())
        .first()
    )

    if existing_approval:
        logger.info(f"Approval status: {existing_approval.status}, Decision at: {existing_approval.decision_at}")

    if not existing_approval or existing_approval.status == ApprovalStatus.PENDING:
        now = datetime.utcnow()
        logger.info(f"No approved record found. Checking pre-approval for {visitor_id} at {now.isoformat()}")

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

            logger.info(f"Valid pre-approval found. max_per_day={pre.max_visits_per_day}, visits_today={visits_today}")

            if visits_today < pre.max_visits_per_day:
                try:
                    auto_approval = Approval(
                        visitor_id=visitor_id,
                        employee_id=pre.employee_id,
                        status=ApprovalStatus.APPROVED,
                        decision_at=datetime.utcnow(),
                        requested_at=datetime.utcnow()
                    )
                    db.add(auto_approval)

                    if not visitor.badge_url:
                        badge_url = generate_qr_and_upload(str(visitor.id))
                        visitor.badge_url = badge_url
                        visitor.check_in = datetime.utcnow()

                    db.commit()
                    db.refresh(auto_approval)
                    db.refresh(visitor)
                    logger.info(f"Auto-approved and generated badge for visitor {visitor_id}")

                except Exception as e:
                    db.rollback()
                    logger.error(f"❌ Failed to auto-approve visitor {visitor_id}: {e}", exc_info=True)

    # Always return the latest approval (after any potential update)
    latest_approval = (
        db.query(Approval)
        .filter(Approval.visitor_id == visitor_id, Approval.status == ApprovalStatus.APPROVED)
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
        raise HTTPException(status_code=400, detail="Visitor already checkout out")
    
    visitor.check_out = datetime.utcnow()
    db.commit()
    db.refresh(visitor)

    return visitor