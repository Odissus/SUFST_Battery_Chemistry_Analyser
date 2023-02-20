import pandas as pd
import numpy as np
import warnings
from typing import Dict, Any
import copy
import datetime


class FileParser:
    def __init__(self, filename=""):
        self.filename = filename
        self.data_frame: pd.DataFrame = None
        self.reduced_data_frame: pd.DataFrame = None
        self.constants: Dict[str: Any] = {}

    def parse(self, skip_rows: int = 3, apply_fixes: bool = True, seperator='\s+', fix_time=True, callback_function=None):
        def change_time(time_string):
            zero_time = datetime.datetime.strptime("00:00:0", "%H:%M:%S")
            format_data = "%H:%M:%S.%f"
            try:
                dt = datetime.datetime.strptime(time_string, format_data)
            except ValueError:
                try:
                    format_data = "%H:%M:%S"
                    dt = datetime.datetime.strptime(time_string, format_data)
                except ValueError:
                    format_data = "%H:%M"
                    dt = datetime.datetime.strptime(time_string, format_data)
            time_difference = (dt - zero_time).total_seconds()
            return time_difference

        self.data_frame = pd.read_csv(self.filename, sep=seperator, skiprows=skip_rows)  # Needed to fix the unicode error
        self.reduced_data_frame = copy.deepcopy(self.data_frame)
        if apply_fixes:
            for (i, column) in enumerate(self.data_frame.columns):
                unique_values = self.data_frame[column].unique()
                if fix_time:
                    if 'TIME' in column.upper():
                        times = self.data_frame[column].apply(change_time)
                        self.data_frame[column] = self.reduced_data_frame[column] = times
                if len(unique_values) == 1:
                    self.constants.update({column: unique_values[0]})
                    del self.reduced_data_frame[column]
                if callback_function is not None:
                    callback_function(i+1,  len(self.data_frame.columns))


    def read(self):
        self.parse(skip_rows=0, apply_fixes=True, seperator=",", fix_time=False)

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
