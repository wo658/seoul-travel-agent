"""Plan domain models."""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class TravelPlan(Base):
    """Travel plan model."""

    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    # AI generated content
    itinerary = Column(JSON)
    recommendations = Column(JSON)

    # Metadata
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="plans")
    conversation = relationship(
        "Conversation",
        back_populates="travel_plan",
        foreign_keys="[TravelPlan.conversation_id]",
        uselist=False,
    )
