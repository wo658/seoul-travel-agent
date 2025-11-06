"""Seoul Open API HTTP client."""

import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)


class SeoulOpenAPIClient:
    """HTTP client for Seoul Open Data API.

    Base URL: http://openapi.seoul.go.kr:8088/{API_KEY}/json/{SERVICE}/{START}/{END}/
    """

    BASE_URL = "http://openapi.seoul.go.kr:8088"

    def __init__(self, api_key: str):
        """Initialize Seoul Open API client.

        Args:
            api_key: Seoul Open Data API key from data.go.kr
        """
        if not api_key:
            raise ValueError("Seoul Open API key is required")

        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _fetch_paginated(
        self,
        service_name: str,
        start: int = 1,
        end: int = 1000,
        max_records: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch data with pagination support.

        Args:
            service_name: API service name (e.g., "TbVwNature")
            start: Start index (1-based)
            end: End index
            max_records: Maximum number of records to fetch (None = all)

        Returns:
            List of records

        Raises:
            httpx.HTTPError: If API request fails
        """
        all_records = []
        current_start = start
        page_size = end - start + 1

        while True:
            current_end = current_start + page_size - 1

            # Build URL
            url = f"{self.BASE_URL}/{self.api_key}/json/{service_name}/{current_start}/{current_end}/"

            logger.info(
                f"Fetching {service_name}: {current_start}-{current_end}"
            )

            try:
                response = await self.client.get(url)
                response.raise_for_status()
                data = response.json()

                # Check for API errors
                if "RESULT" in data:
                    result = data["RESULT"]
                    code = result.get("CODE")
                    message = result.get("MESSAGE", "")

                    if code == "INFO-000":
                        # Success but no data
                        logger.info(f"No more data for {service_name}")
                        break
                    elif code != "INFO-000":
                        logger.warning(
                            f"API returned code {code}: {message}"
                        )
                        break

                # Extract records from response
                records = data.get(service_name, {}).get("row", [])

                if not records:
                    logger.info(f"No records found for {service_name}")
                    break

                all_records.extend(records)
                logger.info(
                    f"Fetched {len(records)} records, total: {len(all_records)}"
                )

                # Check if we've reached max_records
                if max_records and len(all_records) >= max_records:
                    all_records = all_records[:max_records]
                    logger.info(f"Reached max_records limit: {max_records}")
                    break

                # Check if this is the last page
                if len(records) < page_size:
                    logger.info("Reached last page")
                    break

                # Move to next page
                current_start = current_end + 1

            except httpx.HTTPError as e:
                logger.error(f"HTTP error fetching {service_name}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error fetching {service_name}: {e}")
                raise

        return all_records

    async def fetch_nature_sites(
        self, max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch natural tourism sites (TbVwNature).

        Args:
            max_records: Maximum number of records to fetch

        Returns:
            List of nature site records
        """
        return await self._fetch_paginated(
            "TbVwNature", max_records=max_records
        )

    async def fetch_restaurants(
        self, max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch restaurant information (TbVwRestaurants).

        Args:
            max_records: Maximum number of records to fetch

        Returns:
            List of restaurant records
        """
        return await self._fetch_paginated(
            "TbVwRestaurants", max_records=max_records
        )

    async def fetch_attractions(
        self, max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch tourism attractions (TbVwAttractions).

        Args:
            max_records: Maximum number of records to fetch

        Returns:
            List of attraction records
        """
        return await self._fetch_paginated(
            "TbVwAttractions", max_records=max_records
        )

    async def fetch_accommodations(
        self, max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch accommodation information (LOCALDATA_031101).

        Args:
            max_records: Maximum number of records to fetch

        Returns:
            List of accommodation records
        """
        return await self._fetch_paginated(
            "LOCALDATA_031101", max_records=max_records
        )

    async def close(self):
        """Close HTTP client connection."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
