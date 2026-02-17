import yfinance as yf
import pandas as pd
import numpy as np

def get_sp500_components():
    '''
    Returns the up to date list of stocks currently in the S&P 500 from Wikipedia
    '''

    wiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                        storage_options={'User-Agent': 'pandas'},
                        index_col=0)
    
    df_current = wiki[0]

    df_current.to_csv('/home/jamie/code/JamieW365/trading_algos/src/datasets/data/sp500_components.csv')

    return df_current
