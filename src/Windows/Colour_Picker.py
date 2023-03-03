import tkinter as tk
from tkinter import colorchooser, ttk


class ColorPickerApp(tk.Canvas):
    def __init__(self, master, identifier: str, default_colour='white', pick_callback=None, *args, **kwargs):
        super().__init__(master, width=30, height=20)
        self.master = master
        self.identifier = identifier
        self.color = default_colour
        self.pick_callback = pick_callback

        self.rect = self.create_rectangle(0, 0, 30, 20, fill=self.color)
        self.tag_bind(self.rect, '<Button-1>', self.open_color_picker)

    def open_color_picker(self, event):
        # Open a color picker dialog
        color = colorchooser.askcolor(title="Choose color", initialcolor=self.color)[1]
        if color is not None:
            # Update the color of the rectangle
            self.color = color
            self.itemconfig(self.rect, fill=self.color)
            if self.pick_callback is not None:
                self.pick_callback((self.identifier, color))


if __name__ == "__main__":
    # Create a tkinter window and run the app
    root = tk.Tk()
    app = ColorPickerApp(root)
    app.pack()
    root.mainloop()
