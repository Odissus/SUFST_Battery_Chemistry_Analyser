import pandas as pd
import numpy as np
import warnings
from typing import Dict, Any
import copy
import datetime
import re


class FileParser:
    def __init__(self, filename=""):
        self.filename = filename
        self.data_frame: pd.DataFrame = None
        self.reduced_data_frame: pd.DataFrame = None
        self.constants: Dict[str: Any] = {}
        self.cycles_start_indexes = {}

    def parse(self, skip_rows: int = 3, apply_fixes: bool = True, seperator='\s+', fix_time=True, callback_function=None, ravel_time=True):
        def change_time(time_string):
            zero_time = datetime.datetime.strptime("00:00:0", "%H:%M:%S")
            format_data = None
            patterns = [["%H:%M:%S.%f", r'^\d{2}:\d{2}:\d{1,2}\.\d{1,6}$'],
                        ["%H:%M:%S", r'^\d{2}:\d{2}:\d{1,2}$'],
                        [ "%H:%M", r'^\d{2}:\d{2}$']]
            for (format, regex) in patterns:
                if re.match(regex, time_string):
                    format_data = format
                    break
            if format_data is None:
                raise ValueError("Invalid time format")
            dt = datetime.datetime.strptime(time_string, format_data)
            time_difference = (dt - zero_time).total_seconds()
            return time_difference

        def _ravel_time(times: np.ndarray):
            time_differences = np.diff(times)
            reset_points = np.where(time_differences < 0)[0]
            for reset_point, offset in zip(reset_points, times[reset_points]):
                times[reset_point+1:] = times[reset_point+1:] + offset
            return times



        self.data_frame = pd.read_csv(self.filename, sep=seperator, skiprows=skip_rows)  # Needed to fix the unicode error
        self.reduced_data_frame = copy.deepcopy(self.data_frame)
        if apply_fixes:
            for (i, column) in enumerate(self.data_frame.columns):
                unique_values = self.data_frame[column].unique()
                if fix_time:
                    if 'TIME' in column.upper():
                        times = self.data_frame[column].apply(change_time)
                        if ravel_time:
                            times = _ravel_time(times)
                        self.data_frame[column] = self.reduced_data_frame[column] = times
                if column.upper() == "MD":
                    self._get_charge_cycles_indexes(self.data_frame[column])
                if len(unique_values) == 1:
                    self.constants.update({column: unique_values[0]})
                    del self.reduced_data_frame[column]
                if callback_function is not None:
                    callback_function(i+1,  len(self.data_frame.columns))


    def read(self):
        self.parse(skip_rows=0, apply_fixes=True, seperator=",", fix_time=False)

    def _get_charge_cycles_indexes(self, modes: np.array):
        # Get the unique values in the array
        unique_vals = np.unique(modes)

        # Create a dictionary to map unique values to integers
        val_map = {val: i for i, val in enumerate(unique_vals)}

        # Map each value in the input array to an integer
        new_arr = np.array([val_map[val] for val in modes])

        # Find the indices where the values change
        change_indices = np.hstack([0, np.where(np.diff(new_arr) != 0)[0] + 1])

        # Update the dictionary of changes
        for val in unique_vals:
            self.cycles_start_indexes[val] = change_indices[np.where(new_arr[change_indices] == val_map[val])]

    def save_as(self, filename=""):
        if self.data_frame is None:
            warnings.warn("File not parsed, run file_parsed.parse() first")
            return
        type = filename.split(".")[1]
        if type == "csv":
            self.data_frame.to_csv(filename, index=False)
        elif type == "xlsx":
            with pd.ExcelWriter(filename) as writer:
                self.reduced_data_frame.to_excel(writer, sheet_name="Variables", index=False)
                if len(self.constants) > 0:
                    constants = pd.DataFrame(self.constants.items())
                    constants.to_excel(writer, sheet_name="Constants", index=False)
        else:
            warnings.warn("Saving in formats other than csv not implemented")

if __name__ == "__main__":
    filename = "SUFST 1C-10C - RAW DATA.txt"
    fp = FileParser(filename=filename)
    fp.parse()
    fp.save_as("parsed.csv")
