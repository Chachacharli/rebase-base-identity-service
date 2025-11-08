from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
from app.utils.dates import generate_date_now

from app.models.app_settings import AppSetting


@dataclass
class CacheEntry:
    """Entry of cache in memory."""

    value: Optional[str]
    time: datetime


class AppSettingRepository:
    _cache: dict[str, CacheEntry] = {}
    _cache_ttl_seconds: int = 60

    def __init__(self, session: Session):
        self.session = session

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get the value of a configuration by its key."""
        cached = self._cache.get(key)
        if (
            cached
            and (generate_date_now() - cached.time).total_seconds()
            < self._cache_ttl_seconds
        ):
            return cached.value

        stmt = select(AppSetting).where(AppSetting.key == key)
        setting = self.session.exec(stmt).first()

        if not setting:
            return default

        value = setting.value
        # store in cache
        self._cache[key] = CacheEntry(value=value, time=generate_date_now())
        return value

    def set(
        self, key: str, value: str, is_active: bool, description: Optional[str] = None
    ) -> AppSetting:
        """Create or update an existing configuration."""
        stmt = select(AppSetting).where(AppSetting.key == key)
        setting = self.session.exec(stmt).first()

        if not setting:
            setting = AppSetting(
                key=key, value=value, description=description, is_active=is_active
            )
        else:
            setting.value = value
            setting.description = description or setting.description
            setting.updated_at = generate_date_now()

        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)

        # invalidate cache
        self._cache.pop(key, None)
        return setting

    def get_all(self) -> list[AppSetting]:
        """Get all available configurations."""
        return list(self.session.exec(select(AppSetting)).all())

    def delete(self, key: str) -> bool:
        """Delete a configuration (soft delete optional)."""
        stmt = select(AppSetting).where(AppSetting.key == key)
        setting = self.session.exec(stmt).first()
        if not setting:
            return False

        setting.is_active = False
        self.session.add(setting)
        self.session.commit()
        self._cache.pop(key, None)
        return True
