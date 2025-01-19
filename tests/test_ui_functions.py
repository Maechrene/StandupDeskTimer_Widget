from unittest.mock import MagicMock
from unittest.mock import Mock
import tkinter as tk
from standup_timer_desktop_widget import update_countdown_label, start_timer, stop_timer, countdown_timer, timer_done, start_drag
 
def test_update_countdown_label():
    mock_label = MagicMock()
    update_countdown_label(mock_label, 1, 2, 3)
    mock_label.config.assert_called_once_with(text="01:02:03")

def test_start_button(mocker):
    mock_countdown = mocker.patch("standup_timer_desktop_widget.countdown_timer")
    is_timer_running = False

    # Simulate starting the timer
    mock_countdown.return_value = None
    assert not is_timer_running
    start_timer("1", Mock())  # Call the function
    mock_countdown.assert_called_once()

# def test_stop_button():
#    global is_timer_running
#    is_timer_running = True
#    stop_timer()
#    assert not is_timer_running

def test_countdown_timer(mocker):
    mock_countdown_label = mocker.Mock()

    # Simulate a countdown of 1 hour
    countdown_timer(1, mock_countdown_label)
    mock_countdown_label.config.assert_called_with(text="01:00:00")

# def test_dropdown_menu():
#     options = ["1", "1.5", "2", "3", "0.001"]
#     selected_time = tk.StringVar()
#     selected_time.set(options[0])
#     assert selected_time.get() == "1"

# def test_visual_feedback(mocker):
#     mock_countdown_label = mocker.Mock()
#     timer_done(mock_countdown_label)
#     mock_countdown_label.config.assert_called_with(fg="orange")

def test_window_dragging(mocker):
    mock_event = mocker.Mock()
    mock_event.x, mock_event.y = 10, 20

    root = tk.Tk()
    root.geometry("150x240+100+100")
    start_drag(mock_event)
    launch_widget(mock_event) 
    assert root.geometry() == "+110+120"
