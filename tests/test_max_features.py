import pandas as pd


def compute_metric(parameter_max_features, X):
    parameter_max_features_metric = parameter_max_features
    if parameter_max_features == 'all':
        parameter_max_features = None
        parameter_max_features_metric = X.shape[1]
    return parameter_max_features_metric


def test_metric_all():
    X = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    assert compute_metric('all', X) == X.shape[1]


def test_metric_sqrt():
    X = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    assert compute_metric('sqrt', X) == 'sqrt'
