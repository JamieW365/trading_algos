import numpy as np

def calc_returns(df_stocks):

    '''
    Take stock price data and generate a returns table
    '''

    df_returns = df_stocks.Close.pct_change().dropna()

    return df_returns