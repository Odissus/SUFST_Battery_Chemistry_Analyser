from src.Windows.Window import Window
from src.File_Parser import FileParser
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from typing import Iterable
import pandas as pd


class FileParsingOptionsWinow(Window):
    def __init__(self, master, parent):
        super().__init__(master, title="Parse Raw Data", geometry="500x200", parent=parent)
        frame, self.path_to_file = self.text_entry_with_label_and_button(label_text="Path to file", entry_length=50, button_icon="📁", button_command=None)
        frame.grid(row=0, column=0)
        frame, self.apply_fixes = self.tick_box_with_label(label_text="Apply fixes")
        frame.grid(row=1, column=0)
        ok_button = ttk.Button(self.master, text="OK", command=self.parse)
        cancel_button = ttk.Button(self.master, text="Cancel", command=self.destroy)
        ok_button.grid(row=2, column=0)
        cancel_button.grid(row=3, column=0)

    def destroy(self):
        self.unlock_parent_and_destroy()

    def parse(self):
        path_to_file = self.path_to_file.get()
        apply_fixes = bool(self.apply_fixes.get())
        fp = FileParser(path_to_file)
        fp.parse(apply_fixes=apply_fixes, fix_time=apply_fixes)
        new_filename = fd.asksaveasfilename(confirmoverwrite=True)
        fp.save_as(new_filename)
        messagebox.showinfo("Success!", "File parsed successfully and saved!")
        self.destroy()

