def Get_Classification_Params():

    algo_params = {}

    algo_params['Gausian Naive Bayes'] = 'priors=None|None|, var_smoothing=1e-09|float|'
    algo_params['Bernoulli Naive Bayes'] = 'alpha=1.0|float|, binarize=0.0|float/None|, fit_prior=True|bool|, class_prior=None|None|'

    algo_params['Ada Booster'] = 'base_estimator=None|None|, n_estimators=50|int|,\
                learning_rate=1.0|float|, algorithm=SAMME.R|string|, random_state=None|int/None|'

    # algo_params['Multi Layer Preceptron'] = 'hidden_layer_sizes=(100, ), activation=relu, solver=adam,\
    #                     alpha=0.0001, batch_size=auto, learning_rate=constant,\
    #                     learning_rate_init=0.001, power_t=0.5, max_iter=200,\
    #                     shuffle=True, random_state=None, tol=0.0001, verbose=False,\
    #                     warm_start=False, momentum=0.9, nesterovs_momentum=True,\
    #                     early_stopping=False, validation_fraction=0.1,\
    #                     beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10'

    algo_params['Decision Tree'] = 'criterion=gini|string|, splitter=best|string|, max_depth=None|int/None|,\
                                 min_samples_split=2|int/float|, min_samples_leaf=1|int/float|,\
                                 min_weight_fraction_leaf=0.0|float|, max_features=None|int/float/string/None|,\
                                 random_state=None|int/None|, max_leaf_nodes=None|int/None|,\
                                 min_impurity_decrease=0.0|float|,\
                                 min_impurity_split=None|float|, class_weight=None|string/None|, presort=False|bool|'

    algo_params['Random Forest'] = 'n_estimators=warn|int|, criterion=gini|string|, max_depth=None|int/None|,\
                                 min_samples_split=2|int/float|, min_samples_leaf=1|int/float|,\
                                 min_weight_fraction_leaf=0.0|float|, max_features=auto|int/string/float/None|,\
                                 max_leaf_nodes=None|int/None|, min_impurity_decrease=0.0|float|, min_impurity_split=None|float|,\
                                 bootstrap=True|bool|, oob_score=False|bool|, n_jobs=None|int/None|, random_state=None|int/None|,\
                                 verbose=0|int|, warm_start=False|bool|, class_weight=None|string/None|'

    algo_params['Linear SVC'] = 'C=1.0|float|, kernel=linear|string|, degree=3|int|, gamma=auto_deprecated|float|,\
               coef0=0.0|float|, shrinking=True|bool|, probability=False|bool|, tol=0.001|float|,\
               cache_size=200|float|, class_weight=None|string/None|, verbose=False|bool|, max_iter=-1|int|,\
               decision_function_shape=ovr|string|, random_state=None|int|'

    algo_params['Support Vector'] = 'C=1.0|float|, kernel=rbf|string|, degree=3|int|, gamma=auto_deprecated|float|,\
               coef0=0.0|float|, shrinking=True|bool|, probability=False|bool|, tol=0.001|float|,\
               cache_size=200|float|, class_weight=None|string/None|, verbose=False|bool|, max_iter=-1|int|,\
               decision_function_shape=ovr|string|, random_state=None|int|'

    return algo_params