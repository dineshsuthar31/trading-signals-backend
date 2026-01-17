from app.core.redis import get_redis_client

class RateLimiter:
    def __init__(self):
        try:
            self.r = get_redis_client()
            self.r.ping()
        except Exception:
            self.r = None

    def allow(self, key: str, limit: int = 5, window_seconds: int = 60) -> bool:
        """
        Returns True if allowed, False if rate limited.
        If Redis is not available, allow requests (dev mode).
        """
        if not self.r:
            return True

        count = self.r.incr(key)
        if count == 1:
            self.r.expire(key, window_seconds)

        return count <= limit
