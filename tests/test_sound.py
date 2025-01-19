"""Testing sounds"""

from unittest.mock import patch
from standup_timer_desktop_widget import play_chime

@patch("pygame.mixer.music")
def test_play_chime(mock_music):
    """Test using mock music"""
    play_chime(volume=0.7)
    mock_music.load.assert_called_once()
    mock_music.set_volume.assert_called_once_with(0.7)
    mock_music.play.assert_called_once()
