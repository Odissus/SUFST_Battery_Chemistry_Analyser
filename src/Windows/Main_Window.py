from src.Windows.Window import Window
from src.Windows.File_Parsing_Options_Winow import FileParsingOptionsWinow
from src.Windows.Graph_Frame import GraphCanvas
from src.File_Parser import FileParser
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from typing import List
import pandas as pd


class MainWindow(Window):
    __data = None
    __constants = None

    def __init__(self, master: Tcl, data=None, constants=None):
        super().__init__(master, title="SUFST Battery Analyser", geometry="1920x1080")
        headings = list(data.columns)
        GraphCanvas.update_axis_options(headings)
        if data is not None:
            MainWindow.__data = data
            GraphCanvas.update_data(data)

        if constants is not None:
            MainWindow.__constants = constants

        self.top_frame = Frame(self.master)
        self.top_frame.grid(row=0, column=0)

        # Create a frame for the bottom row of columns
        self.bottom_frame = Frame(self.master)
        self.bottom_frame.grid(row=1, column=0)

        # create a 3x3 grid
        left_frame = Frame(self.top_frame, borderwidth=2, relief="ridge")
        left_frame.grid(row=0, column=0)

        text_label = Label(left_frame, text="hello")
        text_label.pack()

        middle_frame = Frame(self.top_frame, borderwidth=2, relief="ridge")
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

        right_frame = Frame(self.top_frame, borderwidth=2, relief="ridge")
        right_frame.grid(row=0, column=2)

        text_label = Label(right_frame, text="hello")
        text_label.pack()

        # create a menubar
        menubar_options = {"File": ["New", "Open", "Save", "Save As"],
                           "Tools": ["Parse a raw data file"]}
        menubar_functions = {"File": [None, None, None, None],
                             "Tools": [self.parse_raw_data_file]}
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        for menu_option in menubar_options.keys():
            menu_option_widget = Menu(menubar, tearoff=False)
            for item, function in zip(menubar_options[menu_option], menubar_functions[menu_option]):
                menu_option_widget.add_command(label=item, command=function)
            menubar.add_cascade(label=menu_option, menu=menu_option_widget)

        # c1=GraphCanvas(master=self.master)
        # c1.get_tk_widget().grid(row=1, sticky="nsew")
        # self.master.bind('<Configure>', c1.on_resize)

        # Create a button to add columns to the second row
        self.add_column_button = Button(self.top_frame, text="Add Column", command=self.add_graph)
        self.add_column_button.grid(row=1, column=0, padx=10, pady=10)

        # Create a button to remove columns from the second row
        self.remove_column_button = Button(self.top_frame, text="Remove Column", command=self.remove_graph)
        self.remove_column_button.grid(row=1, column=1, padx=10, pady=10)

        self.graph_canvases = []

        for i in range(3):
            self.top_frame.columnconfigure(i, weight=1)

    def add_graph(self):
        # Create a new label with the current number of columns
        column_number = len(self.graph_canvases) + 1
        graph_canvas = GraphCanvas(master=self.bottom_frame)
        graph_canvas.grid(row=0, column=column_number - 1, sticky="nsew", padx=10, pady=10)
        # self.master.bind('<Configure>', graph_canvas.on_resize)
        # label = Label(self.bottom_frame, text="Column {}".format(column_number))
        # label.grid(row=0, column=column_number - 1, padx=10, pady=10)

        # Add the label to the list of labels
        self.graph_canvases.append(graph_canvas)

        # Set the column weight for the new column
        self.bottom_frame.columnconfigure(column_number, weight=1)

    def remove_graph(self):
        if len(self.graph_canvases) > 0:
            # Remove the last label from the list of labels
            graph_canvas = self.graph_canvases.pop()

            # Remove the label from the grid
            graph_canvas.grid_forget()

            # Set the column weight for the last column to 0
            self.bottom_frame.columnconfigure(len(self.graph_canvases) + 1, weight=0)

    def update_table_headings(self, headings):
        raise NotImplementedError("Changing headings at runtime is not implemented")

    def populate_table(self, df: pd.DataFrame):
        return
        for i, row in df.iterrows():
            self.tv.insert('', i, text=str(i), values=list(row))
            if i > 100:
                return

    def parse_raw_data_file(self):
        tl = self.create_top_level_and_lock(FileParsingOptionsWinow)
        # fp = FileParser()
