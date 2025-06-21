"""
repos/visitor_repo.py — Repository for managing visitor data operations.
"""

from sqlalchemy.orm import Session
from app.models import Visitor


class VisitorRepository:
    """
    Handles database operations related to the Visitor entity.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def create_visitor(self, visitor_data: dict) -> Visitor:
        """
        Creates a new visitor record in the database.

        Args:
            visitor_data (dict): Dictionary containing visitor fields.

        Returns:
            Visitor: The newly created visitor record.
        """
        visitor = Visitor(**visitor_data)
        self.db.add(visitor)
        self.db.commit()
        self.db.refresh(visitor)
        return visitor

    def get_visitor_by_id(self, visitor_id: int) -> Visitor | None:
        """
        Fetches a visitor by their ID.

        Args:
            visitor_id (int): Visitor's unique ID.

        Returns:
            Visitor | None: Visitor object if found, else None.
        """
        return self.db.query(Visitor).filter(Visitor.id == visitor_id).first()
