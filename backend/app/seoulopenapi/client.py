"""Seoul Open API HTTP Client"""

import httpx
from typing import List, Optional
from app.config import settings
from .schemas import (
    TbVwNatureResponse,
    TbVwRestaurantsResponse,
    TbVwAttractionsResponse,
    VenueData,
)


class SeoulOpenAPIError(Exception):
    """Seoul Open API 에러"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Seoul OpenAPI Error [{code}]: {message}")


class SeoulOpenAPIClient:
    """서울시 관광 OpenAPI 클라이언트"""

    BASE_URL = "http://openapi.seoul.go.kr:8088"

    # Service names
    SERVICE_NATURE = "TbVwNature"
    SERVICE_RESTAURANTS = "TbVwRestaurants"
    SERVICE_ATTRACTIONS = "TbVwAttractions"

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: 서울 OpenAPI 인증키. None이면 settings에서 가져옴.
        """
        self.api_key = api_key or settings.SEOUL_OPENAPI_KEY
        if not self.api_key:
            raise ValueError("Seoul OpenAPI key is required")

        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """클라이언트 연결 종료"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _build_url(
        self,
        service: str,
        start_index: int = 1,
        end_index: int = 100,
        response_type: str = "json",
    ) -> str:
        """API URL 생성

        Format: BASE_URL/{API_KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/
        """
        return f"{self.BASE_URL}/{self.api_key}/{response_type}/{service}/{start_index}/{end_index}/"

    async def _request(
        self,
        service: str,
        start_index: int = 1,
        end_index: int = 100,
    ) -> dict:
        """API 요청 실행"""
        url = self._build_url(service, start_index, end_index)

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            # Check for API-level errors
            if service in data:
                result = data[service].get("RESULT")
                if result and result.get("CODE") != "INFO-000":
                    raise SeoulOpenAPIError(
                        code=result.get("CODE", "UNKNOWN"),
                        message=result.get("MESSAGE", "Unknown error"),
                    )

            return data

        except httpx.HTTPStatusError as e:
            raise SeoulOpenAPIError(
                code=f"HTTP_{e.response.status_code}",
                message=f"HTTP error: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise SeoulOpenAPIError(
                code="REQUEST_ERROR", message=f"Request failed: {str(e)}"
            )
        except Exception as e:
            raise SeoulOpenAPIError(code="UNKNOWN", message=str(e))

    async def get_nature_attractions(
        self, start_index: int = 1, end_index: int = 100, language: str = "ko"
    ) -> List[VenueData]:
        """자연 관광지 목록 조회

        Args:
            start_index: 시작 인덱스 (1부터 시작)
            end_index: 종료 인덱스
            language: 언어 코드 (ko, en, ja, zh 등)

        Returns:
            VenueData 목록
        """
        data = await self._request(self.SERVICE_NATURE, start_index, end_index)
        response = TbVwNatureResponse(**data)

        venues = []
        if response.TbVwNature.row:
            for venue in response.TbVwNature.row:
                # Filter by language if specified
                if language and venue.LANG_CODE_ID and venue.LANG_CODE_ID != language:
                    continue
                venues.append(VenueData.from_nature(venue))

        return venues

    async def get_restaurants(
        self, start_index: int = 1, end_index: int = 100, language: str = "ko"
    ) -> List[VenueData]:
        """음식점 목록 조회

        Args:
            start_index: 시작 인덱스 (1부터 시작)
            end_index: 종료 인덱스
            language: 언어 코드 (ko, en, ja, zh 등)

        Returns:
            VenueData 목록
        """
        data = await self._request(self.SERVICE_RESTAURANTS, start_index, end_index)
        response = TbVwRestaurantsResponse(**data)

        venues = []
        if response.TbVwRestaurants.row:
            for venue in response.TbVwRestaurants.row:
                # Filter by language if specified
                if language and venue.LANG_CODE_ID and venue.LANG_CODE_ID != language:
                    continue
                venues.append(VenueData.from_restaurant(venue))

        return venues

    async def get_attractions(
        self, start_index: int = 1, end_index: int = 100, language: str = "ko"
    ) -> List[VenueData]:
        """관광명소 목록 조회

        Args:
            start_index: 시작 인덱스 (1부터 시작)
            end_index: 종료 인덱스
            language: 언어 코드 (ko, en, ja, zh 등)

        Returns:
            VenueData 목록
        """
        data = await self._request(self.SERVICE_ATTRACTIONS, start_index, end_index)
        response = TbVwAttractionsResponse(**data)

        venues = []
        if response.TbVwAttractions.row:
            for venue in response.TbVwAttractions.row:
                # Filter by language if specified
                if language and venue.LANG_CODE_ID and venue.LANG_CODE_ID != language:
                    continue
                venues.append(VenueData.from_attraction(venue))

        return venues

    async def get_all_venues(
        self, start_index: int = 1, end_index: int = 100, language: str = "ko"
    ) -> dict[str, List[VenueData]]:
        """모든 카테고리의 장소 조회

        Args:
            start_index: 시작 인덱스
            end_index: 종료 인덱스
            language: 언어 코드

        Returns:
            카테고리별 VenueData 목록 딕셔너리
            {
                "nature": [...],
                "restaurants": [...],
                "attractions": [...]
            }
        """
        # Fetch all categories in parallel
        nature, restaurants, attractions = await asyncio.gather(
            self.get_nature_attractions(start_index, end_index, language),
            self.get_restaurants(start_index, end_index, language),
            self.get_attractions(start_index, end_index, language),
            return_exceptions=True,
        )

        result = {}

        # Handle potential errors
        if isinstance(nature, Exception):
            result["nature"] = []
        else:
            result["nature"] = nature

        if isinstance(restaurants, Exception):
            result["restaurants"] = []
        else:
            result["restaurants"] = restaurants

        if isinstance(attractions, Exception):
            result["attractions"] = []
        else:
            result["attractions"] = attractions

        return result

    async def get_total_count(self, service: str) -> int:
        """특정 서비스의 총 데이터 개수 조회

        Args:
            service: 서비스명 (SERVICE_NATURE, SERVICE_RESTAURANTS, SERVICE_ATTRACTIONS)

        Returns:
            총 데이터 개수
        """
        data = await self._request(service, 1, 1)

        if service in data:
            return data[service].get("list_total_count", 0)

        return 0


# Import asyncio at the end to avoid circular import
import asyncio
