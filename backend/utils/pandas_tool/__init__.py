from .check_and_read import check_and_read
from .dimensionless_processing import dimensionless_processing
from .scientific_calculation import scientific_calculation
from .one_hot_encoding import one_hot_encoding
from .statistical_summary import statistical_summary
from .hypothesis_tests import normality_test, t_test, f_test, chi_square_test, non_parametric_test
from .text_to_numeric_or_datetime import text_to_numeric_or_datetime
from .correlation_analysis import correlation_analysis
from .linear_regression import linear_regression

__all__ = [
    "check_and_read",
    "dimensionless_processing",
    "scientific_calculation",
    "one_hot_encoding",
    "statistical_summary",
    "normality_test",
    "t_test",
    "f_test",
    "chi_square_test",
    "non_parametric_test",
    "text_to_numeric_or_datetime",
    "correlation_analysis",
    "linear_regression"
]

__author__ = 'github.com/746505972'
