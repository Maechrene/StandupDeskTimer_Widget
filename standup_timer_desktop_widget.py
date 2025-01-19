"""Creates a standup desk timer"""
import tkinter as tk
import time
import threading
import pygame

# Initialize pygame mixer for sound control
pygame.mixer.init()



class Timer:
    """Timer"""

    def __init__(self):
        # GUI Setup
        self.root = tk.Tk()
        self.root.title("") # test removal
        self.root.geometry("150x240+3600+900") # (height x width + x + y) , bottom right of 2nd monitor

        # Grid configuration
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Initialize class variables
        self.timer_count = 0
        self.selected_hours = 1.0
        self.selected_time = tk.StringVar(value = "1")
        self.is_timer_running = False
        self.total_seconds = 0
        self.previous_x = 0
        self.previous_y = 0

        # Set label with white text and transparent background
        self.label = tk.Label(self.root, text="", font=("Helvetica", 1), fg="white")
        self.label.grid(row=0, column = 0, columnspan=3)

        self.countdown_label = tk.Label(self.root, text="0:00:00", font=("Helvetica", 24))
        self.countdown_label.grid(row=0, column=1, columnspan= 2, padx=0, pady=0, sticky = "nsew")


        # Button to start the timer
        start_button = tk.Button(
            self.root,
            text="Start",
            command= self.start_timer,
            fg='white',
            bg='black',
            highlightthickness=0
        )
        start_button.grid(row=1, column = 2, padx=10, pady=10)

        # Button to exit the application
        exit_button = tk.Button(
            self.root,
            text="x",
            command=self.root.destroy, fg='white', borderwidth=0, highlightthickness=0,
            bg = "black")
        exit_button.grid(row=0, column=0, padx=10, pady=10)  # Positioning at the top-left corner

        # Add icon to the window to make it appear in the taskbar
        # root.iconbitmap('desk-chair.ico')  # Replace it with your desired path

        # Set window attributes to show it in the taskbar (Windows-specific)
        # root.wm_attributes("-toolwindow", 0)  # This ensures the window is not a tool window

        # Make window transparent (Windows OS specific)
        self.root.wm_attributes('-transparentcolor', self.root['bg'])

        # Remove window decorations (title bar, etc.)
        self.root.overrideredirect(True) # Remove window decorations for custom draggable window

        # Move window to the top
        self.root.attributes('-topmost', True)

        # Dropdown to select the timer interval
        options = ["1", "1.5", "2", "3", "0.001"]  # String options
        self.selected_time = tk.StringVar()  # StringVar for OptionMenu
        self.selected_time.set(options[0])

        dropdown = tk.OptionMenu(self.root, self.selected_time, *options)
        dropdown.config( fg='white', highlightthickness=0, bg='black')
        dropdown.grid(row=1, column=1, padx=10, pady=10, sticky = "w")

        # Button to minimize the application, placed next to the exit button
        # minimize_button = tk.Button(
            # self.root,
            # text="_",
            # command=root.iconify,
            # fg='white',
            # font=("Helvetica", 10),
            # borderwidth=0,
            # highlightthickness=0,
            # bg = "black")
        # minimize_button.place(x=35, y=0, width=30, height=20)# Positioning next to the exit button

        # Bind right-click to print the position
        self.root.bind("<Button-3>", Timer.print_position)  # Right-click to print the position

        # Bind the drag functions to the root window
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # Force window to resize properly based on controls
        #root.update_idletasks()
        #root.minsize(root.winfo_width(), root.winfo_height())

    def start_timer(self):
        """Start the countdown timer in a separate thread"""
        self.selected_hours = float(self.selected_time.get())  # Convert string to float for timing

        if self.is_timer_running:
            return

        self.is_timer_running = True
        threading.Thread(target=self.countdown_timer, args=(self.selected_hours,)).start()
        self.countdown_label.config(fg="orange")

    def timer_done(self):
        """Handle timer completion"""

        self.timer_count += 1

        self.play_chime()

        if self.timer_count % 2 == 0:
            self.countdown_label.config(fg="orange") # Even times: change text color to orange
            threading.Thread(
                target=self.countdown_timer,
                args=(self.selected_hours,)
            ).start()
        else:
            self.countdown_label.config(fg="white")
            threading.Thread(
                target=self.countdown_timer,
                args=(1.0,)
            ).start()

        self.is_timer_running = False

    def stop_timer(self):
        """Stop the current timer"""
        self.is_timer_running = False

    def do_drag(self, event):
        """Function to move the widget as it's dragged"""
        x = self.root.winfo_x() + event.x - self.previous_x
        y = self.root.winfo_y() + event.y - self.previous_y
        self.root.geometry(f"+{x}+{y}")

    def print_position(self):
        """Print the current window position"""
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        print(f"Current window position: x={x}, y={y}")

    def start_drag(self, event):
        """Function to track the mouse click and start dragging"""
        self.previous_x = event.x
        self.previous_y = event.y

    def calculate_remaining_time(self):
        """Calculate hours, minutes, and seconds from total seconds."""
        if self.total_seconds < 0:
            raise ValueError("Total seconds cannot be negative")
        minutes, seconds = divmod(self.total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return hours, minutes, seconds

    def update_countdown_label(self, hours, minutes, seconds):
        """Update the countdown label with formatted time."""
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.countdown_label.config(text=formatted_time)


    def countdown_timer(self, hours):
        """Function to update the countdown timer."""
        self.total_seconds = int(hours * 60 * 60)  # Convert hours to seconds

        while self.total_seconds > 0:
            # Calculate remaining time
            hours_display, minutes, seconds = self.calculate_remaining_time()

            # Update the label with the formatted time
            self.update_countdown_label(hours_display, minutes, seconds)

            # Sleep for 1 second
            time.sleep(1)

            # Decrement the total seconds
            self.total_seconds -= 1

        # Call the timer_done function when countdown finishes
        self.timer_done()

    def play_chime(self, volume = 0.5): # Volume 0.0(silent) and 1.0 (max)
        """Function to play the .mp3 sound"""
        pygame.mixer.music.load('assets/wind-chime-g-003-89307.mp3')  # Replace with your .mp3 file
        pygame.mixer.music.set_volume(volume)  # Set the volume
        pygame.mixer.music.play()  # Play the .mp3 file

    def run(self):
        """Create an instance of the Timer"""
        self.root.mainloop()





# code to create an executable widget
# pyinstaller --onefile --windowed  StandupTimerDesktopWidget.py

if __name__  == "__main__":
    app = Timer()
    app.run()
