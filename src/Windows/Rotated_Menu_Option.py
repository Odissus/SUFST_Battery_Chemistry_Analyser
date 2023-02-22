import tkinter as tk
from PIL import Image, ImageTk

class RotatedOptionMenu(tk.Frame):
    def __init__(self, parent, options, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.options = options

        # Create a dropdown menu with the given options
        self.var = tk.StringVar(self.parent)
        self.var.set(self.options[0])
        self.menu = tk.OptionMenu(self, self.var, *self.options)
        self.menu.config(width=8)
        self.menu.grid(row=0, column=0, sticky="nsew")

        # Rotate the canvas 90 degrees
        self.canvas = tk.Canvas(self, width=30, height=100)
        self.canvas.grid(row=0, column=1)
        self.rotate = Image.new('RGBA', (30, 100), (255, 255, 255, 0))
        self.rotate_draw = ImageDraw.Draw(self.rotate)
        self.rotate_draw.text((15,50), self.var.get(), font=("Helvetica", 12), fill="black", anchor="center")
        self.image = ImageTk.PhotoImage(self.rotate.rotate(90))
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        # Bind the dropdown menu to update the label when an option is selected
        self.var.trace("w", self.update_label)

    def update_label(self, *args):
        self.rotate_draw.rectangle((0, 0, 30, 100), fill=(255, 255, 255, 0))
        self.rotate_draw.text((15,50), self.var.get(), font=("Helvetica", 12), fill="black", anchor="center")
        self.image = ImageTk.PhotoImage(self.rotate.rotate(90))
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

# Create a tkinter window and set its size
root = tk.Tk()
root.geometry("300x300")

# Create a rotated dropdown menu
options = ["Option 1", "Option 2", "Option 3"]
rotated_menu = RotatedOptionMenu(root, options)
rotated_menu.grid(row=0, column=0)

# Run the tkinter event loop
root.mainloop()
