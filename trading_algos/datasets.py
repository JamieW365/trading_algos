import yfinance as yf
import pandas as pd
import numpy as np
# import random
import warnings

from trading_algos import config as tac

def get_sp500_meta(get_latest:       bool = False,
                   meta_table:       str  = 'full',
                   curr_path:        str  = tac.EXTERNAL_DATA_DIR,
                   curr_filename:    str  = 'sp500_current.csv',
                   changes_path:     str  = tac.EXTERNAL_DATA_DIR,
                   changes_filename: str  = 'sp500_changes.csv'):

    '''
    Returns the current S&P 500 metadata from Wikipedia detailing the
    following information for each security:

        Symbol (ticker)
        Security (full name)
        GICS Sector (security industry)
        GICS Sub-Industry (security sub-industry)
        Headquarters Location
        Date added (most recent date added to the index)
        CIK (unique identifier)
        Founded (year founded)
    
    Note: 
        This is not the most ideal way to retrieve this information.
        New attempts to read the data via URL may fail for many reasons,
        including: server side issues, blocks to API calls, website
        changes etc. However, without utilising a paid-for API, it will
        provide enough functionality to serve it's purpose.

    Parameters:
        get_latest (default = False)
            When True this will make a URL call to Wikipedia to retrieve
                the most up to date information available.
            When False this will load the latest available information
                from a saved data source.
    '''
    
    curr_filepath = curr_path/curr_filename
    changes_filepath = changes_path/changes_filename

    if get_latest:
        # Attempt to load the latest metadata from Wikipedia
        # This may fail for a number of reasons, such as website change,
        # server unavailability, etc.
        try:
            wiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                                storage_options={'User-Agent': 'pandas'},
                                index_col=0)
            
            # The first wiki table contains the current S&P 500 metadata
            df_current_meta = wiki[0].copy()
            df_current_meta.reset_index(inplace=True)
            df_current_meta['Date added'] = pd.to_datetime(df_current_meta['Date added'])         
            df_current_meta.set_index(df_current_meta['Date added'], inplace=True)
            df_current_meta.sort_index(inplace=True)
            df_current_meta.drop('Date added', axis=1, inplace=True)

            # Save metadata locally so that wikipedia calls can be
            # avoided as much as possible
            df_current_meta.to_csv(curr_filepath)
            
            # The second wiki table contains an extensive list of stocks
            # that were once included in the S&P500 but have been
            # removed
            df_changes_meta = wiki[1].copy()
            df_changes_meta.index = pd.DatetimeIndex(df_changes_meta.index)
            df_changes_meta.sort_index(inplace=True)
            
            # Save metadata locally so that wikipedia calls can be
            # avoided as much as possible
            df_changes_meta.to_csv(changes_filepath)

        # If Wikipedia call fails then attempt to load the latest
        # metadata from saved memory as backup
        except Exception as err:    
            raise Exception(err)
              
    try:
        match meta_table:
            case 'current':
                return pd.read_csv(curr_filepath, index_col=0)
            case 'past':
                return pd.read_csv(changes_filepath, index_col=0, header=[0,1])
            case _:
                return pd.read_csv(curr_filepath, index_col=0), \
                       pd.read_csv(changes_filepath, index_col=0, header=[0,1])
                    
    except Exception as err:
        raise Exception(err)
    
def calc_sp500_survivors(get_latest: bool = True):

    df_current, df_changes = get_sp500_meta(get_latest=get_latest)
    df_changes_added = df_changes['Added'].copy()
    df_changes_removed = df_changes['Removed'].copy()



    return df_current, df_changes

def get_sp500(get_latest: bool = False):

    if get_latest:
        return calc_sp500_survivors(get_latest=get_latest)

    else:
        try:
            pass
        except:
            pass

    pass

def get_sp500_tickers(get_latest: bool=False):

    '''
    Returns the up to date list of stocks currently in the S&P 500 from
    Wikipedia
    '''

    return get_sp500_meta(get_latest=get_latest, meta_table='current').index.tolist()

def load_data(tickers: list=None,
              file: str=None,
              filepath: str=tac.RAW_DATA_DIR,
              start_date: None = None,
              end_date: None = None,
              columns: list = ['Close']):
    
    '''
    This function downloads stock data from yfinance in a way that is
    consistent for use throughout the trading_algos repository
    '''

    if file != None:
        df_stocks = pd.read_csv(filepath/file,
                                header=[0,1],
                                index_col=0)
        df_stocks.index = pd.to_datetime(df_stocks.index)
    else:
        df_stocks = yf.download(tickers, start=start_date, end=end_date)[columns]
        
    return df_stocks