from datetime import datetime, timezone
from pydantic import SerializerFunctionWrapHandler

def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)

def to_utc(
    utc_or_native: datetime,
    nxt: SerializerFunctionWrapHandler
) -> str:
    utc_datetime = utc_or_native.replace(
        tzinfo=timezone.utc)
    return nxt(utc_datetime)