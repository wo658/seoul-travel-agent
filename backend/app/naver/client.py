"""Naver Local Search API client."""

import logging
from typing import Dict, List, Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class NaverLocalClient:
    """Client for Naver Local Search API."""

    BASE_URL = "https://openapi.naver.com/v1/search/local.json"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """Initialize Naver Local API client.

        Args:
            client_id: Naver API Client ID (defaults to settings)
            client_secret: Naver API Client Secret (defaults to settings)
        """
        self.client_id = client_id or settings.NAVER_CLIENT_ID
        self.client_secret = client_secret or settings.NAVER_CLIENT_SECRET

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Naver API credentials not configured. "
                "Please set NAVER_CLIENT_ID and NAVER_CLIENT_SECRET in .env file."
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        return {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    async def search_local(
        self,
        query: str,
        display: int = 5,
        start: int = 1,
        sort: str = "random",
    ) -> List[Dict]:
        """Search for local places using Naver Local API.

        Args:
            query: Search query (e.g., "강남역 맛집", "명동 카페")
            display: Number of results to return (1-5, default: 5)
            start: Start position (default: 1)
            sort: Sort order - "random" or "comment" (default: "random")

        Returns:
            List of place dictionaries with the following fields:
            - title: Place name (HTML tags removed)
            - link: Naver place URL
            - category: Category classification
            - description: Place description
            - telephone: Phone number
            - address: Old address format
            - roadAddress: New road address format
            - mapx: X coordinate (longitude * 10^7)
            - mapy: Y coordinate (latitude * 10^7)

        Raises:
            httpx.HTTPError: If API request fails
        """
        params = {
            "query": query,
            "display": min(display, 5),  # Max 5 per request
            "start": start,
            "sort": sort,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.BASE_URL,
                    headers=self._get_headers(),
                    params=params,
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()

                items = data.get("items", [])
                logger.info(f"Found {len(items)} results for query: {query}")

                # Convert coordinates to standard WGS84 format
                for item in items:
                    if item.get("mapx") and item.get("mapy"):
                        item["longitude"] = int(item["mapx"]) / 10000000
                        item["latitude"] = int(item["mapy"]) / 10000000

                    # Remove HTML tags from title
                    if item.get("title"):
                        item["title"] = (
                            item["title"]
                            .replace("<b>", "")
                            .replace("</b>", "")
                            .replace("&amp;", "&")
                        )

                return items

        except httpx.HTTPError as e:
            logger.error(f"Naver Local API error: {e}")
            raise

    async def search_nearby_restaurants(
        self,
        latitude: float,
        longitude: float,
        query: str = "맛집",
        radius_km: float = 1.0,
        limit: int = 5,
    ) -> List[Dict]:
        """Search for restaurants near a specific location.

        Args:
            latitude: Center point latitude
            longitude: Center point longitude
            query: Additional search keyword (default: "맛집")
            radius_km: Search radius in kilometers (default: 1.0)
            limit: Maximum number of results (default: 5)

        Returns:
            List of restaurant dictionaries
        """
        # Convert coordinates to area name for better search results
        # In production, you might want to use reverse geocoding
        search_query = f"{query}"

        results = await self.search_local(
            query=search_query,
            display=min(limit, 5),
            sort="random",
        )

        # Filter by distance if needed (simple approximation)
        # For production, implement proper haversine distance calculation
        return results[:limit]

    async def search_nearby_accommodations(
        self,
        latitude: float,
        longitude: float,
        query: str = "숙박",
        radius_km: float = 2.0,
        limit: int = 5,
    ) -> List[Dict]:
        """Search for accommodations near a specific location.

        Args:
            latitude: Center point latitude
            longitude: Center point longitude
            query: Additional search keyword (default: "숙박")
            radius_km: Search radius in kilometers (default: 2.0)
            limit: Maximum number of results (default: 5)

        Returns:
            List of accommodation dictionaries
        """
        search_query = f"{query}"

        results = await self.search_local(
            query=search_query,
            display=min(limit, 5),
            sort="random",
        )

        return results[:limit]
