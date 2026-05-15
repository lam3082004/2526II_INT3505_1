import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_rate_limiter():
    enabled = os.getenv("RATE_LIMIT_ENABLED", "1") == "1"
    
    if not enabled:
        return None

    rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{rate_limit_per_minute}/minute"],
        storage_uri="memory://",
    )
    return limiter
