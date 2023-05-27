import tkinter as tk
from tkinter import ttk
from src.Windows.Tooltip import ToolTip
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, Any, Iterable, List
import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimise
from numpy.polynomial import Polynomial
from scipy.fft import fft


class GraphCommand(tk.Frame):
    def __init__(self, master, command_index: int):
        super().__init__(master)
        self.master = master
        self.command_index = command_index

    def delete(self):
        super().grid_forget()
        index = self.command_index
        self.master.commands.remove(self)
        self.master.regrid_commands()


class CurveFit(GraphCommand):
    _curve_fits = ["Polynomial", "Exponential", "Logarithmic"]

    def __init__(self, master, command_index: int):
        super().__init__(master, command_index)
        validate = master.register(self._validate_limit)
        self.remove_command_button = ttk.Button(self, text="-", width=3, command=self.delete)
        self.remove_command_button.grid(row=0, column=0)

        self.method = tk.StringVar(master)
        self.method.set(CurveFit._curve_fits[0])
        method_dropdown = ttk.Combobox(self, values=Integrate._integration_methods,
                                       textvariable=self.method,
                                       state="readonly", width=15)
        method_dropdown.grid(row=0, column=1, sticky="w")

        self.integration_option = tk.StringVar(master)
        self.integration_option.set(" fit where n = ")
        label = ttk.Label(self, textvariable=self.integration_option)
        label.grid(row=0, column=2)

        self.control_variable = tk.StringVar(master)
        self.control_variable.set("")
        control_value_entry = ttk.Entry(self, textvariable=self.control_variable, width=3, validate='key',
                                        validatecommand=(validate, '%P'))
        control_value_entry.grid(row=0, column=3)

        label = ttk.Label(self, text=" between ")
        label.grid(row=0, column=4)

        self.min_limit = tk.StringVar(master)
        self.min_limit.set("")
        min_value_entry = ttk.Entry(self, textvariable=self.min_limit, width=7, validate='key',
                                    validatecommand=(validate, '%P'))
        min_value_entry.grid(row=0, column=5)

        label = ttk.Label(self, text="and")
        label.grid(row=0, column=6)

        self.max_limit = tk.StringVar(master)
        self.max_limit.set("")
        max_value_entry = ttk.Entry(self, textvariable=self.max_limit, width=7, validate='key',
                                    validatecommand=(validate, '%P'))
        max_value_entry.grid(row=0, column=7)

        self.go_button = ttk.Button(self, text="Go", width=5, command=self.curve_fit)
        self.go_button.grid(row=0, column=8)

        self.result = tk.StringVar(master)
        self.result.set("")
        self.result_label = ttk.Entry(self, textvariable=self.result, width=50, state="readonly")
        self.result_label.grid(row=1, column=1, columnspan=8, sticky="e")

    def _validate_limit(self, new_value):
        # If the new value is empty, allow it
        if new_value == '' or new_value == '-':
            return True
        # Try to convert the new value to a float
        try:
            value = float(new_value)
        except ValueError:
            # self.errors.update({""})
            return False
        # If the new value is not between 3 and 5, disallow it
        # if value < 3 or value > 5:
        #    return False
        # Allow the new value
        return True

    def curve_fit(self):
        # optimise.curve_fit() - to be used for custom function, might implement this, might not
        method = self.method.get()
        xs, ys = self.master.xs, self.master.ys
        if method == CurveFit._curve_fits[0]:
            degree = int(self.control_variable.get())
            coef = np.round(np.polyfit(xs, ys, degree), 5)
            result = "+".join([f"{c}x^{len(coef) - i - 1}" for (i, c) in enumerate(coef)])
        elif method == CurveFit._curve_fits[1]:
            result = integrate.simpson(ys, xs, dx=1)
        self.result.set(result)


class Integrate(GraphCommand):
    _integration_methods = ["Trapezoidal", "Simpson", "Newton-Cotes"]

    def __init__(self, master, command_index: int):
        super().__init__(master, command_index)
        validate = master.register(self._validate_limit)

        self.remove_command_button = ttk.Button(self, text="-", width=3, command=self.delete)
        self.remove_command_button.grid(row=0, column=0)

        self.integration_methods = tk.StringVar(master)
        self.integration_methods.set(Integrate._integration_methods[0])
        self.method_dropdown = ttk.Combobox(self, values=Integrate._integration_methods,
                                            textvariable=self.integration_methods,
                                            state="readonly", width=15)
        self.method_dropdown.grid(row=0, column=1, sticky="w")

        self.integration_option = tk.StringVar(master)
        self.integration_option.set(" integration where n = ")
        label = ttk.Label(self, textvariable=self.integration_option)
        label.grid(row=0, column=2)

        self.control_variable = tk.StringVar(master)
        self.control_variable.set("")
        control_value_entry = ttk.Entry(self, textvariable=self.control_variable, width=3, validate='key',
                                        validatecommand=(validate, '%P'))
        control_value_entry.grid(row=0, column=3)

        label = ttk.Label(self, text=" between ")
        label.grid(row=0, column=4)

        self.min_limit = tk.StringVar(master)
        self.min_limit.set("")
        min_value_entry = ttk.Entry(self, textvariable=self.min_limit, width=7, validate='key',
                                    validatecommand=(validate, '%P'))
        min_value_entry.grid(row=0, column=5)

        label = ttk.Label(self, text="and")
        label.grid(row=0, column=6)

        self.max_limit = tk.StringVar(master)
        self.max_limit.set("")
        max_value_entry = ttk.Entry(self, textvariable=self.max_limit, width=7, validate='key',
                                    validatecommand=(validate, '%P'))
        max_value_entry.grid(row=0, column=7)

        self.go_button = ttk.Button(self, text="Go", width=5, command=self.integrate)
        self.go_button.grid(row=0, column=8)

        # self.method_dropdown.bind('<<ComboboxSelected>>', self._update_graph)

        self.result = tk.StringVar(master)
        self.result.set("")
        self.result_label = ttk.Entry(self, textvariable=self.result, width=30, state="readonly")
        self.result_label.grid(row=1, column=1, columnspan=8, sticky="e")

    def _validate_limit(self, new_value):
        # If the new value is empty, allow it
        if new_value == '' or new_value == '-':
            return True
        # Try to convert the new value to a float
        try:
            value = float(new_value)
        except ValueError:
            # self.errors.update({""})
            return False
        # If the new value is not between 3 and 5, disallow it
        # if value < 3 or value > 5:
        #    return False
        # Allow the new value
        return True

    def integrate(self):
        integration_method = self.integration_methods.get()
        xs, ys = self.master.xs, self.master.ys
        if integration_method == Integrate._integration_methods[0]:
            result = integrate.trapezoid(ys, xs, dx=1)
        elif integration_method == Integrate._integration_methods[1]:
            result = integrate.simpson(ys, xs, dx=1)
        self.result.set(result)

    @property
    def graph_command(self):
        return "Integrate"


class GraphCanvas(tk.Frame):
    __graph_commands = ["", "Differentiate", "Integrate", "Curve fit"]
    __possible_axes: List[str] = []
    __instances: List['GraphCanvas'] = []
    __data: Any = None

    class _GraphCanvas(FigureCanvasTkAgg):
        def __init__(self, master):
            self.master = master

            # Create a new matplotlib figure
            self.fig = Figure(figsize=(4, 3), dpi=100)
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
            # self.errors.update({""})
            return False
        # If the new value is not between 3 and 5, disallow it
        # if value < 3 or value > 5:
        #    return False
        # Allow the new value
        return True

    def regrid_commands(self):
        for (index, command) in zip(range(len(self.commands)), self.commands):
            self.rowconfigure(index + 3, weight=2)
            self.commands[index].grid(row=index + 3, column=0, columnspan=5)
        self.add_command_dropdown.grid(row=len(self.commands) + 3, column=0, columnspan=5)
        self.add_command_button.grid(row=len(self.commands) + 3, column=5)
        self.rowconfigure(len(self.commands), weight=1)

    def __init__(self, master, regrid_command, index: int, *args, **kwargs):
        # self.master = master
        GraphCanvas.__instances.append(self)
        super().__init__(master=master, *args, **kwargs)
        self.index = index
        self.regrid_command = regrid_command
        validate = master.register(self.validate_limit)
        self.commands = []
        self.errors = {}
        self.current_axis_limits = []
        self.xs, self.ys = np.array([]), np.array([])
        self.xs_split, self.ys_split = np.array([]), np.array([])

        self.close_button = ttk.Button(self, text="X", width=3, command=self.delete)
        self.close_button.place(anchor="nw", x=5, y=5)

        self.cycle_button_text = tk.StringVar()
        self.cycle_button_text.set("⮔")  # ⭢
        self.cycle_button = ttk.Button(self, textvariable=self.cycle_button_text, width=3,
                                       command=self.split_by_most_common_frequency)
        self.cycle_button.place(anchor="nw", x=5, y=30)

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
        y_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_y_axis, width=7, validate='key',
                                           validatecommand=(validate, '%P'))
        y_axis_min_value_entry.grid(row=1, column=3)
        y_axis_min_value_entry.bind('<KeyRelease>', self._update_graph)
        y_axis_label = ttk.Label(self, text=" to ")
        y_axis_label.grid(row=1, column=4)
        self.max_y_axis = tk.StringVar(self)
        self.max_y_axis.set("")
        y_axis_max_value_entry = ttk.Entry(self, textvariable=self.max_y_axis, width=7, validate='key',
                                           validatecommand=(validate, '%P'))
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
        x_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_x_axis, width=7, validate='key',
                                           validatecommand=(validate, '%P'))
        x_axis_min_value_entry.grid(row=2, column=3)
        x_axis_min_value_entry.bind('<KeyRelease>', self._update_graph)
        x_axis_label = ttk.Label(self, text=" to ")
        x_axis_label.grid(row=2, column=4)
        self.max_x_axis = tk.StringVar(self)
        self.max_x_axis.set("")
        x_axis_max_value_entry = ttk.Entry(self, textvariable=self.max_x_axis, width=7, validate='key',
                                           validatecommand=(validate, '%P'))
        x_axis_max_value_entry.grid(row=2, column=5)
        x_axis_max_value_entry.bind('<KeyRelease>', self._update_graph)

        self.new_command = tk.StringVar(self)
        self.new_command.set("")
        self.add_command_dropdown = ttk.Combobox(self, values=GraphCanvas.__graph_commands,
                                                 textvariable=self.new_command,
                                                 state="readonly", width=70)
        self.add_command_dropdown.grid(row=3, column=0, columnspan=5)
        self.add_command_button = ttk.Button(self, text="+", width=3, command=self.add_command)
        self.add_command_button.grid(row=3, column=5)
        for i in range(3):
            self.rowconfigure(i + 1, weight=1)
        # self.parameters: Dict[str, Any] = {}

    def delete(self) -> None:
        super().grid_forget()
        index = self.index
        super().destroy()
        self.regrid_command(index)

        # self.master.regrid_commands()

    def add_command(self):
        command_to_add = self.new_command.get()
        if command_to_add == GraphCanvas.__graph_commands[2]:
            new_frame = Integrate(self, len(self.commands))
        elif command_to_add == GraphCanvas.__graph_commands[3]:
            new_frame = CurveFit(self, len(self.commands))
        else:
            return
        self.commands.append(new_frame)
        row_number = len(self.commands) + 3
        new_frame.grid(row=row_number - 1, column=0, columnspan=6)
        # Set the column weight for the new column
        self.rowconfigure(row_number - 1, weight=2)
        self.add_command_dropdown.grid(row=row_number, column=0, columnspan=5)
        self.add_command_button.grid(row=row_number, column=5)
        self.rowconfigure(row_number, weight=1)

    def _change_button_icon(self, button_text_variable):
        pass

    def split_by_most_common_frequency(self):
        # Calculate the length of each segment based on the repeating frequency
        data_arrays = []
        power_arrays = []
        time_arrays = []
        mode_changes = np.diff(self.__data['__MDToken'].values)

        # Find the indices where mode changes occur
        change_indices = np.where(mode_changes != 0)[0] + 1

        # Split the data
        start_index = 0

        for end_index in change_indices:
            power_array = self.ys[start_index:end_index]
            time_array = self.xs[start_index:end_index]
            time_array -= time_array[0]  # Reset time to 0 for each array
            time_arrays.append(time_array)
            power_arrays.append(power_array)
            start_index = end_index

        self.xs_split, self.ys_split = time_arrays, power_arrays
        self._update_graph(cycles=True)

    def _update_graph_axis_options(self):
        self.y_axis_dropdown.configure(values=GraphCanvas.__possible_axes)
        self.y_axis_dropdown.set(GraphCanvas.__possible_axes[0])
        self.x_axis_dropdown.configure(values=GraphCanvas.__possible_axes)
        if len(GraphCanvas.__possible_axes) > 1:
            self.x_axis_dropdown.set(GraphCanvas.__possible_axes[1])
        else:
            self.x_axis_dropdown.set(GraphCanvas.__possible_axes[0])

    def _update_graph(self, *args, cycles=False):
        if cycles:
            self.graph_canvas.ax.cla()
            for (xs, ys) in zip(self.xs_split, self.ys_split):
                self.graph_canvas.ax.plot(xs, ys)
            self.graph_canvas.draw()
            return

        y_col, y_min, y_max = self.y_axis.get(), self.min_y_axis.get(), self.max_y_axis.get()
        x_col, x_min, x_max = self.x_axis.get(), self.min_x_axis.get(), self.max_x_axis.get()
        # Correct the limits
        y_min = -np.inf if y_min in ["", "-"] else float(y_min)
        y_max = np.inf if y_max in ["", "-"] else float(y_max)
        x_min = -np.inf if x_min in ["", "-"] else float(x_min)
        x_max = np.inf if x_max in ["", "-"] else float(x_max)

        subset = GraphCanvas.__data.loc[(GraphCanvas.__data[y_col] > y_min) &
                                        (GraphCanvas.__data[y_col] < y_max) &
                                        (GraphCanvas.__data[x_col] > x_min) &
                                        (GraphCanvas.__data[x_col] < x_max), [y_col, x_col]]
        self.xs, self.ys = np.array(subset[x_col]), np.array(subset[y_col])
        if len(self.xs.shape) == 2:
            self.xs, self.ys = self.xs.T[0], self.xs.T[0]
        print(self.xs)
        self.graph_canvas.ax.cla()
        self.graph_canvas.ax.plot(self.xs, self.ys)
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
