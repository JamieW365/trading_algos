import yfinance as yf
import pandas as pd
import numpy as np
import random
import warnings

def select_n(n: int=5,
             stocks: list=[],
             seed: int=None):
    '''
    Choose n stocks from a given list
    '''

    # Set the seed for repeatability
    if type(seed)==int:
        random.seed(seed)

    return random.sample(stocks, n)

def calculate_weights(df_stocks,
                      method: str='EWP'):

    '''
    Return weights matrix for a given portfolio of stocks
    '''

    # Run weighting calculations dependent on the selected methodology
    match method:
        # Equal Weighted Portfolio
        case 'EWP':
            # Each asset is given a weight of 1/N for N assets
            num_assets = len(df_stocks.Close.columns)
            weights = np.array([1] * num_assets) / num_assets

        # ValueError if an invalid methodology is into the function
        case _:
            raise ValueError(f'{method} an invalid weighting method, input a pre-defined weighting methodology.')

    return weights