import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
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
    
def calc_sp500_survivors(get_latest: bool = False,
                         start_date: str  = '1900',
                         end_date:   str  = datetime.today().strftime('%Y-%m-%d')):

    # The following nested functions will be used to mask any date where 
    # stocks are not to be included in the S&P500 timeline due to being
    # either added beyond the given start date, or removed before the
    # given end date.

    # Mask removed stocks
    def filter_removed(ticker):
        if ticker in df_stocks.columns.get_level_values(1).unique():
            df_stocks.loc[:, pd.IndexSlice[: ,ticker]] = df_stocks.loc[:, pd.IndexSlice[: ,ticker]].reindex(pd.date_range(start_date, df_removed[df_removed['Ticker']==ticker].index[0], freq='B'))
    # Mask added stocks
    def filter_added(ticker):
        if ticker in df_stocks.columns.get_level_values(1).unique():
            df_stocks.loc[:, pd.IndexSlice[: ,ticker]] = df_stocks.loc[:, pd.IndexSlice[: ,ticker]].reindex(pd.date_range(df_added[df_added['Symbol']==ticker].index[0], end_date, freq='B'))

    # Load S&P Metadata from Wikipedia or local repo
    df_current, df_changes = get_sp500_meta(get_latest=get_latest)

    # Identify the stocks that have been added to the S&P500 within the
    # selected date range.
    df_added = df_current[(end_date >= df_current.index) & 
                          (df_current.index >= start_date)].copy()
    
    # Identify the stocks that have been removed from the S&P500 within
    # the selected date range.

    df_removed = df_changes['Removed'][(end_date >= df_changes.index) &
                                       (df_changes.index >= start_date)].copy()
    # Sometimes spin-off stocks will be temporarily added to the S&P500
    # without removing any other stocks. This is to ensure that there 
    # are no immediate changes in index holding. As a result there may 
    # be some null entries in the removed table which can be ignored.
    df_removed.dropna(inplace=True)

    # The total list of stocks that have been included in the S&P500
    # at any point within the selected date range
    stocks = df_current['Symbol'].tolist() + df_removed['Ticker'].tolist()

    # Load the latest stock data from yFinance or from local repo
    # May error if local data does not exist or yFinance is having
    # issues
    try:
        df_stocks = load_data(filename=None if get_latest else 'sap500alltime.csv' ,
                              tickers=stocks,
                              start_date=start_date,
                              end_date=end_date)
        # Default all dtypes to float to prevent any issues in masking
        df_stocks = df_stocks.astype(float)
        
        print('data loaded')
    # If local file does not exist then recommend that the user run with
    # get_latest set to True
    except Exception as err:
        raise err
    
    for ticker in df_removed['Ticker']:
        filter_removed(ticker)
    for ticker in df_added['Symbol']:
        filter_added(ticker)

    # Save to local repo for easier access in testing
    save_data(df_stocks,
              'sap500alltimesurvivors.csv')
    
    return df_stocks

def get_sp500(get_latest: bool = False,
              survivors:  bool = True,
              start_date: str  = '1900',
              end_date:   str  = datetime.today().strftime('%Y-%m-%d')):

    if get_latest:
        df_stocks = load_data(stocklist,
                                   start_date=start,
                                   end_date=end)

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

def load_data(tickers:     list = None,
              start_date:  str  = '1900',
              end_date:    str  = datetime.today().strftime('%Y-%m-%d'),
              columns:     list = None,
              auto_adjust: bool = True,
              filename:    str  = None,
              filepath:    str  = tac.RAW_DATA_DIR,
              usecols           = None):
    
    '''
    This function downloads stock data from either a local source or
    yfinance in a way that is consistent for use throughout the
    trading_algos repository.

    Parameters
        tickers (str, list)
            List of tickers to download.

        start (str)
            Download start date string (YYYY-MM-DD) or _datetime,
            inclusive. Default is 1900-01-01.
            E.g. for start='2020-01-01', the first data point will be on
            '2020-01-01'

        end (str)
            Download end date string (YYYY-MM-DD) or _datetime,
            exclusive. Default is now.

        columns (str, iterable)
            Columns to be included in the output. All columns are
            returned by default. 

    '''
    if columns:
        # Ensure that the correct type is passed for columns
        if not isinstance(columns, (list, str, tuple)):
            raise Exception('Invalid data type for: columns')

        # Allow for different types to be passed into columns and use
        # the appropriate method to conver them into a list
        if type(columns) != list:
            match columns:
                case str():
                    columns = [columns]
                case tuple():
                    columns = list(columns)

    # Load data from a previously saved file
    if filename != None:
        if tickers or columns:

            if not tickers:
                tickers = slice(None)
            if not columns:
                columns = slice(None)

            # Load headers from csv file
            headers = pd.read_csv(filepath/filename, index_col=0, header=[0,1], nrows=0)
            # Store column headers as a multi-index
            mi = headers.columns
            # Ignore any stocks that arent included in the data file
            avail_stocks = [x for x in tickers if x in set(mi.get_level_values(1))]
            # Identifying column positions of selected stocks
            positions = mi.get_locs([columns, avail_stocks])
            # Ensure that file structure is maintained on load
            positions = np.sort(positions)
            # Add 1 to positions to account for index loading
            usecols = [0] + (positions + 1).tolist()

            # All stock data should be saved in the default format for
            # standard use throughout the project
            df_stocks = pd.read_csv(filepath/filename,
                                    index_col=0,
                                    skiprows=2,
                                    usecols=usecols)
            
            # Ensure that column names are preserved
            df_stocks.columns = mi[positions]

            # Ensure that datetime index is preserved
            df_stocks.index = pd.to_datetime(df_stocks.index)

            # Filter data between given start and end date
            df_stocks = df_stocks.loc[start_date:end_date]

            return df_stocks

        # All stock data should be saved in the default format for
        # standard use throughout the project
        df_stocks = pd.read_csv(filepath/filename,
                                header=[0,1],
                                index_col=0,
                                usecols=usecols)
        # Ensure that datetime index is preserved
        df_stocks.index = pd.to_datetime(df_stocks.index)
        if columns:
            df_stocks = df_stocks[columns]

        return df_stocks.loc[start_date:end_date]
        
    # Otherwise load fresh stock data from Yahoo Finance
    else:
        if columns:
            df_stocks = yf.download(tickers, 
                                    start=start_date, 
                                    end=end_date, 
                                    auto_adjust=auto)[columns]
        else:
            df_stocks = yf.download(tickers,
                                    start=start_date,
                                    end=end_date,
                                    auto_adjust=auto_adjust)
            
        # If auto_adjust is True then Adj Close should not be returned
        # Close will contain adjusted close prices by default
        if auto_adjust and 'Adj Close' in df_stocks.columns:
            df_stocks.drop('Adj Close', axis=1, inplace=True)

        return df_stocks

def save_data(data: pd.DataFrame,
              filename: str,
              filepath: str=tac.RAW_DATA_DIR):
    
    data.to_csv(filepath/filename)