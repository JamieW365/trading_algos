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