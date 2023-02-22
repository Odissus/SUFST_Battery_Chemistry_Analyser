import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphCanvas(FigureCanvasTkAgg):
    def __init__(self, master):
        self.master = master

        # Create a new matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)

        # Add a subplot to the figure
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Sample Plot")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.plot([1, 2, 3, 4], [10, 5, 8, 3])
        super().__init__(self.fig, master=self.master)
        self.draw()

    def on_resize(self, event):
        w, h = event.width, event.height
        self.fig.set_size_inches(w / 100, h / 100)

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
