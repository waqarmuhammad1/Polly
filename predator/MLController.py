from RegressionController import *
from ClassificationController import *


def apply_algorithms(analysis_mode, data_df, training_vars, target_var, selected_algorithms, test_size):

    try:
        result = None
        samples = None
        training_data = None
        test_data = None
        predicted_data = None

        if 'regression' in analysis_mode.lower():
            result, samples, training_data,\
                test_data, predicted_data = Perform_Regression(data_df, training_vars,
                                                               target_var, selected_algorithms, test_size)
        elif 'classification' in analysis_mode.lower():
            result, samples, training_data,\
                test_data, predicted_data = Perform_Classification(data_df, training_vars,
                                                                   target_var, selected_algorithms, test_size)

        result = {'algorithm_results': result, 'prediction_values': samples}

        return result, training_data, test_data, predicted_data
    except:
        raise