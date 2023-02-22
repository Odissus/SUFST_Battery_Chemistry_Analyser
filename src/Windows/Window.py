from tkinter import *
from tkinter import ttk
from src.Windows import *


class Window:
    def __init__(self, master: Tcl, title="", geometry="1000x1000", parent=None):
        """
        Window superclass  - implements all attributes and methods used by various windows.

        :param master: Tkinter interpreter object (root or TopLevel)
        :param title: Top left text, title of the window
        :param geometry: outlines window size in pixels eg 1000x1000
        :param parent: parent window, necessary when going back from this window to open the parent
        """
        self.master = parent
        self.master = master
        self.master.title(title)
        self.master.geometry(geometry)
        self.background_colour = "gray55"
        self.foreground_colour = "black"
        self.big_label_height = "2"
        self.small_label_height = "1"

    def text_entry_with_label(self, frame=None, label_text="", entry_length=10):
        """frame, entry_variable"""
        if frame is None:
            frame = ttk.Frame(self.master)
        label = self.small_Label(label_text, master=frame)
        label.grid(row=0, column=0)
        entry_variable = StringVar(frame)
        entry = ttk.Entry(frame, textvariable=entry_variable, width=entry_length)
        entry.grid(row=0, column=1)
        return frame, entry_variable

    def tick_box_with_label(self, frame=None, label_text=""):
        """frame, entry_variable"""
        if frame is None:
            frame = ttk.Frame(self.master)
        label = self.small_Label(label_text, master=frame)
        label.grid(row=0, column=0)
        tick_variable = IntVar(value=1)
        tick_box = ttk.Checkbutton(frame, variable=tick_variable)
        tick_box.grid(row=0, column=1)
        return frame, tick_variable

    def text_entry_with_label_and_button(self, frame=None, label_text="", entry_length=None, button_icon=None, button_command=None):
        """frame, entry_variable"""
        frame, entry_variable = self.text_entry_with_label(frame=frame, label_text=label_text, entry_length=entry_length)
        if isinstance(button_icon, str):
            b = ttk.Button(frame, command=button_command, text=button_icon, width=len(button_icon)+3)
        else:
            b = ttk.Button(frame, command=button_command)
        b.grid(row=0, column=2)
        return frame, entry_variable


    def destroy(self):
        """
        Destroys the window

        :return:
        """
        self.master.destroy()

    def normal_button(self, text, command=None):
        """
        Stylised standard button object with custom text

        :param text: Text to appear in the button
        :param command: Optional command that button invokes upon being pressed
        :return: Tkinter stylised button object
        """
        return Button(self.master, text=text, bg=self.background_colour, fg=self.foreground_colour, width="8",
                      height="1", command=command,
                      font=("Ariel", 13))

    def big_Label(self, text: str):
        """
        Sylised heading label with custom text

        :param text: Text to appear in the label
        :return: Tkinter stylised label object
        """
        return Label(self.master, text=text, bg=self.background_colour, fg=self.foreground_colour, width="300",
                     height=self.big_label_height,
                     font=("Ariel", 14, "bold"))

    def small_Label(self, text: str, master=None):
        """
        Sylised body text label with custom text

        :param text: Text to appear in the label
        :return: Tkinter stylised label object
        """
        return Label(self.master if master is None else master, text=text, height=self.small_label_height)

    def show_window_and_hide(self, window_name):
        """
        Procedure used to hide this window and make a new window that when closed will show this window again.

        :param window_name: name of the class used to create the new window object
        :return: Returns the window object if needed
        """
        self.master.withdraw()
        win = Toplevel()
        window_obj = window_name(win, self)
        return window_obj

    def create_top_level_and_lock(self, window_name):
        #self.master.grab_set()
        win = Toplevel()
        win.grab_set()
        window_obj = window_name(win, self)
        return window_obj

    def unlock(self):
        """
        A more programmer friendly name for self.master.deiconify; shows the window if it's in the hidden state.
        """
        self.master.deiconify()

    def unlock_parent_and_destroy(self):
        """
        Unlocks the parent window if such exists and destroys this window
        """
        if self.master is not None:
            self.master.unlock()
        self.master.destroy()


# Demo
if __name__ == "__main__":
    root = Tk()
    Window(root)
    root.mainloop()
