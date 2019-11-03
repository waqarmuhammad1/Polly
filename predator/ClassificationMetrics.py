import json
from sklearn import metrics


def Calc_Accuracy(y_test, y_pred):
    try:
        return json.dumps({'Accuracy': metrics.accuracy_score(y_test, y_pred) * 100})
    except:
        raise