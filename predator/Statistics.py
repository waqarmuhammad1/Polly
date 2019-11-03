import pandas as pd
from logger import Logger

class Stats():

    def __init__(self):
        self.data_desc = None
        self.logger = Logger()

    def get_data_description(self, data_df):

        # Null Values handling
        null_columns = data_df.columns[data_df.isnull().any()]
        null_vals = data_df[null_columns].isnull().sum()
        null_vals.name = "Nulls"

        self.logger.log('appending null count column in data')


        # percentile list
        perc = [.20, .40, .60, .80]

        # list of dtypes to include
        include = ['float', 'int']
        data_desc = data_df.describe(percentiles=perc, include=include)
        data_desc = data_desc.append(null_vals)
        data_desc = data_desc.applymap(str)
        data_desc['Statistics'] = data_desc.index
        cols = data_desc.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data_desc = data_desc[cols]
        data_desc.reset_index()

        return data_desc

    def get_column_description(self, data_df, column_name):

        if data_df[column_name].dtype == 'object':
            # Null Values handling
            null_columns = data_df.columns[data_df.isnull().any()]
            null_vals = data_df[null_columns].isnull().sum()
            null_vals.name = "Nulls"
            self.logger.log('appending null count column in data')

            data_df = data_df.append(null_vals)

            column_desc = data_df[column_name].describe()

            return column_desc
        else:
            return 'Column is not string'

    def get_correlation(self, data_df):
        self.logger.log('calculating correlation')
        corr_df = data_df.corr()

        self.logger.log('inserting correlation dataframe index as [Variables] column')
        corr_df.insert(loc=0, column='Variables', value=corr_df.index)

        self.logger.log('deleting index column')
        corr_df.reset_index(drop=True, inplace=True)

        return corr_df
