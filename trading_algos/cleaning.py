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

def identify_spikes(data: pd.DataFrame,
                    data_format: str='normprice'):
    
    '''
    Identifies and produces a summary of extreme price movements for
    every ticker
    '''

    data = data.copy()

    # If standard price data is passed in then convert into daily log returns
    if data_format == 'normprice':
        data = np.log(data) - np.log(data).shift(1)
    else:
        raise ValueError(f'{data_format} an invalid format')
    
    # Abnormaly large price changes directly both preceded and followed by
    # comparatively small price movements.
    isolated_spikes = (
        # Abnormaly large daily change (> 170%)
        abs(data > 1).mask(data.isna(), np.nan) &
        # Followed by a comparatively smally daily change (< 10.5%)
        (abs(data.shift(1) < 0.1).mask(data.isna(), np.nan) &
        # Preceded by a comparitively small daily change (< 10.5%)
        abs(data.shift(-1) < 0.1).mask(data.isna(), np.nan))
        ).sum()

    # Abnormaly large price changes followed directly by an abnormaly large
    # reversal.
    reversal_spikes = (
        (((data > 1) & (data.shift(1) < -1)) | 
        ((data < 1) & (data.shift(1) > 1)))
    ).sum()

    # Identifying all abnormal price movements that deviate enourmously
    # from the monthly median price
    rolling_med = data.rolling(21).median()
    residual_spikes = (abs(data - rolling_med) > 2).sum()

    problem_counts = pd.concat(
        [isolated_spikes[isolated_spikes!=0],
        reversal_spikes[reversal_spikes!=0],
        residual_spikes[residual_spikes!=0]], 
        axis=1)\
            .fillna(0)\
                .astype(int)

    problem_counts.columns = ['Isolated Spikes', 'Spike Reversals', 'Extreme Price Movements']
    return problem_counts


def pipeline(data: pd.DataFrame,
             smoothing_window: int=5,
             smoothing_min_periods: int=1,
             smoothing_method: str='median'):

    data = data.copy()

    # Firstly identify possible tickers for smoothing and any tickers
    # as well as any tickers that are too problematic to keep 
    df_nulls = nulls_summary(data.Close)

    # Dropping any tickers that have more than 5% of internal data missing
    # or have atleast one period of 5 or more consecutive missing data points
    problem_tickers = df_nulls[(df_nulls['Max Duration'] > smoothing_window-1) | 
                               (df_nulls['Pct Null'] >= 5)].index.tolist()

    # Remaining tickers with missing data points will be smoothed out with
    # the rolling weekly median
    smooth_tickers = df_nulls.drop(problem_tickers).index.tolist()
    print('smoothing:', smooth_tickers)
    # Smooth the stocks identified for smoothing
    data.loc[:, pd.IndexSlice[:, smooth_tickers]] = \
        data.loc[:, pd.IndexSlice[:, smooth_tickers]]\
            .apply(smooth,
                   window=smoothing_window,
                   min_periods=smoothing_min_periods,
                   method=smoothing_method)
    
    # After smoothing, identify stocks with extreme price movements
    # We may look to smooth stocks with limited extremes, replacing spikes
    # by the median, for now I will simply drop any potentially problematic
    # stocks
    # Dropping any tickers that have extreme price movements
    problem_tickers += identify_spikes(data.Close).index.tolist()
    problem_tickers = list(set(problem_tickers))
    print('dropping', problem_tickers)
    # Remove any problematic stocks from the dataset
    data = data.drop(problem_tickers, axis=1, level=1)

    # Return cleaned dataset
    return data