from src.Windows.Window import Window
from tkinter import *
from PIL import Image, ImageTk


class InitialWindow(Window):
    def __init__(self, master: Tcl):
        super().__init__(master, title="Loading", geometry="500x500")
        #master.overrideredirect(True)
        #image = PhotoImage(file="Stag.jpg")
        # create a label to display the image
        #label = Label(self.master, image=image)
        #label.pack()

        my_img = ImageTk.PhotoImage(Image.open("Stag.jpg"))
        b1 = Button(self.master, image=my_img)
        b1.grid(row=1, column=1)
