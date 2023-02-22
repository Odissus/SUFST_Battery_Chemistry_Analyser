import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphCanvas(tk.Frame):
    class _GraphCanvas(FigureCanvasTkAgg):
        def __init__(self, master):
            self.master = master

            # Create a new matplotlib figure
            self.fig = Figure(figsize=(5, 4), dpi=100)
            self.fig.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.9)

            # Add a subplot to the figure
            self.ax = self.fig.add_subplot(111)
            self.ax.set_title("Sample Plot")
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")
            self.ax.plot([1, 2, 3, 4], [10, 5, 8, 3])
            super().__init__(self.fig, master=self.master)
            self.draw()

        def on_resize(self, event):
            w, h = event.width, event.height
            self.fig.set_size_inches(w / 100, h / 100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_canvas = GraphCanvas._GraphCanvas(self)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, rowspan=180, columnspan=9)
        self.y_axis_button = ttk.Button(self)
        self.y_axis_button.grid(row=170, column=4)
        self.x_axis_button = ttk.Button(self)
        self.x_axis_button.grid(row=90, column=0)



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
