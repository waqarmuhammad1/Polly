
def Get_Regression_Algo_Params():

    algo_params = {}

    algo_params['Linear Regression'] = 'fit_intercept=True|bool|,\
               normalize=False|bool|, copy_X=True|bool|, n_jobs=None|int/None|'

    algo_params['Elastic Regression'] = 'alpha=1.0|float|, l1_ratio=0.5|float|, fit_intercept=True|bool|,\
                       normalize=False|bool|, precompute=False|bool|, max_iter=1000|int|,\
                       copy_X=True|bool|, tol=0.0001|float|, warm_start=False|bool|,\
                       positive=False|bool|, random_state=None|int/None|, selection="cyclic"|string|'

    algo_params['Lasso Regression'] = 'alpha=1.0|float|, fit_intercept=True|bool|, normalize=False|bool|,\
                      precompute=False|bool|, copy_X=True|bool|, max_iter=1000|int|,\
                      tol=0.0001|float|, warm_start=False|bool|, positive=False|bool|,\
                      random_state=None|int/None|, selection="cyclic"|string|'

    algo_params['Lars Regression'] = 'fit_intercept=True|bool|, verbose=False|bool|, normalize=True|bool|,\
                    precompute="auto"|bool/auto/array|, n_nonzero_coefs=500|int|,\
                    eps=2.220446049250313e-16|float|, copy_X=True|bool|,\
                    fit_path=True|bool|, positive=False|bool|'

    algo_params['LassoLars Regression'] = 'alpha=1.0|float|, fit_intercept=True|bool|,\
                               verbose=False|bool|, normalize=True|bool|,\
                               precompute="auto"|bool/auto/array|, max_iter=500|int|,\
                               eps=2.220446049250313e-16|float|, copy_X=True|bool|,\
                               fit_path=True|bool|, positive=False|bool|'

    return algo_params