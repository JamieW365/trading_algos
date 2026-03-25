import numpy as np
import pandas as pd

def calc_returns(df_stocks):

    '''
    Take stock price data and generate a returns table
    '''

    df_returns = df_stocks.Close.pct_change().dropna()

    return df_returns

def get_returns_summary(data,
                        annualize: bool=True,
                        ann_trading_periods: int=252,
                        risk_free_return: float=0.0):

    '''
    Generate an asset returns summary table
    '''

    # Aggregate calculations on returns data at a trading period level
    df_summary = data.agg(['mean', 'std']).T
    df_summary.columns = ['Return', 'Risk']

    # Summary statistics are most commonly reviewed in annual terms
    # Convert trading period statistics to annual statistics here
    if annualize:
        df_summary['Return'] *= ann_trading_periods
        df_summary['Risk'] *= np.sqrt(ann_trading_periods)

    # Sharpe ratio is a measure of asset risk versus return
    # We may take into account the returns of a 'risk free' asset, generally something like government bonds
    df_summary['Sharpe'] = (df_summary['Return'] - risk_free_return) / df_summary['Risk']
    df_summary

    return df_summary

def stock_slice(data: pd.DataFrame = pd.DataFrame(),
                ticker: str = None):
    
    _df = data.copy()
    return _df.loc[:, pd.IndexSlice[: ,ticker]]

def head_tail(data: pd.DataFrame = pd.DataFrame(),
              n:    int          = 3):
    
    '''
    Returns both the head and tail of a dataframe at the same time
    '''

    if data.empty:
        return
    
    _df_ht = pd.concat([data.head(n), data.tail(n)])

    return _df_ht

    # This code adds a divider to the output, making it clear where the
    # head and tail is. Some work needs to be done to improve the 
    # formatting
    # mid = len(_df_ht) // 2  # middle row index

    # styled = _df_ht.style.format_index(lambda x: x.strftime('%Y-%m-%d')).set_table_styles([
    #     {
    #         'selector': f'tr:nth-child({mid + 1}) th, tr:nth-child({mid + 1}) td',
    #         'props': [('border-top', '2px solid black')]
    #     }
    # ], overwrite=False)

    # return styled