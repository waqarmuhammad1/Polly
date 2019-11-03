from ClassificationMetrics import *
from ClassificationAlgorithms import *

from sklearn import preprocessing
from sklearn.model_selection import train_test_split


def Perform_Classification(data, training_vars, target_var, algos, split_ratio=0.2):

    training_vars = data[training_vars]

    results = {}
    fit_data = {}

    target = data[target_var[0]]
    x_train, x_test, y_train, y_test = train_test_split(training_vars, target, test_size=split_ratio)

    training_data = x_train.copy()
    training_data[target_var[0]] = y_train.copy()

    test_data = x_test.copy()
    test_data[target_var[0]] = y_test.copy()

    predicted_data = test_data.copy()


    samples = {}
    algo_results = {}
    for y in algos:

        if 'gausian' in y.lower():
            try:
                algo_name = 'Gausian Naive Bayes'

                params = algos[y]
                #Gausian_Naive_Bayes(x_train, y_train, x_test, priors=None, var_smoothing=1e-09):
                estimated_values = Gausian_Naive_Bayes(x_train, y_train, x_test,

                                                       None, params['var_smoothing'])

                algo_results[algo_name] = Calc_Accuracy(y_test, estimated_values)

                estimated_values = [str(x) for x in list(estimated_values)]

                samples[algo_name] = list(estimated_values)

                predicted_data['Gausian_Naive_Bayes'] = estimated_values
            except:
                raise

        elif 'bernoulli' in y.lower():
            try:
                algo_name = 'Bernoulli Naive Bayes'

                params = algos[y]
                #Bernoulli_Naive_Bayes(x_train, y_train, x_test, alpha=1.0, binarize=0.0, fit_prior=True, class_prior=None):
                estimated_values = Bernoulli_Naive_Bayes(x_train, y_train, x_test,

                                                         params['alpha'], params['binarize'], params['fit_prior'], None)

                algo_results[algo_name] = Calc_Accuracy(y_test, estimated_values)
                estimated_values = [str(x) for x in list(estimated_values)]

                samples[algo_name] = list(estimated_values)
                predicted_data['Bernoulli_Naive_Bayes'] = estimated_values
            except:
                raise

        elif 'linear' in y.lower():
            try:
                algo_name = 'Linear Support Vector Classifier'

                params = algos[y]
                #Linear_SVC(x_train, y_train, x_test, C=1.0, kernel='rbf', degree=3, gamma='auto_deprecated',
                #   coef0=0.0, shrinking=True, probability=False, tol=0.001,
                #   cache_size=200, class_weight=None, verbose=False, max_iter=-1,
                #   decision_function_shape='ovr', random_state=None):

                estimated_values = Linear_SVC(x_train, y_train, x_test,

                                              params['C'], params['kernel'], params['degree'], params['gamma'],
                                              params['coef0'], params['shrinking'], params['probability'],
                                              params['tol'], params['cache_size'], None, params['verbose'],
                                              params['max_iter'], params['decision_function_shape'], params['random_state'])

                algo_results[algo_name] = Calc_Accuracy(y_test, estimated_values)
                estimated_values = [str(x) for x in list(estimated_values)]

                samples[algo_name] = list(estimated_values)
                predicted_data['Linear_Support_Vector_Classifier'] = estimated_values
            except:
                raise

        elif 'support' in y.lower():
            try:
                algo_name = 'Support Vector Classifier'

                params = algos[y]
                # Linear_SVC(x_train, y_train, x_test, C=1.0, kernel='rbf', degree=3, gamma='auto_deprecated',
                #   coef0=0.0, shrinking=True, probability=False, tol=0.001,
                #   cache_size=200, class_weight=None, verbose=False, max_iter=-1,
                #   decision_function_shape='ovr', random_state=None):

                estimated_values = SV_C(x_train, y_train, x_test,

                                              params['C'], params['kernel'], params['degree'], params['gamma'],
                                              params['coef0'], params['shrinking'], params['probability'],
                                              params['tol'], params['cache_size'], None, params['verbose'],
                                              params['max_iter'], params['decision_function_shape'], params['random_state'])

                algo_results[algo_name] = Calc_Accuracy(y_test, estimated_values)
                estimated_values = [str(x) for x in list(estimated_values)]

                samples[algo_name] = list(estimated_values)
                predicted_data['Support_Vector_Classifier'] = estimated_values
            except:
                raise

    try:
        results[target_var[0]] = algo_results
        y_test = [str(x) for x in list(y_test)]
        fit_data[target_var[0]] = {'predicted': samples, 'Actual': list(y_test)}
    except:
        raise


    return results, fit_data, training_data, test_data, predicted_data


def Process_Data_Features(data, training_vars, target_var):
    features_list = []
    try:
        for feature in training_vars:
            features_list.append(Feature_Encoder(data[feature]))

        features = zip(features_list)

        encoded_target = Feature_Encoder(target_var)

        return features, encoded_target
    except:
        raise

def Feature_Encoder(feature):
    try:
        label_encoder = preprocessing.LabelEncoder()
        feature_encoded = label_encoder.fit_transform(feature)

        return feature_encoded
    except:
        raise