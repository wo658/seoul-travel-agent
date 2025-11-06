"""Pydantic schemas for Seoul Open API responses."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BaseAPIResponse(BaseModel):
    """Base response model for Seoul Open API."""

    RESULT: Optional[Dict[str, Any]] = None


class NatureItem(BaseModel):
    """자연 관광지 (TbVwNature) item schema."""

    POST_SN: str = Field(..., description="게시물 일련번호 (고유 ID)")
    POST_SJ: str = Field(..., description="게시물 제목 (명칭)")
    ADDRESS: Optional[str] = Field(None, description="구주소")
    NEW_ADDRESS: Optional[str] = Field(None, description="신주소")
    CMMN_TELNO: Optional[str] = Field(None, description="대표 전화번호")
    CMMN_HMPG_URL: Optional[str] = Field(None, description="홈페이지 URL")
    CMMN_INTRCN_CN: Optional[str] = Field(None, description="소개 내용")
    CMMN_USE_TIME: Optional[str] = Field(None, description="이용시간")
    SUBWAY_INFO: Optional[str] = Field(None, description="지하철 정보")
    X_COORD: Optional[float] = Field(None, description="X좌표 (경도)")
    Y_COORD: Optional[float] = Field(None, description="Y좌표 (위도)")


class RestaurantItem(BaseModel):
    """음식점 (TbVwRestaurants) item schema."""

    POST_SN: str = Field(..., description="게시물 일련번호")
    POST_SJ: str = Field(..., description="게시물 제목 (상호명)")
    ADDRESS: Optional[str] = Field(None, description="구주소")
    NEW_ADDRESS: Optional[str] = Field(None, description="신주소")
    CMMN_TELNO: Optional[str] = Field(None, description="전화번호")
    CMMN_HMPG_URL: Optional[str] = Field(None, description="홈페이지")
    FD_REPRSNT_MENU: Optional[str] = Field(None, description="대표 메뉴")
    CMMN_USE_TIME: Optional[str] = Field(None, description="이용시간")
    SUBWAY_INFO: Optional[str] = Field(None, description="지하철 정보")
    X_COORD: Optional[float] = Field(None, description="X좌표")
    Y_COORD: Optional[float] = Field(None, description="Y좌표")


class AttractionItem(BaseModel):
    """관광명소 (TbVwAttractions) item schema."""

    POST_SN: str = Field(..., description="게시물 일련번호")
    POST_SJ: str = Field(..., description="게시물 제목")
    ADDRESS: Optional[str] = Field(None, description="구주소")
    NEW_ADDRESS: Optional[str] = Field(None, description="신주소")
    CMMN_TELNO: Optional[str] = Field(None, description="전화번호")
    CMMN_HMPG_URL: Optional[str] = Field(None, description="홈페이지")
    CMMN_INTRCN_CN: Optional[str] = Field(None, description="소개 내용")
    CMMN_USE_TIME: Optional[str] = Field(None, description="이용시간")
    SUBWAY_INFO: Optional[str] = Field(None, description="지하철 정보")
    TAG: Optional[str] = Field(None, description="태그")
    BF_DESC: Optional[str] = Field(None, description="장애인 편의시설")
    X_COORD: Optional[float] = Field(None, description="X좌표")
    Y_COORD: Optional[float] = Field(None, description="Y좌표")


class AccommodationItem(BaseModel):
    """관광숙박업 (LOCALDATA_031101) item schema."""

    MGTNO: str = Field(..., description="관리번호 (고유 ID)")
    BPLCNM: str = Field(..., description="사업장명")
    SITEWHLADDR: Optional[str] = Field(None, description="지번 주소")
    RDNWHLADDR: Optional[str] = Field(None, description="도로명 주소")
    SITETEL: Optional[str] = Field(None, description="전화번호")
    TRDSTATENM: Optional[str] = Field(None, description="영업 상태명")
    STROOMCNT: Optional[int] = Field(None, description="객실수")
    AFC: Optional[str] = Field(None, description="편의시설")
    TRSTLODGCLNM: Optional[str] = Field(None, description="관광숙박업 구분명")
    X: Optional[float] = Field(None, description="X좌표")
    Y: Optional[float] = Field(None, description="Y좌표")


class NatureResponse(BaseModel):
    """TbVwNature API response."""

    TbVwNature: List[Dict[str, Any]]


class RestaurantResponse(BaseModel):
    """TbVwRestaurants API response."""

    TbVwRestaurants: List[Dict[str, Any]]


class AttractionResponse(BaseModel):
    """TbVwAttractions API response."""

    TbVwAttractions: List[Dict[str, Any]]


class AccommodationResponse(BaseModel):
    """LOCALDATA_031101 API response."""

    LOCALDATA_031101: List[Dict[str, Any]]
