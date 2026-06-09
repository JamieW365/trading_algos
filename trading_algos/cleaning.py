import numpy as np
import pandas as pd

def smooth(s: pd.Series,
           window: int = 5,
           min_periods: int = 1,
           method: str = 'median'):
    
    '''
    Smoothing function to be applied to dataset columns
    '''

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
        
def nulls_summary(data = pd.DataFrame):

    '''
    Returns a summary table describing null counts and lengths of consecutive
    null periods
    '''

    def get_nulls(s = pd.Series):
        
        '''
        Captures null values, grouping them by periods of consecutive missing
        values and providing summary statistics
        '''

        # Filter series to periods where data is to be expected, between
        # the first and last data points
        start = s.first_valid_index()
        end = s.last_valid_index()

        if (start == None) | (end == None):
            return np.nan
        
        s_valid = s.loc[start: end].copy()
        
        nulls = s_valid.isna() * 1

        if nulls.sum() == 0:
            return np.nan
        
        # Group consecutive null periods
        nulls_periods =(
            ((nulls.diff().fillna(nulls.iloc[0]) == 1) * 1)\
                .mask(nulls==False,np.nan)\
                    .cumsum())
        
        # Calculate summary statistics for null periods
        stats = nulls_periods.value_counts()\
                    .agg(['count', 'mean', 'max', 'sum']).astype(int)
        
        stats['pct'] = nulls.mean() * 100

        stats.index=['Null Events', 'Avg Duration', 'Max Duration', 'Tot Missing', 'Pct Null']

        return stats.round(2)

    # Gather null statistics for every column
    stats = data.apply(get_nulls)

    # Focus on columns where intermittent nulls exist
    stats = stats[stats.notna()]

    # Format as dataframe
    df_null = pd.DataFrame(stats.tolist(), index=stats.index)

    df_null[df_null.columns[:4]] = df_null[df_null.columns[:4]].astype(int)

    return df_null

def pipeline(data: pd.DataFrame,
             smoothing_window: int=5,
             smoothing_min_periods: int=1,
             smoothing_method: str='median'):

    data = data.copy()

    # Firstly identify possible tickers for smoothing and any tickers
    # as well as any tickers that are too problematic to keep 
    df_nulls = nulls_summary(data)

    # Dropping any tickers that have more than 5% of internal data missing
    # or have atleast one period of 5 or more consecutive missing data points
    problem_tickers = df_nulls[(df_nulls['Max Duration'] > smoothing_window-1) | 
                               (df_nulls['Pct Null'] >= 5)].index.tolist()

    # Remaining tickers with missing data points will be smoothed out with
    # the rolling weekly median
    smooth_tickers = df_nulls.drop(problem_tickers).index.tolist()

    # Smooth the stocks identified for smoothing
    data[smooth_tickers] = data[smooth_tickers].apply(smooth,
                                                      window=smoothing_window,
                                                      min_periods=smoothing_min_periods,
                                                      method=smoothing_method)
    
    return data