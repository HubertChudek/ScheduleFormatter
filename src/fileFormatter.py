import pandas as pd


class FileFormatter:

    def __init__(self, data_frame):
        self.dataFrame = data_frame

    def format_data_column(self, column_name, format_string):
        temp = self.dataFrame[column_name].astype(str)
        return pd.to_datetime(temp).apply(lambda x: x.strftime(format_string))

    def format_time_column(self, column_name, format_string):
        temp = pd.to_datetime(self.dataFrame[column_name])
        return temp.dt.strftime(format_string)
