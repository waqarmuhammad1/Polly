import ntpath
import pandas as pd
from logger import Logger
from Commons import *

class FileReader():

    def __int__(self):
        self.data = None
        self.file_path = None
        self.file_name = None
        self.column_names = None
        self.sheet_names = None
        self.file_type = None
        self.logger = Logger()


    def read_file(self, file_path, delimiter):
        filename, file_extension = os.path.splitext(file_path)

        self.file_type = file_extension

        data_df = None
        if file_extension == '.xlsx' or file_extension == '.xls':
            data_df = self.read_excel(file_path)

        elif file_extension == '.csv':
            data_df = self.read_csv(file_path, delimiter)

        return data_df


    #read excel file, ignores indexes
    def read_excel(self, file_path):

        try:
            self.file_path = file_path
            self.file_name = ntpath.basename(file_path)
            excel_file = pd.ExcelFile(file_path)
            self.sheet_names = excel_file.sheet_names

            data_df = {sheet_name: excel_file.parse(sheet_name)
                   for sheet_name in excel_file.sheet_names}

            return data_df
        except:
            user_exception, log_exception = self.logger.get_exception()
            self.logger.log(str(log_exception) + "" + str(user_exception), self.logger.ERROR)
            return user_exception

    #read csv file, only if there is a header available
    def read_csv(self, file_path, delimiter=','):

        try:

            data_df = pd.read_csv(file_path, delimiter=delimiter)

            return data_df
        except:
            user_exception, log_exception = self.logger.get_exception()
            self.logger.log(str(log_exception) + "" + str(user_exception), self.logger.ERROR)
            return {'error': user_exception}

    def get_columns(self, sheet_name=None):
        if self.file_type != '.csv':
            try:
                self.column_names = list(self.data[sheet_name].columns)
            except:
                raise
        else:
            self.column_names = list(self.data.columns)

        return self.column_names


