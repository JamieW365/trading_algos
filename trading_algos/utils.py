import numpy as np

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