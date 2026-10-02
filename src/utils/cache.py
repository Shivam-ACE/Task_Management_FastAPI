import json
import redis
from src.utils.settings import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        if not settings.REDIS_URL:
            return None
        _client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
        )
    return _client


def cache_get(key: str):
    r = _get_client()
    if not r:
        return None
    try:
        raw = r.get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None  # redis down -> app falls back to postgres


def cache_set(key: str, value, ttl: int = 60):
    r = _get_client()
    if not r:
        return
    try:
        r.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass


def cache_delete(key: str):
    r = _get_client()
    if not r:
        return
    try:
        r.delete(key)
    except Exception:
        pass