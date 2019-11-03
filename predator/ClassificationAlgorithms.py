from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier


def Gausian_Naive_Bayes(x_train, y_train, x_test, priors=None, var_smoothing=1e-09):
    try:
        gnb = GaussianNB(priors=priors, var_smoothing=var_smoothing)

        gnb.fit(x_train, y_train)
        y_pred = gnb.predict(x_test)
        return y_pred
    except:
        raise


def Bernoulli_Naive_Bayes(x_train, y_train, x_test, alpha=1.0, binarize=0.0, fit_prior=True, class_prior=None):

    bnb = BernoulliNB(alpha=alpha, binarize=binarize, fit_prior=fit_prior, class_prior=class_prior)
    try:
        bnb.fit(x_train, y_train)
        y_pred = bnb.predict(x_test)
        return y_pred
    except:
        raise


def Ada_Booster(x_train, y_train, x_test, base_estimator=None, n_estimators=50,
                learning_rate=1.0, algorithm='SAMME.R', random_state=None):

    ada_classifier = AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators,
                                        learning_rate=learning_rate, algorithm=algorithm,
                                        random_state=random_state)
    try:
        ada_classifier.fit(x_train, y_train)
        y_pred = ada_classifier.predict(x_test)
        return y_pred
    except:
        raise


def M_Preceptron(x_train, y_train, x_test, hidden_layer_sizes=(100, ), activation='relu', solver='adam',
                        alpha=0.0001, batch_size='auto', learning_rate='constant',
                        learning_rate_init=0.001, power_t=0.5, max_iter=200,
                        shuffle=True, random_state=None, tol=0.0001, verbose=False,
                        warm_start=False, momentum=0.9, nesterovs_momentum=True,
                        early_stopping=False, validation_fraction=0.1,
                        beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10):

    mpc = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver,
                        alpha=alpha, batch_size=batch_size, learning_rate=learning_rate,
                        learning_rate_init=learning_rate_init, power_t=power_t, max_iter=max_iter,
                        shuffle=shuffle, random_state=random_state, tol=tol, verbose=verbose,
                        warm_start=warm_start, momentum=momentum, nesterovs_momentum=nesterovs_momentum,
                        early_stopping=early_stopping, validation_fraction=validation_fraction,
                        beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, n_iter_no_change=n_iter_no_change)

    try:
        mpc.fit(x_train, y_train)
        y_pred = mpc.predict(x_test)
        return y_pred
    except:
        raise


def Decision_Tree(x_train, y_train, x_test, criterion='gini', splitter='best', max_depth=None,
                                 min_samples_split=2, min_samples_leaf=1,
                                 min_weight_fraction_leaf=0.0, max_features=None,
                                 random_state=None, max_leaf_nodes=None,
                                 min_impurity_decrease=0.0,
                                 min_impurity_split=None, class_weight=None, presort=False):

    dtc = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth,
                                 min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                 min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
                                 random_state=random_state, max_leaf_nodes=max_leaf_nodes,
                                 min_impurity_decrease=min_impurity_decrease,
                                 min_impurity_split=min_impurity_split, class_weight=class_weight, presort=presort)
    try:
        dtc.fit(x_train, y_train)
        y_pred = dtc.predict(x_test)
        return y_pred
    except:
        raise


def Random_Forest(x_train, y_train, x_test, n_estimators='warn', criterion='gini', max_depth=None,
                                 min_samples_split=2, min_samples_leaf=1,
                                 min_weight_fraction_leaf=0.0, max_features='auto',
                                 max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,
                                 bootstrap=True, oob_score=False, n_jobs=None, random_state=None,
                                 verbose=0, warm_start=False, class_weight=None):

    rfc = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth,
                                 min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                 min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
                                 max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split,
                                 bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs, random_state=random_state,
                                 verbose=verbose, warm_start=warm_start, class_weight=class_weight)
    try:
        rfc.fit(x_train, y_train)
        y_pred = rfc.predict(x_test)
        return y_pred
    except:
        raise


def Linear_SVC(x_train, y_train, x_test, C=1.0, kernel='linear', degree=3, gamma='auto_deprecated',
               coef0=0.0, shrinking=True, probability=False, tol=0.001,
               cache_size=200, class_weight=None, verbose=False, max_iter=-1,
               decision_function_shape='ovr', random_state=None):

    lsvc = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma,
               coef0=coef0, shrinking=shrinking, probability=probability, tol=tol,
               cache_size=cache_size, class_weight=class_weight, verbose=verbose, max_iter=max_iter,
               decision_function_shape=decision_function_shape, random_state=random_state)
    try:
        lsvc.fit(x_train, y_train)
        y_pred = lsvc.predict(x_test)
        return y_pred
    except:
        raise


def SV_C(x_train, y_train, x_test, C=1.0, kernel='rbf', degree=3, gamma='auto_deprecated',
               coef0=0.0, shrinking=True, probability=False, tol=0.001,
               cache_size=200, class_weight=None, verbose=False, max_iter=-1,
               decision_function_shape='ovr', random_state=None):

    sv = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma,
               coef0=coef0, shrinking=shrinking, probability=probability, tol=tol,
               cache_size=cache_size, class_weight=class_weight, verbose=verbose, max_iter=max_iter,
               decision_function_shape=decision_function_shape, random_state=random_state)

    try:
        sv.fit(x_train,y_train)
        y_pred = sv.predict(x_test)
        return y_pred
    except:
        raise