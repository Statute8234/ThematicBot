import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import time
from textblob import TextBlob 
import neural_network_classifier

def center_window():
    win = gw.getWindowsWithTitle('ThematicBot')[0]  # Get the window with the title
    win.center()

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("ThematicBot")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        default_font = ('Georgia', 11)
        # Create a text widget with a vertical scrollbar
        self.text_display = tk.Text(root, wrap=tk.WORD, height=10, width=50, bg="dim gray", fg="white", font=default_font)
        scroll_bar = tk.Scrollbar(root, command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scroll_bar.set)
        
        # Pack the scrollbar to the right of the text widget
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.text_display.config(state=tk.DISABLED)
        # Proper call to configReturn method with initial message
        self.configReturn("Hello")
        # Text box for typing at the bottom
        self.text_entry = tk.Text(root, height=2, bg="light gray", fg="black", font=default_font)
        self.text_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_entry.bind("<Return>", self.handle_enter)
        self.root.mainloop()

    def configReturn(self, Userinput):
        """This function should enable the text widget, display the response, and disable it again."""
        self.text_display.config(state=tk.NORMAL)  # Enable text widget for modification
        anylisis = neural_network_classifier.predict_response(Userinput)
        self.text_display.insert(tk.END, "Bot: " + anylisis.capitalize() + '\n')  # Simulate a response
        self.text_display.config(state=tk.DISABLED)  # Disable it back
        self.text_display.see(tk.END)  # Auto-scroll to the end of tex

    def handle_enter(self, event):
        """Handle pressing the Enter key in text_entry."""
        # Get the input text from text_entry
        input_text = self.text_entry.get("1.0", tk.END).strip()
        if input_text:
            self.text_display.config(state=tk.NORMAL)
            self.text_display.insert(tk.END, f"User: {input_text} \n")
            self.text_display.config(state=tk.DISABLED)
            self.text_display.see(tk.END)
            self.text_entry.delete("1.0", tk.END)
            self.typo_count = 0
            self.configReturn(input_text)
        return 'break'

root = tk.Tk()
app = App(root)
