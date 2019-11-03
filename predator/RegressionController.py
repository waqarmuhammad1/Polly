from RegressionMetrics import *
from RegressionAlgorithms import *
from sklearn.model_selection import train_test_split


def Perform_Regression(data, training_vars, target_vars, algos, test_size=0.2):

    try:
        training_vars = data[training_vars]
        results = {}
        fit_data = {}
        target_var = data[target_vars]
        x_train, x_test, y_train, y_test = train_test_split(training_vars, target_var, test_size=test_size)

        training_data = x_train.copy()
        training_data[target_vars[0]] = y_train.copy()

        test_data = x_test.copy()
        test_data[target_vars[0]] = y_test.copy()

        predicted_data = test_data.copy()
    except:
        raise

    samples = {}
    algo_results = {}
    for y in algos:

        if 'linear' in y.lower():
            try:
                algo_name = 'Linear Regression'

                params = algos[y]
                #(X_train, y_train, X_test, fit_intercept=True, normalize=False, copy_X=True, n_jobs=None)

                estimated_values = linear_reg(x_train, y_train, x_test,

                                              params['fit_intercept'], params['normalize'],
                                              params['copy_X'], params['n_jobs'])

                algo_results[algo_name] = calc_metrics(estimated_values, y_test)
                samples[algo_name] = list(estimated_values)
                predicted_data['Linear_Regression'] = list(estimated_values)
            except:
                raise

        elif 'elastic' in y.lower():
            try:
                params = algos[y]
                #(X_train, y_train, X_test, alpha=1.0, l1_ratio=0.5, fit_intercept=True,
                #normalize=False, precompute=False, max_iter=1000,
                #copy_X=True, tol=0.0001, warm_start=False,
                #positive=False, random_state=None, selection='cyclic'):

                algo_name = 'Elastic Net Regression'

                estimated_values = elastic_reg(x_train, y_train, x_test, params['alpha'],
                                               params['l1_ratio'], params['fit_intercept'],
                                               params['normalize'], params['precompute'],
                                               params['max_iter'], params['copy_X'], params['tol'],
                                               params['warm_start'], params['positive'],
                                               params['random_state'], params['selection'])

                algo_results[algo_name] = calc_metrics(estimated_values, y_test)
                samples[algo_name] = list(estimated_values)
                predicted_data['Elastic_Regression'] = list(estimated_values)
            except:
                raise

        elif 'lars' in y.lower() and 'lasso' not in y.lower():
            try:
                params = algos[y]
                algo_name = 'Lars Regression'

                #X_train, y_train, X_test, fit_intercept=True, verbose=False, normalize=True,
                #precompute='auto', n_nonzero_coefs=500,
                #eps=2.220446049250313e-16, copy_X=True,
                #fit_path=True, positive=False
                estimated_values = lars_reg(x_train, y_train, x_test, params['fit_intercept'],
                                            params['verbose'], params['normalize'], params['precompute'],
                                            params['n_nonzero_coefs'], params['eps'],
                                            params['copy_X'], params['fit_path'], params['positive'])

                algo_results[algo_name] = calc_metrics(estimated_values, y_test)
                samples[algo_name] = list(estimated_values)
                predicted_data['Lars_Regression'] = list(estimated_values)
            except:
                raise

        elif 'lasso' in y.lower() and 'lars' not in y.lower():
            try:
                params = algos[y]
                #X_train, y_train, X_test, alpha=1.0, fit_intercept=True, normalize=False,
                #precompute=False, copy_X=True, max_iter=1000,
                #tol=0.0001, warm_start=False, positive=False,
                #random_state=None, selection='cyclic'

                algo_name = 'Lasso Regression'


                estimated_values = lasso_reg(x_train, y_train, x_test, params['alpha'],
                                             params['fit_intercept'], params['normalize'],
                                             params['precompute'], params['copy_X'], params['max_iter'],
                                             params['tol'], params['warm_start'], params['positive'],
                                             params['random_state'], params['selection'])

                algo_results[algo_name] = calc_metrics(estimated_values, y_test)
                samples[algo_name] = list(estimated_values)
                predicted_data['Lasso_Regression'] = list(estimated_values)
            except:
                raise

        elif 'lassolars' in y.lower():
            try:
                params = algos[y]
                #X_train, y_train, X_test, alpha=1.0, fit_intercept=True,
                #verbose=False, normalize=True,
                #precompute='auto', max_iter=500,
                #eps=2.220446049250313e-16, copy_X=True,
                #fit_path=True, positive=False

                algo_name = 'LassoLars Regression'

                estimated_values = lasso_lars_reg(x_train, y_train, x_test, params['alpha'],
                                                  params['fit_intercept'], params['verbose'],
                                                  params['normalize'], params['precompute'], params['max_iter'],
                                                  params['eps'], params['copy_X'], params['fit_path'], params['positive'])

                algo_results[algo_name] = calc_metrics(estimated_values, y_test)
                samples[algo_name] = list(estimated_values)
                predicted_data['LassoLars_Regression'] = list(estimated_values)
            except:
                raise

    try:
        results[target_vars[0]] = algo_results
        fit_data[target_vars[0]] = {'predicted': samples, 'Actual': list(y_test[target_vars[0]])}
        return results, fit_data, training_data, test_data, predicted_data
    except:
        raise

