import pytest
from standup_timer_desktop_widget import calculate_remaining_time

def test_calculate_remaining_time():
    # Basic test
    assert calculate_remaining_time(3661) == (1, 1, 1)  # 1 hour, 1 minute, 1 second
    
    # Test zero seconds
    assert calculate_remaining_time(0) == (0, 0, 0)
    
    # Test large input
    assert calculate_remaining_time(3600 * 24) == (24, 0, 0)  # 24 hours
    
    # Test edge case
    with pytest.raises(ValueError):
        calculate_remaining_time(-1)  # Negative input should raise an error