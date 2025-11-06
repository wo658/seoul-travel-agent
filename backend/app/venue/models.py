"""Venue database models for Seoul Open API integration."""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base


class Venue(Base):
    """Venue model for tourism locations.

    Supports attractions, restaurants, accommodations, and natural sites
    from Seoul Open API. Vector embeddings are stored in ChromaDB separately.
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

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Indexes
    __table_args__ = (Index("idx_category_status", "category", "business_status"),)

    def get_embedding_description(self) -> str:
        """Generate description for embedding generation.

        Returns:
            Formatted description string for embedding
        """
        parts = [f"이름: {self.name}", f"카테고리: {self.category}"]

        # Address
        if self.new_address:
            parts.append(f"주소: {self.new_address}")
        elif self.address:
            parts.append(f"주소: {self.address}")

        # Transportation
        if self.subway_info:
            parts.append(f"교통: {self.subway_info}")

        # Category-specific extra info
        if self.extra_info:
            if self.category == "restaurant":
                menu = self.extra_info.get("representative_menu")
                if menu:
                    parts.append(f"대표메뉴: {menu}")

            elif self.category == "attraction":
                tags = self.extra_info.get("tags")
                if tags:
                    parts.append(f"특징: {tags}")
                accessibility = self.extra_info.get("accessibility")
                if accessibility:
                    parts.append(f"편의시설: {accessibility}")

            elif self.category == "accommodation":
                acc_type = self.extra_info.get("accommodation_type")
                if acc_type:
                    parts.append(f"숙박유형: {acc_type}")
                facilities = self.extra_info.get("facilities")
                if facilities:
                    parts.append(f"시설: {facilities}")

            elif self.category == "nature":
                tags = self.extra_info.get("tags")
                if tags:
                    parts.append(f"특징: {tags}")

        # Operating hours
        if self.operating_hours:
            parts.append(f"운영시간: {self.operating_hours}")

        return " | ".join(parts)

    def get_llm_summary(self, similarity: float) -> str:
        """Generate formatted summary for LLM context.

        Args:
            similarity: Similarity score (0.0-1.0)

        Returns:
            Formatted summary string
        """
        info_parts = [f"- {self.name} (관련도: {similarity:.2f})"]

        # Category-specific information
        if self.category == "restaurant":
            if self.extra_info and "representative_menu" in self.extra_info:
                menu = self.extra_info["representative_menu"]
                info_parts.append(f"대표메뉴: {menu}")
            else:
                info_parts.append("음식점")

        elif self.category == "accommodation":
            if self.extra_info:
                room_count = self.extra_info.get("room_count")
                acc_type = self.extra_info.get("accommodation_type")
                facilities = self.extra_info.get("facilities")

                acc_info = []
                if acc_type:
                    acc_info.append(acc_type)
                if room_count:
                    acc_info.append(f"객실 {room_count}개")
                if facilities:
                    acc_info.append(f"시설: {facilities}")

                if acc_info:
                    info_parts.append(", ".join(acc_info))
                else:
                    info_parts.append("숙박시설")
            else:
                info_parts.append("숙박시설")

        elif self.category == "attraction":
            if self.extra_info and "tags" in self.extra_info:
                tags = self.extra_info["tags"]
                info_parts.append(f"특징: {tags}")
            else:
                info_parts.append("관광명소")

        elif self.category == "nature":
            if self.extra_info and "tags" in self.extra_info:
                tags = self.extra_info["tags"]
                info_parts.append(f"특징: {tags}")
            else:
                info_parts.append("자연명소")

        # Transportation and operating info
        if self.subway_info:
            info_parts.append(f"교통: {self.subway_info}")

        if self.operating_hours:
            info_parts.append(f"운영: {self.operating_hours}")

        if self.phone:
            info_parts.append(f"전화: {self.phone}")

        return " | ".join(info_parts)

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
