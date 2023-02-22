import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, Any


class GraphCanvas(tk.Frame):
    class _GraphCanvas(FigureCanvasTkAgg):
        def __init__(self, master):
            self.master = master

            # Create a new matplotlib figure
            self.fig = Figure(figsize=(5, 4), dpi=100)
            #self.fig.subplots_adjust(left=0.1, bottom=0.1, right=1, top=1)

            # Add a subplot to the figure
            self.ax = self.fig.add_subplot(111)
            #self.ax.set_title("Sample Plot")
            #self.ax.set_xlabel("")
            #self.ax.set_ylabel("")
            self.ax.plot([1, 2, 3, 4], [10, 5, 8, 3])
            super().__init__(self.fig, master=self.master)
            self.draw()

        def on_resize(self, event):
            w, h = event.width, event.height
            self.fig.set_size_inches(w / 100, h / 100)

    def __init__(self, possible_axes=None, *args, **kwargs):
        if possible_axes is None:
            self.possible_axes = ["demo option 1", "demo option 2"]

        super().__init__(*args, **kwargs)
        self.graph_canvas = GraphCanvas._GraphCanvas(self)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, columnspan=6)

        y_axis_label = ttk.Label(self, text="Y_axis: ")
        y_axis_label.grid(row=1, column=0, sticky="e")
        self.y_axis = tk.StringVar(self)
        self.y_axis.set(self.possible_axes[0])
        self.y_axis_dropdown = ttk.Combobox(self, values=self.possible_axes, textvariable=self.y_axis, state="readonly")
        self.y_axis_dropdown.grid(row=1, column=1, sticky="w")
        y_axis_domain_label = ttk.Label(self, text="Domain: ")
        y_axis_domain_label.grid(row=1, column=2, sticky="e")
        self.min_y_axis = tk.StringVar(self)
        self.min_y_axis.set("")
        y_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_y_axis, width=5)
        y_axis_min_value_entry.grid(row=1, column=3, sticky="w")
        y_axis_label = ttk.Label(self, text=" to ")
        y_axis_label.grid(row=1, column=4)
        self.max_y_axis = tk.StringVar(self)
        self.max_y_axis.set("")
        y_axis_max_value_entry = ttk.Entry(self, textvariable=self.min_y_axis, width=5)
        y_axis_max_value_entry.grid(row=1, column=5, sticky="w")

        x_axis_label = ttk.Label(self, text="X_axis: ")
        x_axis_label.grid(row=2, column=0, sticky="e")
        self.x_axis = tk.StringVar(self)
        self.x_axis.set(self.possible_axes[0])
        x_axis_dropdown = ttk.Combobox(self, values=self.possible_axes, textvariable=self.x_axis, state="readonly")
        x_axis_dropdown.grid(row=2, column=1, sticky="w")
        x_axis_domain_label = ttk.Label(self, text="Domain: ")
        x_axis_domain_label.grid(row=2, column=2, sticky="e")
        self.min_x_axis = tk.StringVar(self)
        self.min_x_axis.set("")
        x_axis_min_value_entry = ttk.Entry(self, textvariable=self.min_x_axis, width=5)
        x_axis_min_value_entry.grid(row=2, column=3, sticky="w")
        x_axis_label = ttk.Label(self, text=" to ")
        x_axis_label.grid(row=2, column=4)
        self.max_x_axis = tk.StringVar(self)
        self.max_x_axis.set("")
        x_axis_max_value_entry = ttk.Entry(self, textvariable=self.max_x_axis, width=5)
        x_axis_max_value_entry.grid(row=2, column=5, sticky="w")


        #self.parameters: Dict[str, Any] = {}

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
    #canvas.draw()
    canvas.get_tk_widget().pack()

    # Run the tkinter event loop
    tk.mainloop()
