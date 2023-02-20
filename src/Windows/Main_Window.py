from src.Windows.Window import Window
from src.File_Parser import FileParser
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Iterable
import pandas as pd


class MainWindow(Window):
    def __init__(self, master: Tcl, headings: Iterable[str]):
        super().__init__(master, title="SUFST Battery Analyser", geometry="1920x1080")
        # create a 3x3 grid
        left_frame = Frame(self.master, borderwidth=2, relief="ridge")
        left_frame.grid(row=0, column=0)

        text_label = Label(left_frame, text="hello")
        text_label.pack()

        middle_frame = Frame(self.master, borderwidth=2, relief="ridge")
        middle_frame.grid(row=0, column=1)

        # headings = ['Product ID', 'Product Name', 'Product Price', 'Product Stock', 'Product Type']

        # Treeview is tkinter implementation of a table
        self.tv = ttk.Treeview(middle_frame)
        self.tv['columns'] = tuple(headings)

        self.tv.column('#0', width=0, stretch=NO)
        self.tv.heading('#0', text='', anchor=CENTER)

        # Add every heading
        for heading in headings:
            self.tv.heading(heading, text=heading, anchor=CENTER)
            self.tv.column(heading, anchor=CENTER, width=100)

        self.tv.pack(side='left')
        verscrlbar = ttk.Scrollbar(middle_frame,
                                   orient="vertical",
                                   command=self.tv.yview)
        self.tv.configure(xscrollcommand=verscrlbar.set)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side='right', fill='x')

        right_frame = Frame(self.master, borderwidth=2, relief="ridge")
        right_frame.grid(row=0, column=2)

        text_label = Label(right_frame, text="hello")
        text_label.pack()

        # create a menubar
        menubar_options = {"File": ["New", "Open", "Save", "Save As"],
                           "Tools": ["Parse a raw data file"]}
        menubar_functions = {"File": [None, None, None, None],
                             "Tools": [None]}
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for menu_option in menubar_options.keys():
            menu_option_widget = Menu(menubar, tearoff=False)
            for item, function in zip(menubar_options[menu_option], menubar_functions[menu_option]):
                menu_option_widget.add_command(label=item, command=function)
            menubar.add_cascade(label=menu_option, menu=menu_option_widget)

    def update_table_headings(self, headings):
        raise NotImplementedError("Changing headings at runtime is not implemented")

    def populate_table(self, df: pd.DataFrame):
        for i, row in df.iterrows():
            self.tv.insert('', i, text=str(i), values=list(row))
            if i > 100:
                return

    def parse_raw_data_file(self):
        fp = FileParser()
