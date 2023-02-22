from tkinter import *
from src import *


if __name__ == "__main__":
    #fp = FileParser("SUFST 1C-10C - RAW DATA.txt")
    #fp.parse()
    #fp.save_as("corrected_data.csv")
    fp = FileParser("corrected_data.csv")
    fp.read()
    #print(fp.constants)
    #print(fp.reduced_data_frame.head())
    root = Tk()
    mw = MainWindow(root, headings=list(fp.reduced_data_frame.columns), data=fp.reduced_data_frame, constants=fp.constants)
    mw.populate_table(fp.reduced_data_frame)
    root.mainloop()
