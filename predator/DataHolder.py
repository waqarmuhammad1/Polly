from Regression_Params import *
from Classification_Params import *

class Holder():

    user_id = None
    user_pass = None

    analysis_mode = None

    data_df = None
    user_data = None

    data_source_type = None
    table_name = None
    db_name = None

    train_df = None
    train_user_data = None
    train_vars = None

    target_df = None
    target_user_data = None
    target_var = None

    selected_df = None
    selected_user_data = None

    desc_df = None
    desc_user_data = None

    correlation_df = None
    correlation_user_data = None

    processed_data = None
    processed_user_data = None

    methods_applied = []
    attributes_encoded = []

    available_methods = ['mean', 'mode', 'std', 'drop_missing_column', 'drop_missing_row', 'most_freq']

    classification_algorithms = ['Gausian Naive Bayes', 'Bernoulli Naive Bayes',
                                 #'Ada Booster',  # 'Multi Layer Preceptron',
                                 #'Decision Tree',
                                 #'Random Forest',
                                 'Linear SVC', 'Support Vector']

    regression_algorithms = ['Linear Regression', 'Elastic Regression', 'Lars Regression', 'Lasso Regression',
                             'LassoLars Regression']

    regression_params = Get_Regression_Algo_Params()
    classification_params = Get_Classification_Params()
    
    selected_algorithms = None
    selected_algorithms_params = None

    test_size = 0.2

    algorithm_results = None
    training_data = None
    training_user_data = None

    test_data = None
    test_user_data = None

    predicted_data = None
    predicted_user_data = None

    prediction_values = None

    def append_methods_applied(self, applied_method):
        try:
            self.methods_applied.append(applied_method)
        except:
            raise

    def get_methods_applied(self):
        return self.methods_applied

    def append_attributes_encoded(self, encoded_attributes):
        try:
            self.attributes_encoded.append(encoded_attributes)
        except:
            raise

    def get_attributes_encoded(self):
        return self.attributes_encoded

    def reset_data(self):
        self.data_df = None
        self.user_data = None

        self.data_source_type = None
        self.table_name = None
        self.db_name = None

        self.train_df = None
        self.train_user_data = None
        self.train_vars = None

        self.target_df = None
        self.target_user_data = None
        self.target_var = None

        self.selected_df = None
        self.selected_user_data = None

        self.desc_df = None
        self.desc_user_data = None

        self.correlation_df = None
        self.correlation_user_data = None

        self.processed_data = None
        self.processed_user_data = None

        self.methods_applied = []
        self.attributes_encoded = []

        self.available_methods = ['mean', 'mode', 'std', 'drop_missing_column', 'drop_missing_row', 'most_freq']

        self.classification_algorithms = ['Gausian Naive Bayes', 'Bernoulli Naive Bayes',
                                     # 'Ada Booster',  # 'Multi Layer Preceptron',
                                     # 'Decision Tree',
                                     # 'Random Forest',
                                     'Linear SVC', 'Support Vector']

        self.regression_algorithms = ['Linear Regression', 'Elastic Regression', 'Lars Regression', 'Lasso Regression',
                                 'LassoLars Regression']

        self.regression_params = Get_Regression_Algo_Params()
        self.classification_params = Get_Classification_Params()

        self.selected_algorithms = None
        self.selected_algorithms_params = None

        self.test_size = 0.2

        self.algorithm_results = None
        self.training_data = None
        self.training_user_data = None

        self.test_data = None
        self.test_user_data = None

        self.predicted_data = None
        self.predicted_user_data = None

        self.prediction_values = None
