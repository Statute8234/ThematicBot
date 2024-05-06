import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import time
from textblob import TextBlob 

def center_window():
    win = gw.getWindowsWithTitle('ThematicBot')[0]  # Get the window with the title
    win.center()

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("ThematicBot")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Initialize timing attributes
        self.last_time = time.time()
        self.time_intervals = []
        self.typo_count = 0

        # Create a text widget with a vertical scrollbar
        self.text_display = tk.Text(root, wrap=tk.WORD, height=10, width=50, bg="dark gray", fg="white")
        scroll_bar = tk.Scrollbar(root, command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scroll_bar.set)

        # Pack the scrollbar to the right of the text widget
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text_display.config(state=tk.DISABLED)

        # Text box for typing at the bottom
        self.text_entry = tk.Text(root, height=2, bg="light gray", fg="black")
        self.text_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_entry.bind("<Return>", self.handle_enter)
        self.text_entry.bind("<KeyPress>", self.on_key_press) 
        self.root.mainloop()

    def detect_speed_change(self):
        """Detect changes in typing speed."""
        if len(self.time_intervals) < 2:
            return "Not enough data to compare"

        # Compare last two intervals
        last_interval = self.time_intervals[-1]
        previous_interval = self.time_intervals[-2]

        if last_interval < previous_interval:
            return "Typing Accelerating"
        elif last_interval > previous_interval:
            return "Typing Decelerating"
        else:
            return "Typing Speed Constant"

    def on_key_press(self, event):
        """Handle key press event and calculate intervals between keystrokes."""
        current_time = time.time()
        interval = current_time - self.last_time
        self.last_time = current_time
        self.time_intervals.append(interval)

        # Increment typo count on backspace
        if event.keysym == 'BackSpace':
            self.typo_count += 1

        # Optionally print the interval or update any display
        if len(self.time_intervals) > 1:
            print(self.detect_speed_change())

    def handle_enter(self, event):
        """Handle pressing the Enter key in text_entry."""
        # Get the input text from text_entry
        input_text = self.text_entry.get("1.0", tk.END).strip()
        if input_text:
            sentiment = TextBlob(input_text).sentiment.polarity
            sentiment_desc = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
            response_length = "Short response" if len(input_text.split()) < 5 else "Long response"

            self.text_display.config(state=tk.NORMAL)
            self.text_display.insert(tk.END, f"User: {input_text} (Sentiment: {sentiment_desc}, {response_length}, Typos: {self.typo_count})\n")
            self.text_display.config(state=tk.DISABLED)
            self.text_display.see(tk.END)
            self.text_entry.delete("1.0", tk.END)
            self.typo_count = 0
        return 'break'

root = tk.Tk()
app = App(root)