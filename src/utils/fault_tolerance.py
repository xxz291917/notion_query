"""Fault tolerance utilities: retry, circuit breaker, rate limiter."""

import logging
import time
from enum import Enum
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(Exception):
    pass


class CircuitBreaker:
    """Prevents cascading failures by opening the circuit after consecutive failures."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is OPEN. Will retry after {self.recovery_timeout}s"
                )
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return False
        return (time.time() - self.last_failure_time) > self.recovery_timeout

    def _on_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker OPENED after {self.failure_count} failures")


class RetryPolicy:
    """Retry with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def retry(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        delay = self.base_delay * (2**attempt)
                        logger.warning(
                            f"Attempt {attempt + 1}/{self.max_retries + 1} failed: {e}. "
                            f"Retrying after {delay}s..."
                        )
                        time.sleep(delay)
            if last_exception:
                raise last_exception
            return None

        return wrapper


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, rate: float = 3.0):
        self.rate = rate
        self.tokens = rate
        self.last_update = time.time()

    def acquire(self) -> None:
        while True:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(self.rate, self.tokens + time_passed * self.rate)
            self.last_update = now
            if self.tokens >= 1:
                self.tokens -= 1
                return
            sleep_time = (1 - self.tokens) / self.rate
            time.sleep(sleep_time)
