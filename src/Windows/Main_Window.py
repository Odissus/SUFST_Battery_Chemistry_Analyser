from src.Windows.Window import Window
from src.Windows.File_Parsing_Options_Winow import FileParsingOptionsWinow
from src.Windows.Graph_Frame import GraphCanvas
from src.Windows.Colour_Picker import ColorPickerApp
from src.File_Parser import FileParser
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from typing import List, Tuple, Any, Union, Dict
import pandas as pd


class MainWindow(Window):
    __data = None
    __constants = None

    class LeftFrame(Frame):
        def __init__(self, master, constants: Union[None, Dict[str, Any]] = None, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.master = master
            self.constants_boxes = []
            if constants is not None:
                self.apply_constants(constants)

        def apply_constants(self, constants: Dict[str, Any]):
            text = ttk.Label(self, text="Constants")
            text.grid(column=0, row=0, columnspan=2)
            for (i, constant) in enumerate(constants):
                text = ttk.Label(self, text=constant)
                text.grid(column=0, row=i + 1)
                value_var = StringVar()
                value_var.set(constants[constant])
                value = ttk.Entry(self, textvariable=value_var, width=10, state="readonly")
                value.grid(column=1, row=i + 1)
                self.constants_boxes.append((text, value, value_var))

    class RightFrame(Frame):
        mode_words = {"R": ("Recharge", "yellow"),
                        "C": ("Charge", "green"),
                        "D": ("Discharge", "orange"),
                        "O": ("O", "grey"),
                        "S": ("S", "grey")}

        def __init__(self, master, modes=None, callback=None, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.modes = modes
            self.callback = callback
            self.widget_containers = []
            if modes is not None:
                self._populate_modes()

        def _populate_modes(self):
            for (i, mode) in enumerate(self.modes.keys()):
                mode_colour = ColorPickerApp(self, mode, pick_callback=self.callback)
                text_to_show = mode
                if mode in MainWindow.RightFrame.mode_words.keys():
                    text_to_show = MainWindow.RightFrame.mode_words[mode][0]
                    mode_colour = ColorPickerApp(self, mode, default_colour=MainWindow.RightFrame.mode_words[mode][1], pick_callback=self.callback)
                label = ttk.Label(self, text=text_to_show)
                mode_colour.grid(row=i, column=0)
                label.grid(row=i, column=1)
                self.widget_containers.append((mode_colour, label))

    def __init__(self, master: Tcl, data=None, constants=None, modes=None, *args, **kwargs):
        super().__init__(master, title="SUFST Battery Analyser", geometry="1920x1080", *args, **kwargs)
        self.table_colour_scheme = {}
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
        left_frame = MainWindow.LeftFrame(self.top_frame, constants=MainWindow.__constants)
        left_frame.grid(row=0, column=0)

        middle_frame = Frame(self.top_frame)
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
        self.tv.configure(yscrollcommand=verscrlbar.set)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side='right', fill='y')

        right_frame = self.RightFrame(self.top_frame, modes=modes, callback=self.recolour_table)
        right_frame.grid(row=0, column=2)

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

        # Create a button to add columns to the second row
        self.add_column_button = ttk.Button(self.bottom_frame, text="Add graph", command=self.add_graph)
        self.add_column_button.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.columnconfigure(0, weight=1)

        # Create a button to remove columns from the second row
        # self.remove_column_button = Button(self.top_frame, text="Remove Column", command=self.remove_graph)
        # self.remove_column_button.grid(row=1, column=1, padx=10, pady=10)

        self.graph_canvases = []

        for i in range(3):
            self.top_frame.columnconfigure(i, weight=1)

    def regrid_graphs(self, index_to_remove: int = None):
        if index_to_remove is not None:
            del self.graph_canvases[index_to_remove]
        for (index, command) in zip(range(len(self.graph_canvases)), self.graph_canvases):
            self.bottom_frame.columnconfigure(index, weight=2)
            self.graph_canvases[index].grid(row=0, column=index)
        self.add_column_button.grid(row=0, column=len(self.graph_canvases), sticky="nsew")
        self.bottom_frame.columnconfigure(len(self.graph_canvases), weight=1)

    def add_graph(self):
        # Create a new label with the current number of columns
        column_number = len(self.graph_canvases) + 1
        graph_canvas = GraphCanvas(master=self.bottom_frame, regrid_command=self.regrid_graphs, index=column_number - 1)
        graph_canvas.grid(row=0, column=column_number - 1, sticky="n", padx=10, pady=10)
        # self.master.bind('<Configure>', graph_canvas.on_resize)
        # label = Label(self.bottom_frame, text="Column {}".format(column_number))
        # label.grid(row=0, column=column_number - 1, padx=10, pady=10)

        # Add the label to the list of labels
        self.graph_canvases.append(graph_canvas)
        self.add_column_button.grid(row=0, column=column_number, sticky="nsew")

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
        for mode in self.RightFrame.mode_words.keys():
            self.tv.tag_configure(mode, background=self.RightFrame.mode_words[mode][1])
        for i, row in self.__data.iterrows():
            self.tv.insert('', int(i), text=str(i), values=list(row), tags=(row["MD"],))
            if i > 100:
                return

    def recolour_table(self, new_colour_name_and_colour):
        self.tv.tag_configure(new_colour_name_and_colour[0], background=new_colour_name_and_colour[1])
        indexes = self.__data.index[self.__data["MD"] == new_colour_name_and_colour[0]]
        #for i in indexes:
        #    if i < 100:
        #        self.tv.item(i, tags=(new_colour_name_and_colour[0],))
        #    else:
        #        return

    def parse_raw_data_file(self):
        tl = self.create_top_level_and_lock(FileParsingOptionsWinow)
        # fp = FileParser()
