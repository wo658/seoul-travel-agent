"""Seoul Open API Response Schemas"""

from typing import Optional, List
from pydantic import BaseModel, Field


# Common API Response Structure
class APIResult(BaseModel):
    """API 요청 결과"""
    CODE: str
    MESSAGE: str


class BaseAPIResponse(BaseModel):
    """기본 API 응답 구조"""
    list_total_count: Optional[int] = Field(None, description="총 데이터 건수")
    RESULT: Optional[APIResult] = Field(None, description="요청 결과")


# Common Venue Fields
class BaseVenue(BaseModel):
    """공통 장소 필드"""
    POST_SN: str = Field(..., description="고유번호")
    LANG_CODE_ID: Optional[str] = Field(None, description="언어")
    POST_SJ: Optional[str] = Field(None, description="상호명")
    POST_URL: Optional[str] = Field(None, description="콘텐츠URL")
    ADDRESS: Optional[str] = Field(None, description="주소")
    NEW_ADDRESS: Optional[str] = Field(None, description="신주소")
    CMMN_TELNO: Optional[str] = Field(None, description="전화번호")
    CMMN_HMPG_URL: Optional[str] = Field(None, description="웹사이트")
    CMMN_USE_TIME: Optional[str] = Field(None, description="운영시간")
    CMMN_BSNDE: Optional[str] = Field(None, description="운영요일")
    CMMN_RSTDE: Optional[str] = Field(None, description="휴무일")
    SUBWAY_INFO: Optional[str] = Field(None, description="교통정보")


# Nature Attractions (TbVwNature)
class NatureVenue(BaseVenue):
    """자연 관광지"""
    pass


class NatureResponse(BaseAPIResponse):
    """자연 관광지 API 응답"""
    row: Optional[List[NatureVenue]] = Field(None, description="자연 관광지 목록")


class TbVwNatureResponse(BaseModel):
    """TbVwNature 서비스 응답"""
    TbVwNature: NatureResponse


# Restaurants (TbVwRestaurants)
class RestaurantVenue(BaseVenue):
    """음식점"""
    CMMN_HMPG_LANG: Optional[str] = Field(None, description="홈페이지 언어")
    FD_REPRSNT_MENU: Optional[str] = Field(None, description="대표메뉴")


class RestaurantResponse(BaseAPIResponse):
    """음식점 API 응답"""
    row: Optional[List[RestaurantVenue]] = Field(None, description="음식점 목록")


class TbVwRestaurantsResponse(BaseModel):
    """TbVwRestaurants 서비스 응답"""
    TbVwRestaurants: RestaurantResponse


# Attractions (TbVwAttractions)
class AttractionVenue(BaseVenue):
    """관광명소"""
    CMMN_FAX: Optional[str] = Field(None, description="팩스번호")
    TAG: Optional[str] = Field(None, description="태그")
    BF_DESC: Optional[str] = Field(None, description="장애인편의시설")


class AttractionResponse(BaseAPIResponse):
    """관광명소 API 응답"""
    row: Optional[List[AttractionVenue]] = Field(None, description="관광명소 목록")


class TbVwAttractionsResponse(BaseModel):
    """TbVwAttractions 서비스 응답"""
    TbVwAttractions: AttractionResponse


# Unified Venue Data Schema (for internal use)
class VenueData(BaseModel):
    """통일된 장소 데이터 스키마"""
    venue_id: str = Field(..., description="고유번호")
    category: str = Field(..., description="카테고리 (nature/restaurant/attraction)")
    name: str = Field(..., description="장소명")

    # Location
    address: Optional[str] = Field(None, description="주소")
    new_address: Optional[str] = Field(None, description="신주소")

    # Contact
    phone: Optional[str] = Field(None, description="전화번호")
    fax: Optional[str] = Field(None, description="팩스번호")
    website: Optional[str] = Field(None, description="웹사이트")

    # Operating Info
    operating_hours: Optional[str] = Field(None, description="운영시간")
    operating_days: Optional[str] = Field(None, description="운영요일")
    closed_days: Optional[str] = Field(None, description="휴무일")

    # Additional Info
    subway_info: Optional[str] = Field(None, description="교통정보 (지하철)")
    content_url: Optional[str] = Field(None, description="콘텐츠 URL")
    tags: Optional[str] = Field(None, description="태그")

    # Category-specific
    representative_menu: Optional[str] = Field(None, description="대표메뉴 (음식점)")
    accessibility: Optional[str] = Field(None, description="장애인편의시설 (관광명소)")
    homepage_language: Optional[str] = Field(None, description="홈페이지 언어 (음식점)")
    language: Optional[str] = Field(None, description="언어코드")

    @classmethod
    def from_nature(cls, venue: NatureVenue) -> "VenueData":
        """자연 관광지 데이터를 VenueData로 변환"""
        return cls(
            venue_id=venue.POST_SN,
            category="nature",
            name=venue.POST_SJ or "",
            address=venue.ADDRESS,
            new_address=venue.NEW_ADDRESS,
            phone=venue.CMMN_TELNO,
            website=venue.CMMN_HMPG_URL,
            operating_hours=venue.CMMN_USE_TIME,
            operating_days=venue.CMMN_BSNDE,
            closed_days=venue.CMMN_RSTDE,
            subway_info=venue.SUBWAY_INFO,
            content_url=venue.POST_URL,
            language=venue.LANG_CODE_ID,
        )

    @classmethod
    def from_restaurant(cls, venue: RestaurantVenue) -> "VenueData":
        """음식점 데이터를 VenueData로 변환"""
        return cls(
            venue_id=venue.POST_SN,
            category="restaurant",
            name=venue.POST_SJ or "",
            address=venue.ADDRESS,
            new_address=venue.NEW_ADDRESS,
            phone=venue.CMMN_TELNO,
            website=venue.CMMN_HMPG_URL,
            operating_hours=venue.CMMN_USE_TIME,
            operating_days=venue.CMMN_BSNDE,
            closed_days=venue.CMMN_RSTDE,
            subway_info=venue.SUBWAY_INFO,
            content_url=venue.POST_URL,
            representative_menu=venue.FD_REPRSNT_MENU,
            homepage_language=venue.CMMN_HMPG_LANG,
            language=venue.LANG_CODE_ID,
        )

    @classmethod
    def from_attraction(cls, venue: AttractionVenue) -> "VenueData":
        """관광명소 데이터를 VenueData로 변환"""
        return cls(
            venue_id=venue.POST_SN,
            category="attraction",
            name=venue.POST_SJ or "",
            address=venue.ADDRESS,
            new_address=venue.NEW_ADDRESS,
            phone=venue.CMMN_TELNO,
            fax=venue.CMMN_FAX,
            website=venue.CMMN_HMPG_URL,
            operating_hours=venue.CMMN_USE_TIME,
            operating_days=venue.CMMN_BSNDE,
            closed_days=venue.CMMN_RSTDE,
            subway_info=venue.SUBWAY_INFO,
            content_url=venue.POST_URL,
            tags=venue.TAG,
            accessibility=venue.BF_DESC,
            language=venue.LANG_CODE_ID,
        )
