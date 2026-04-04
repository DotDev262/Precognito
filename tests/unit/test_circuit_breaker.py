import pytest
import time
from precognito.utils import CircuitBreaker

def test_circuit_breaker_trip_and_reset():
    """Test the trip and reset logic of the CircuitBreaker."""
    # 1. Initialize with low threshold for testing
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
    
    @breaker
    def fail_func():
        raise ValueError("Intentional failure")

    @breaker
    def success_func():
        return "Success"

    # 2. First failure - should still be CLOSED
    with pytest.raises(ValueError):
        fail_func()
    assert breaker.state == "CLOSED"
    assert breaker.failure_count == 1

    # 3. Second failure - should TRIP to OPEN
    with pytest.raises(ValueError):
        fail_func()
    assert breaker.state == "OPEN"
    assert breaker.failure_count == 2

    # 4. Immediate call - should return None (skipping)
    result = success_func()
    assert result is None

    # 5. Wait for recovery timeout
    time.sleep(1.1)
    
    # 6. Call should enter HALF-OPEN and then CLOSED on success
    result = success_func()
    assert result == "Success"
    assert breaker.state == "CLOSED"
    assert breaker.failure_count == 0
