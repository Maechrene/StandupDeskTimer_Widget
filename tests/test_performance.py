"""Testing performance"""
from unittest.mock import Mock
from standup_timer_desktop_widget import update_countdown_label


def test_smooth_updates(mocker):
    """Test smooth updates"""
    mock_countdown_label = mocker.Mock()

    # Call the function with test inputs
    update_countdown_label(mock_countdown_label, 0, 0, 1)

    # Assert that the label's config method was called with the correct text
    mock_countdown_label.config.assert_called_with(text="00:00:01")
