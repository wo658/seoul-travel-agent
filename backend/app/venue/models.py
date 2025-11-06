"""Venue database models with vector embedding support."""

from datetime import datetime
from typing import Any, Dict

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON

from app.database import Base


class Venue(Base):
    """Venue model for tourism locations with vector search support.

    Supports attractions, restaurants, accommodations, and natural sites
    from Seoul Open API with semantic search via pgvector embeddings.
    """

    __tablename__ = "venues"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Unique identifier from external API
    external_id = Column(String, unique=True, nullable=False, index=True)

    # Basic information
    name = Column(String, nullable=False, index=True)
    category = Column(
        String, nullable=False, index=True
    )  # nature, restaurant, attraction, accommodation

    # Address information
    address = Column(String)  # Old address format
    new_address = Column(String)  # New address format (road-based)
    postal_code = Column(String)

    # Location coordinates
    x_coord = Column(Float)  # Longitude
    y_coord = Column(Float)  # Latitude

    # Contact information
    phone = Column(String)
    website = Column(String)
    content_url = Column(String)

    # Operating information
    operating_hours = Column(Text)
    operating_days = Column(String)
    closed_days = Column(String)
    business_status = Column(String, index=True)  # For filtering active venues

    # Transportation
    subway_info = Column(Text)

    # Category-specific additional information (JSON)
    # Examples:
    # - restaurant: {"representative_menu": "...", "price_range": "..."}
    # - accommodation: {"room_count": 10, "facilities": "...", "accommodation_type": "..."}
    # - attraction: {"tags": "...", "accessibility": "..."}
    extra_info = Column(JSON)

    # Vector embedding for semantic search (OpenAI text-embedding-3-small dimension=1536)
    description_embedding = Column(Vector(1536))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Indexes for vector similarity search
    __table_args__ = (
        Index(
            "idx_description_embedding",
            "description_embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
        ),
        Index("idx_category_status", "category", "business_status"),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert venue to dictionary representation."""
        return {
            "id": self.id,
            "external_id": self.external_id,
            "name": self.name,
            "category": self.category,
            "address": self.address,
            "new_address": self.new_address,
            "postal_code": self.postal_code,
            "x_coord": self.x_coord,
            "y_coord": self.y_coord,
            "phone": self.phone,
            "website": self.website,
            "content_url": self.content_url,
            "operating_hours": self.operating_hours,
            "operating_days": self.operating_days,
            "closed_days": self.closed_days,
            "business_status": self.business_status,
            "subway_info": self.subway_info,
            "extra_info": self.extra_info,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """String representation of Venue."""
        return f"<Venue(id={self.id}, name='{self.name}', category='{self.category}')>"
