"""Tourist attraction database models."""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base


class TouristAttraction(Base):
    """Tourist attraction model from Seoul Tourism API.

    Stores official Seoul tourist attractions with complete information
    including coordinates for location-based services.
    """

    __tablename__ = "tourist_attractions"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String, nullable=False, index=True)  # 관광지명
    category = Column(String, nullable=False, index=True)  # 관광지구분

    # Address information
    road_address = Column(String)  # 소재지도로명주소
    jibun_address = Column(String)  # 소재지지번주소

    # Location coordinates (WGS84)
    latitude = Column(Float, nullable=False, index=True)  # 위도
    longitude = Column(Float, nullable=False, index=True)  # 경도

    # Facility information
    area = Column(String)  # 면적
    public_facilities = Column(Text)  # 공공편익시설정보
    accommodation_facilities = Column(Text)  # 숙박시설정보
    sports_facilities = Column(Text)  # 운동및오락시설정보
    cultural_facilities = Column(Text)  # 휴양및문화시설정보
    hospitality_facilities = Column(Text)  # 접객시설정보
    support_facilities = Column(Text)  # 지원시설정보

    # Capacity information
    capacity = Column(Integer)  # 수용인원수
    parking_spaces = Column(Integer)  # 주차가능수

    # Description
    introduction = Column(Text)  # 관광지소개

    # Management information
    phone = Column(String)  # 관리기관전화번호
    manager_name = Column(String)  # 관리기관명

    # Metadata
    designated_date = Column(String)  # 지정일자
    reference_date = Column(String)  # 데이터기준일자
    provider_code = Column(String)  # 제공기관코드
    provider_name = Column(String)  # 제공기관명

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def get_embedding_description(self) -> str:
        """Generate description for embedding generation.

        Returns:
            Formatted description string for embedding
        """
        parts = [f"이름: {self.name}", f"구분: {self.category}"]

        # Address
        if self.road_address:
            parts.append(f"주소: {self.road_address}")

        # Introduction
        if self.introduction:
            # Limit introduction to 200 characters for embedding
            intro = self.introduction[:200]
            parts.append(f"소개: {intro}")

        # Facilities
        facilities = []
        if self.public_facilities:
            facilities.append(self.public_facilities)
        if self.cultural_facilities:
            facilities.append(self.cultural_facilities)
        if facilities:
            parts.append(f"시설: {', '.join(facilities)}")

        return " | ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert attraction to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "road_address": self.road_address,
            "jibun_address": self.jibun_address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "area": self.area,
            "capacity": self.capacity,
            "parking_spaces": self.parking_spaces,
            "introduction": self.introduction,
            "phone": self.phone,
            "manager_name": self.manager_name,
            "facilities": {
                "public": self.public_facilities,
                "accommodation": self.accommodation_facilities,
                "sports": self.sports_facilities,
                "cultural": self.cultural_facilities,
                "hospitality": self.hospitality_facilities,
                "support": self.support_facilities,
            },
            "designated_date": self.designated_date,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """String representation of TouristAttraction."""
        return f"<TouristAttraction(id={self.id}, name='{self.name}')>"
