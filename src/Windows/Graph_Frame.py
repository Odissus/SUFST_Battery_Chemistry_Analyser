import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, Any, Iterable, List
import numpy as np


class GraphCanvas(tk.Frame):
    __graph_commands = ["", "Differentiate", "Integrate", "Curve fit"]
    __possible_axes: List[str] = []
    __instances: List['GraphCanvas'] = []
    __data: Any = None

    class _GraphCanvas(FigureCanvasTkAgg):
        def __init__(self, master):
            self.master = master

            # Create a new matplotlib figure
            self.fig = Figure(figsize=(5, 4), dpi=100)
            # self.fig.subplots_adjust(left=0.1, bottom=0.1, right=1, top=1)

            # Add a subplot to the figure
            self.ax = self.fig.add_subplot(111)
            # self.ax.set_title("Sample Plot")
            # self.ax.set_xlabel("")
            # self.ax.set_ylabel("")
            self.ax.plot([1, 2, 3, 4], [10, 5, 8, 3])
            super().__init__(self.fig, master=self.master)
            self.draw()

        def on_resize(self, event):
            w, h = event.width, event.height
            self.fig.set_size_inches(w / 100, h / 100)

    def validate_limit(self, new_value):
        # If the new value is empty, allow it
        if new_value == '' or new_value == '-':
            return True
        # Try to convert the new value to a float
        try:
            value = float(new_value)
        except ValueError:
            #self.errors.update({""})
            return False
        # If the new value is not between 3 and 5, disallow it
        #if value < 3 or value > 5:
        #    return False
        # Allow the new value
        return True

    def __init__(self, master, *args, **kwargs):
        #self.master = master
        GraphCanvas.__instances.append(self)
        super().__init__(master=master, *args, **kwargs)
        validate = master.register(self.validate_limit)
        self.errors = {}
        self.current_axis_limits = []

        self.graph_canvas = GraphCanvas._GraphCanvas(self)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, columnspan=6)

        y_axis_label = ttk.Label(self, text="Y_axis: ")
        y_axis_label.grid(row=1, column=0, sticky="e")
        self.y_axis = tk.StringVar(self)
        self.y_axis.set(GraphCanvas.__possible_axes[0])
        self.y_axis_dropdown = ttk.Combobox(self, values=GraphCanvas.__possible_axes, textvariable=self.y_axis,
                                            state="readonly")
        self.y_axis_dropdown.grid(row=1, column=1, sticky="w")
        self.y_axis_dropdown.bind('<<ComboboxSelected>>', self._update_graph)
        y_axis_domain_label = ttk.Label(self, text="Range: ")
        y_axis_domain_label.grid(row=1, column=2, sticky="e")
        self.min_y_axis = tk.StringVar(self)
        self.min_y_axis.set("")
        y_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_y_axis, width=7, validate='key', validatecommand=(validate, '%P'))
        y_axis_min_value_entry.grid(row=1, column=3)
        y_axis_min_value_entry.bind('<KeyRelease>', self._update_graph)
        y_axis_label = ttk.Label(self, text=" to ")
        y_axis_label.grid(row=1, column=4)
        self.max_y_axis = tk.StringVar(self)
        self.max_y_axis.set("")
        y_axis_max_value_entry = ttk.Entry(self, textvariable=self.max_y_axis, width=7, validate='key', validatecommand=(validate, '%P'))
        y_axis_max_value_entry.grid(row=1, column=5)
        y_axis_max_value_entry.bind('<KeyRelease>', self._update_graph)

        x_axis_label = ttk.Label(self, text="X_axis: ")
        x_axis_label.grid(row=2, column=0, sticky="e")
        self.x_axis = tk.StringVar(self)
        self.x_axis.set(GraphCanvas.__possible_axes[0])
        self.x_axis_dropdown = ttk.Combobox(self, values=GraphCanvas.__possible_axes, textvariable=self.x_axis,
                                            state="readonly")
        self.x_axis_dropdown.grid(row=2, column=1, sticky="w")
        self.x_axis_dropdown.bind('<<ComboboxSelected>>', self._update_graph)
        x_axis_domain_label = ttk.Label(self, text="Domain: ")
        x_axis_domain_label.grid(row=2, column=2, sticky="e")
        self.min_x_axis = tk.StringVar(self)
        self.min_x_axis.set("")
        x_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_x_axis, width=7, validate='key', validatecommand=(validate, '%P'))
        x_axis_min_value_entry.grid(row=2, column=3)
        x_axis_min_value_entry.bind('<KeyRelease>', self._update_graph)
        x_axis_label = ttk.Label(self, text=" to ")
        x_axis_label.grid(row=2, column=4)
        self.max_x_axis = tk.StringVar(self)
        self.max_x_axis.set("")
        x_axis_max_value_entry = ttk.Entry(self, textvariable=self.max_x_axis, width=7, validate='key', validatecommand=(validate, '%P'))
        x_axis_max_value_entry.grid(row=2, column=5)
        x_axis_max_value_entry.bind('<KeyRelease>', self._update_graph)

        self.new_command = tk.StringVar(self)
        self.new_command.set("")
        self.add_command_dropdown = ttk.Combobox(self, values=GraphCanvas.__graph_commands,
                                                 textvariable=self.new_command,
                                                 state="readonly", width=70)
        self.add_command_dropdown.grid(row=3, column=0, columnspan=5)
        self.add_command_button = ttk.Button(self, text="+", width=3)
        self.add_command_button.grid(row=3, column=5)

        # self.parameters: Dict[str, Any] = {}

    def _update_graph_axis_options(self):
        self.y_axis_dropdown.configure(values=GraphCanvas.__possible_axes)
        self.y_axis_dropdown.set(GraphCanvas.__possible_axes[0])
        self.x_axis_dropdown.configure(values=GraphCanvas.__possible_axes)
        if len(GraphCanvas.__possible_axes) > 1:
            self.x_axis_dropdown.set(GraphCanvas.__possible_axes[1])
        else:
            self.x_axis_dropdown.set(GraphCanvas.__possible_axes[0])

    def _update_graph(self, *args):
        y_col, y_min, y_max = self.y_axis.get(), self.min_y_axis.get(), self.max_y_axis.get()
        x_col, x_min, x_max = self.x_axis.get(), self.min_x_axis.get(), self.max_x_axis.get()
        # Correct the limits
        y_min = -np.inf if y_min in ["", "-"] else float(y_min)
        y_max = np.inf if y_max in ["", "-"] else float(y_max)
        x_min = -np.inf if x_min in ["", "-"] else float(x_min)
        x_max = np.inf if x_max in ["", "-"] else float(x_max)

        print(y_min, y_max, x_min, x_max)

        subset = GraphCanvas.__data.loc[(GraphCanvas.__data[y_col] > y_min) &
                                        (GraphCanvas.__data[y_col] < y_max) &
                                        (GraphCanvas.__data[x_col] > x_min) &
                                        (GraphCanvas.__data[x_col] < x_max), [y_col, x_col]]
        y_values, x_values = subset[y_col], subset[x_col]
        self.graph_canvas.ax.cla()
        self.graph_canvas.ax.plot(x_values, y_values)
        self.graph_canvas.draw()

    @classmethod
    def update_axis_options(cls, new_options: List[str]):
        # self.graph_canvas.ax.cla()
        cls.__possible_axes = new_options
        for instance in cls.__instances:
            instance._update_graph_axis_options()

    @classmethod
    def update_data(cls, new_data):
        cls.__data = new_data

    def add_parameter(self, label_text: str, parameter_object):
        raise NotImplementedError()
        label = ttk.Label(self, text=label_text)
        label.grid(row=2, column=0)
        self.y_axis_label = ttk.Label(self, text="X_axis: ")
        self.y_axis_label.grid(row=2, column=0)
        self.x_axis_button = ttk.Button(self)
        self.x_axis_button.grid(row=2, column=1)


if __name__ == "__main__":
    # Create a new tkinter window
    root = tk.Tk()
    root.title("Matplotlib in Tkinter")

    # Create a canvas widget to display the matplotlib figure
    canvas = GraphCanvas(master=root)
    # canvas.draw()
    canvas.get_tk_widget().pack()

    # Run the tkinter event loop
    tk.mainloop()
