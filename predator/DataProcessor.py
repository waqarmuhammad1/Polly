import pandas as pd
from logger import Logger

class Processor():

    def __init__(self):
        self.logger = Logger()

    def process_null_columns(self, data_df, selected_column, selected_method):
        try:
            if 'mean' in selected_method:
                if data_df[selected_column].isnull().values.any():
                    self.logger.log('replacing missing values with mean for column: ' + str(selected_column))
                    data_df[selected_column].fillna(value=data_df[selected_column].mean(), inplace=True)
            elif 'mode' in selected_method:
                if data_df[selected_column].isnull().values.any():
                    self.logger.log('replacing missing values with mode for column: ' + str(selected_column))
                    data_df[selected_column].fillna(value=data_df[selected_column].mode(), inplace=True)
            elif 'std' in selected_method:
                if data_df[selected_column].isnull().values.any():
                    self.logger.log('replacing missing values with std for column: ' + str(selected_column))
                    data_df[selected_column].fillna(value=data_df[selected_column].std, inplace=True)
            elif 'drop_missing_column' in selected_method:
                self.logger.log('dropping selected column [reason=missing_values]: ' + str(selected_column))
                data_df.drop(selected_column, axis=1, inplace=True)
            elif 'drop_missing_row' in selected_method:
                self.logger.log('dropping selected rows [reason=missing_values]: ' + str(selected_column))
                # data_df.drop(selected_column, axis=0, inplace=True)
                data_df = data_df[data_df[selected_column].notnull()]
            elif 'most_freq' in selected_method:
                if data_df[selected_column].isnull().values.any():
                    self.logger.log('replacing missing values with most frequent for column: ' + str(selected_column))
                    data_df[selected_column].fillna(value=(data_df[selected_column].value_counts().idxmax()), inplace=True)


            self.logger.log('storing filtered data_df set in memory')
            return data_df
        except:
            raise

    def process_attribute_encoding(self, data_df, column_name):
        try:
            self.logger.log('preparation complete')

            self.logger.log('calculating categories of selected column: ' + str(column_name))
            data_df[column_name] = data_df[column_name].astype('category')
            self.logger.log('converting column data_df type by applying encoding')
            data_df[column_name] = data_df[column_name].cat.codes
            self.logger.log('conversion complete')

            self.logger.log('storing converted data_df in memory')
            return data_df
        except:
            raise

