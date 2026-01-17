import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.routes.auth import get_current_user
from app.core.redis import get_redis_client
from app.services.signals_service import generate_mock_signals

router = APIRouter(prefix="/signals", tags=["Signals"])

CACHE_KEY = "signals:latest"
CACHE_TTL_SECONDS = 300


def safe_get_redis():
    try:
        r = get_redis_client()
        r.ping()
        return r
    except Exception:
        return None


@router.get("")
def get_signals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = safe_get_redis()

    # Try cache
    signals = None
    if r:
        try:
            cached = r.get(CACHE_KEY)
            if cached:
                signals = json.loads(cached)
        except Exception:
            signals = None

    # If no cache -> generate
    if not signals:
        signals = generate_mock_signals()
        if r:
            try:
                r.setex(CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(signals))
            except Exception:
                pass

    if current_user.is_paid:
        final_signals = signals
    else:
        final_signals = signals[:3]

    return {
        "paid": current_user.is_paid,
        "count": len(final_signals),
        "signals": final_signals,
    }
