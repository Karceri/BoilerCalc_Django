import math, numpy as np


def handle_zero_division(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except:
            return np.nan
    return wrapper