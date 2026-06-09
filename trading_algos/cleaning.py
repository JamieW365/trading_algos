import numpy as np
import pandas as pd

def smooth(s: pd.Series,
           window: int = 5,
           min_periods: int = 1,
           method: str = 'median'):

    start = s.first_valid_index()
    end = s.last_valid_index()
    s_valid = s.loc[start: end].copy()

    match method:
        case 'median':
            return s_valid.fillna(
                s_valid.rolling(window=window, min_periods=min_periods).median())
        case 'mean':
            return s_valid.fillna(
                s_valid.rolling(window=window, min_periods=min_periods).mean())
        case 'min':
            return s_valid.fillna(
                s_valid.rolling(window=window, min_periods=min_periods).min())
        case 'max':
            return s_valid.fillna(
                s_valid.rolling(window=window, min_periods=min_periods).max())