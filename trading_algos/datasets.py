import yfinance as yf
import pandas as pd
import numpy as np
# import random
import warnings

def get_sp500_meta(get_latest: bool=False):

    '''
    Returns the current S&P 500 metadata from Wikipedia detailing the following information for each security:

        Symbol (ticker)
        Security (full name)
        GICS Sector (security industry)
        GICS Sub-Industry (security sub-industry)
        Headquarters Location
        Date added (most recent date added to the index)
        CIK (unique identifier)
        Founded (year founded)
    
    Note: 
        This is not the most ideal way to retrieve this information. New attempts to read the data via URL
        may fail for many reasons, including: server side issues, blocks to API calls, website changes etc.
        However, without utilising a paid-for API, it will provide enough functionality to serve it's purpose.

    Parameters:
        get_latest (default = False)
            When True this will make a URL call to Wikipedia to retrieve the most up to date information available.
            When False this will load the latest available information from a saved data source.
    '''

    # Make a new call to Wikipedia to retrieve the latest S&P metadata
    if get_latest:
        # Attempt to retrieve the latest S&P information from Wikipedia. There is always a chance that this
        # will fail. Catch any error and fallback on loading saved data if necessary.
        try:
            wiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                                storage_options={'User-Agent': 'pandas'},
                                index_col=0)
            df_current = wiki[0]
            df_current.to_csv('/home/jamie/code/JamieW365/trading_algos/src/datasets/data/sp500_components.csv')
        # If pandas fails to read data from Wikipedia for any reason then revert to loading the latest available saved data
        except Exception as err:
            # Attempt to load the latest S&P information from the latest available saved data
            try:
                df_current = pd.read_csv('/home/jamie/code/JamieW365/trading_algos/src/datasets/data/sp500_components.csv', index_col=0)
            # If unable to load saved data then we must error at this point
            except:
                raise Exception(err)
    # Attempt to load the latest S&P information from the latest available saved data
    else:
        # Attempt to load the latest S&P information from the latest available saved data
        try:
            df_current = pd.read_csv('/home/jamie/code/JamieW365/trading_algos/src/datasets/data/sp500_components.csv', index_col=0)
        # If unable to load saved data then we must error at this point
        except:
            raise Exception(err)
            
    return df_current

def get_sp500_tickers(get_latest: bool=False):

    '''
    Returns the up to date list of stocks currently in the S&P 500 from Wikipedia
    '''

    return get_sp500_meta(get_latest = get_latest).index.tolist()

def load_data(tickers,
              start_date: None = None,
              end_date: None = None,
              columns: list = ['Close']):
    
    '''
    This function downloads stock data from yfinance in a way that is consistent for use throughout the trading_algos
    repository
    '''

    df_stocks = yf.download(tickers, start=start_date, end=end_date)[columns]


    return df_stocks