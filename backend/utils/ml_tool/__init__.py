from .logistic_regression import logistic_regression
from .clustering import clustering_analysis
from ._xgboost import xgboost_analysis, xgboost_classification, xgboost_regression
from ._svm import svm_analysis

__all__ = [
    "logistic_regression",
    "clustering_analysis",
    "xgboost_analysis",
    "xgboost_classification",
    "xgboost_regression",
    "svm_analysis"
]

__author__ = 'github.com/746505972'