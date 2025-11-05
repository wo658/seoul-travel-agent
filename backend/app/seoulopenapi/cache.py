"""SQLite-based caching layer for Seoul Open API"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Any, List
import aiosqlite
from pathlib import Path
from .schemas import VenueData


class CacheManager:
    """SQLite 기반 캐시 매니저"""

    DEFAULT_TTL = 24 * 60 * 60  # 24 hours in seconds

    def __init__(self, db_path: str = "seoul_openapi_cache.db"):
        """
        Args:
            db_path: SQLite 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self._initialized = False

    async def initialize(self):
        """캐시 데이터베이스 초기화"""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires_at REAL NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )
            # Index for efficient expiration queries
            await db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_expires_at
                ON cache(expires_at)
                """
            )
            await db.commit()

        self._initialized = True

    @staticmethod
    def _make_key(service: str, params: dict) -> str:
        """캐시 키 생성

        Format: seoul:{service}:{params_hash}

        Args:
            service: 서비스명 (nature, restaurants, attractions)
            params: 파라미터 딕셔너리

        Returns:
            캐시 키
        """
        # Sort params for consistent hashing
        params_str = json.dumps(params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
        return f"seoul:{service}:{params_hash}"

    async def get(self, service: str, params: dict) -> Optional[List[VenueData]]:
        """캐시에서 데이터 조회

        Args:
            service: 서비스명
            params: 파라미터

        Returns:
            캐시된 VenueData 목록 또는 None
        """
        await self.initialize()

        key = self._make_key(service, params)
        now = time.time()

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """
                SELECT value, expires_at
                FROM cache
                WHERE key = ? AND expires_at > ?
                """,
                (key, now),
            ) as cursor:
                row = await cursor.fetchone()

                if row:
                    value_json = row[0]
                    try:
                        # Parse JSON and convert to VenueData objects
                        data = json.loads(value_json)
                        return [VenueData(**item) for item in data]
                    except Exception:
                        # Invalid cache data, return None
                        return None

        return None

    async def set(
        self,
        service: str,
        params: dict,
        venues: List[VenueData],
        ttl: int = DEFAULT_TTL,
    ):
        """캐시에 데이터 저장

        Args:
            service: 서비스명
            params: 파라미터
            venues: VenueData 목록
            ttl: Time-to-live (초)
        """
        await self.initialize()

        key = self._make_key(service, params)
        now = time.time()
        expires_at = now + ttl

        # Convert VenueData objects to JSON
        value_json = json.dumps([venue.model_dump() for venue in venues])

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO cache (key, value, expires_at, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (key, value_json, expires_at, now),
            )
            await db.commit()

    async def invalidate(self, service: str, params: dict):
        """특정 캐시 무효화

        Args:
            service: 서비스명
            params: 파라미터
        """
        await self.initialize()

        key = self._make_key(service, params)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cache WHERE key = ?", (key,))
            await db.commit()

    async def invalidate_service(self, service: str):
        """특정 서비스의 모든 캐시 무효화

        Args:
            service: 서비스명
        """
        await self.initialize()

        pattern = f"seoul:{service}:%"

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cache WHERE key LIKE ?", (pattern,))
            await db.commit()

    async def clear_expired(self):
        """만료된 캐시 삭제"""
        await self.initialize()

        now = time.time()

        async with aiosqlite.connect(self.db_path) as db:
            result = await db.execute("DELETE FROM cache WHERE expires_at <= ?", (now,))
            deleted_count = result.rowcount
            await db.commit()

        return deleted_count

    async def clear_all(self):
        """모든 캐시 삭제"""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cache")
            await db.commit()

    async def get_stats(self) -> dict:
        """캐시 통계 조회

        Returns:
            {
                "total_entries": int,
                "expired_entries": int,
                "valid_entries": int,
                "size_bytes": int
            }
        """
        await self.initialize()

        now = time.time()

        async with aiosqlite.connect(self.db_path) as db:
            # Total entries
            async with db.execute("SELECT COUNT(*) FROM cache") as cursor:
                total = (await cursor.fetchone())[0]

            # Expired entries
            async with db.execute(
                "SELECT COUNT(*) FROM cache WHERE expires_at <= ?", (now,)
            ) as cursor:
                expired = (await cursor.fetchone())[0]

            # Database size
            db_path = Path(self.db_path)
            size_bytes = db_path.stat().st_size if db_path.exists() else 0

        return {
            "total_entries": total,
            "expired_entries": expired,
            "valid_entries": total - expired,
            "size_bytes": size_bytes,
        }


class CachedSeoulOpenAPIClient:
    """캐시 기능이 있는 Seoul Open API 클라이언트"""

    def __init__(self, client, cache_manager: Optional[CacheManager] = None):
        """
        Args:
            client: SeoulOpenAPIClient 인스턴스
            cache_manager: CacheManager 인스턴스 (None이면 새로 생성)
        """
        self.client = client
        self.cache = cache_manager or CacheManager()

    async def get_nature_attractions(
        self,
        start_index: int = 1,
        end_index: int = 100,
        language: str = "ko",
        use_cache: bool = True,
    ) -> List[VenueData]:
        """캐시를 활용한 자연 관광지 조회"""
        params = {
            "start_index": start_index,
            "end_index": end_index,
            "language": language,
        }

        if use_cache:
            cached = await self.cache.get("nature", params)
            if cached is not None:
                return cached

        # Cache miss or disabled - fetch from API
        try:
            venues = await self.client.get_nature_attractions(
                start_index, end_index, language
            )
            if use_cache and venues:
                await self.cache.set("nature", params, venues)
            return venues
        except Exception as e:
            # On error, invalidate cache
            if use_cache:
                await self.cache.invalidate("nature", params)
            raise

    async def get_restaurants(
        self,
        start_index: int = 1,
        end_index: int = 100,
        language: str = "ko",
        use_cache: bool = True,
    ) -> List[VenueData]:
        """캐시를 활용한 음식점 조회"""
        params = {
            "start_index": start_index,
            "end_index": end_index,
            "language": language,
        }

        if use_cache:
            cached = await self.cache.get("restaurants", params)
            if cached is not None:
                return cached

        # Cache miss or disabled - fetch from API
        try:
            venues = await self.client.get_restaurants(start_index, end_index, language)
            if use_cache and venues:
                await self.cache.set("restaurants", params, venues)
            return venues
        except Exception as e:
            # On error, invalidate cache
            if use_cache:
                await self.cache.invalidate("restaurants", params)
            raise

    async def get_attractions(
        self,
        start_index: int = 1,
        end_index: int = 100,
        language: str = "ko",
        use_cache: bool = True,
    ) -> List[VenueData]:
        """캐시를 활용한 관광명소 조회"""
        params = {
            "start_index": start_index,
            "end_index": end_index,
            "language": language,
        }

        if use_cache:
            cached = await self.cache.get("attractions", params)
            if cached is not None:
                return cached

        # Cache miss or disabled - fetch from API
        try:
            venues = await self.client.get_attractions(start_index, end_index, language)
            if use_cache and venues:
                await self.cache.set("attractions", params, venues)
            return venues
        except Exception as e:
            # On error, invalidate cache
            if use_cache:
                await self.cache.invalidate("attractions", params)
            raise
