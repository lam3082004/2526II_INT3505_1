import logging
from functools import wraps
from pybreaker import CircuitBreaker
from flask import jsonify

logger = logging.getLogger(__name__)

# Global circuit breaker
circuit_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    listeners=[],
    name="api-circuit-breaker",
)


def with_circuit_breaker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return circuit_breaker.call(func, *args, **kwargs)
        except Exception as e:
            logger.error(f"Circuit breaker triggered: {str(e)}")
            return jsonify({"error": "Service temporarily unavailable"}), 503

    return wrapper
