from datetime import datetime, timedelta, timezone


def generate_expiration(ttl_minutes: int) -> datetime:
    """Generate expiration datetime based on TTL in minutes."""

    return datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)


def generate_date_now() -> datetime:
    """Get the current datetime in UTC."""
    return datetime.now(timezone.utc)
