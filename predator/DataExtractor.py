import pandas as pd
import numpy as np
from logger import Logger

class Extractor():

    def __int__(self):
        self.column_names = None
        self.column_data = None
        self.selected_df = None
        self.logger = Logger()

    def extract_user_data(self, data_df,data_source_type=None, table_name=None, db_name=None):
        try:
            if data_source_type is not None:
                data_df = self.check_data_source(data_df, data_source_type, table_name, db_name)
            # user_data = list(data_df.T.to_dict().values())
            user_data = list(data_df.to_dict('records'))
            return user_data
        except:
            raise


    def extract_column_names(self, data_df, data_source_type, table_name=None, db_name=None):
        try:
            if data_source_type is not None:
                data_df = self.check_data_source(data_df, data_source_type, table_name, db_name)
            column_names = list(data_df.columns)
            return column_names

        except:
            raise


    def extract_column_data(self, data_df, selected_columns, data_source_type=None, table_name=None, db_name=None):
        try:
            if data_source_type is not None:
                data_df = self.check_data_source(data_df, data_source_type, table_name, db_name)
            self.selected_df = data_df[selected_columns]
            user_data = list(self.selected_df.T.to_dict().values())
            return user_data, self.selected_df
        except:
            raise

    def extract_columns_to_filter(self, data_df, selected_method, data_source_type=None, table_name=None, db_name=None):
        try:
            # self.logger.log('METHOD: get_columns_to_filter()')
            # self.logger.log('methods selected by user: ' + str(selected_method))

            columns_to_filter = list(data_df.columns)
            # self.logger.log('columns selected to filter: ' + str(columns_to_filter))


            # self.logger.log('recording column data types')
            columns_dtype = dict(list(zip(data_df.columns, data_df.dtypes)))
            # self.logger.log('following data types found: ' + str(columns_dtype))

            int_type_methods = ['mean', 'median', 'mode', 'std']

            # self.logger.log('extracting columns for appropriate method types')
            if 'drop_missing_column' in selected_method or 'drop_missing_row' in selected_method or 'most_freq' in selected_method:
                columns_to_filter = [x for x in columns_dtype]
            elif selected_method in int_type_methods:
                columns_to_filter = [x for x in columns_dtype if columns_dtype[x] is np.dtype('int64')
                                     or columns_dtype[x] is np.dtype('float64')
                                     or columns_dtype[x] is np.dtype('float32')
                                     or columns_dtype[x] is np.dtype('int32')]
            else:
                columns_to_filter = [x for x in columns_dtype if columns_dtype[x] is np.dtype('O')]
            # self.logger.log('extraction complete')
            # self.logger.log('returning following columns to user: ' + str(columns_to_filter))
            # self.logger.log('METHOD_EXECUTED: get_columns_to_filter()')

            return columns_to_filter
        except:
            raise

    def extract_data_for_graph(self, data_df, column_names, data_source_type=None, table_name=None, db_name=None):
        try:

            graph_data = {}
            for column_name in column_names:
                user_data, column_series = self.extract_column_data(data_df, column_name)
                graph_data[column_name] = list(column_series)
            return graph_data
        except:
            raise
        
    def extract_string_columns(self, data_df, data_source_type=None, table_name=None, db_name=None):
        try:
            columns_dtype = dict(list(zip(data_df.columns, data_df.dtypes)))
            columns_to_filter = [x for x in columns_dtype if columns_dtype[x] is np.dtype('O')]
            return columns_to_filter
        except:
            raise

    def merge_data_by_col(self, df_list):

        merged_df = pd.concat(df_list, axis=1)
        return merged_df


    def check_data_source(self, data_df, data_source_type, table_name=None, db_name=None):
        try:

            if data_source_type == '.csv':
                return data_df
            elif data_source_type == '.xlsx' or data_source_type == ".xls":
                data_df = data_df[table_name]
            elif data_source_type == 'oracle' or data_source_type == 'mssql' or data_source_type == 'mysql':
                data_df = data_df[db_name][table_name]

            return data_df
        except:
            raise

