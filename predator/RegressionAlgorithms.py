import numpy as np
from sklearn.linear_model import LinearRegression, ElasticNet, Lars, Lasso, LassoLars


def linear_reg(X_train, y_train, X_test, fit_intercept=True,
               normalize=False, copy_X=True, n_jobs=None):

    linreg = LinearRegression(fit_intercept=fit_intercept,
                              normalize=normalize, copy_X=copy_X, n_jobs=n_jobs)

    try:
        linreg.fit(X_train, y_train)
        y_pred = linreg.predict(X_test)
        pred_redef = y_pred
        if type(y_pred[0]) is np.ndarray:
            pred_redef = []
            for x in y_pred:
                pred_redef.append(x[0])
            pred_redef = np.array(pred_redef)

        return pred_redef
    except:
        raise


def elastic_reg(X_train, y_train, X_test, alpha=1.0, l1_ratio=0.5, fit_intercept=True,
                       normalize=False, precompute=False, max_iter=1000,
                       copy_X=True, tol=0.0001, warm_start=False,
                       positive=False, random_state=None, selection='cyclic'):

    e_reg = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=fit_intercept,
                       normalize=normalize, precompute=precompute, max_iter=max_iter,
                       copy_X=copy_X, tol=tol, warm_start=warm_start,
                       positive=positive, random_state=random_state, selection=selection)
    try:
        e_reg.fit(X_train, y_train)
        y_pred = e_reg.predict(X_test)
        return y_pred
    except:
        raise




def lars_reg(X_train, y_train, X_test, fit_intercept=True, verbose=False, normalize=True,
                    precompute='auto', n_nonzero_coefs=500,
                    eps=2.220446049250313e-16, copy_X=True,
                    fit_path=True, positive=False):

    lars_reg = Lars(fit_intercept=fit_intercept, verbose=verbose, normalize=normalize,
                    precompute=precompute, n_nonzero_coefs=n_nonzero_coefs,
                    eps=eps, copy_X=copy_X,
                    fit_path=fit_path, positive=positive)

    try:
        lars_reg.fit(X_train, y_train)
        y_pred = lars_reg.predict(X_test)
        return y_pred
    except:
        raise



def lasso_reg(X_train, y_train, X_test, alpha=1.0, fit_intercept=True, normalize=False,
                      precompute=False, copy_X=True, max_iter=1000,
                      tol=0.0001, warm_start=False, positive=False,
                      random_state=None, selection='cyclic'):

    lasso_reg = Lasso(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize,
                      precompute=precompute, copy_X=copy_X, max_iter=max_iter,
                      tol=tol, warm_start=warm_start, positive=positive,
                      random_state=random_state, selection=selection)

    try:
        lasso_reg.fit(X_train, y_train)
        y_pred = lasso_reg.predict(X_test)
        return y_pred
    except:
        raise


def lasso_lars_reg(X_train, y_train, X_test, alpha=1.0, fit_intercept=True,
                               verbose=False, normalize=True,
                               precompute='auto', max_iter=500,
                               eps=2.220446049250313e-16, copy_X=True,
                               fit_path=True, positive=False):

    least_lars_reg = LassoLars(alpha=alpha, fit_intercept=fit_intercept,
                               verbose=verbose, normalize=normalize,
                               precompute=precompute, max_iter=max_iter,
                               eps=eps, copy_X=copy_X,
                               fit_path=fit_path, positive=positive)

    try:
        least_lars_reg.fit(X_train, y_train)
        y_pred = least_lars_reg.predict(X_test)
        return y_pred
    except:
        raise


