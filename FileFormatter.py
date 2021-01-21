import pandas as pd


class FileFormatter:

    def __init__(self, data_frame):
        self.dataFrame = data_frame

    def format_data_collumn(self, column_name, format_string):
        temp = self.dataFrame[column_name].astype(str)
        temp = pd.to_datetime(temp).apply(lambda x: x.strftime(format_string))
        return temp
