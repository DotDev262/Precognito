import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Simple circuit breaker implementation to prevent cascading failures."""
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF-OPEN"
                    logger.info(f"Circuit breaker for {func.__name__} entering HALF-OPEN state.")
                else:
                    logger.warning(f"Circuit breaker for {func.__name__} is OPEN. Skipping call.")
                    return None

            try:
                result = func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    logger.info(f"Circuit breaker for {func.__name__} RESET to CLOSED.")
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                logger.error(f"Circuit breaker for {func.__name__} failure count: {self.failure_count}. Error: {e}")
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.error(f"Circuit breaker for {func.__name__} TRIPPED to OPEN.")
                
                raise e
        return wrapper

# Global instances for InfluxDB
influx_read_breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=60)
influx_write_breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=60)
