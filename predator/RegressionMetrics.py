import json
import numpy as np
from sklearn import metrics


def filter_nan(s, o):
    try:
        data = np.array([s.flatten(), o.flatten()])
        data = np.transpose(data)
        data = data[~np.isnan(data).any(1)]
        return data[:, 0], data[:, 1]
    except:
        raise


def calc_nash(s, o):
    try:
        s, o = filter_nan(s, o)
        return 1 - sum((s - o) ** 2) / sum((o - np.mean(o)) ** 2)
    except:
        raise


def calc_metrics(y_pred, y_test):
    try:
        rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
        nash = calc_nash(y_pred, y_test.values)
        rel_rmse = 100 * (rmse / np.mean(y_test))
        return json.dumps({'RMSE': str(rmse), 'RMSE%': str(rel_rmse[0]), 'Nash': (nash)})
    except:
        raise

