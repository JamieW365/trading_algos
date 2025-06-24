import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

def plot_windows(df,
                     close_col: str = 'Close',
                     short_col: str = 'sma_short',
                     long_col: str = 'sma_long',
                     short_window = ' Short',
                     long_window = ' Long'):

    """
    Generates a plot highlighting the selected moving averages and how they interact alongside price data

        df : 
            DataFrame containing price

        close_col :
            The column in the given DataFrame (df) that contains closing price data.

        short_col :
            The column in the given DataFrame (df) that contains closing short SMA window rolling average.

        long_col :
            The column in the given DataFrame (df) that contains closing long SMA window rolling average.

        short_window :
            The window length of the short SMA rolling average. This will be used to populate the plot legend.

        long_window :
            The window length of the long SMA rolling average. This will be used to populate the plot legend.
    """

    fig, ax = plt.subplots(figsize=(14,7))

    ax.set_title('Moving Average Crossover', fontsize=20)
    ax.plot(df[close_col], label='Close Price', linestyle='-', linewidth=1, alpha=0.5, zorder=1)
    ax.plot(df[short_col], label=f'SMA{short_window}', color='Green', alpha=1, zorder=2)
    ax.plot(df[long_col], label=f'SMA{long_window}', color='Red', alpha=1, zorder=3)
    ax.spines[["top", "right"]].set(visible=False)
    ax.grid(alpha=0.3)

    ax.fill_between(df.index,
                    df[short_col],
                    df[long_col],
                    where=(df[short_col] > df[long_col]),
                    color='Green',
                    alpha=0.1,
                    label="In Position")

    ax.fill_between(df.index,
                    df[short_col],
                    df[long_col],
                    where=(df[short_col] < df[long_col]),
                    color='Red',
                    alpha=0.1,
                    label="Out of Position")

    ax.legend(loc='upper left')

    return fig, ax

def plot_signals(df,
                 buy_markers,
                 sell_markers,
                 close_col: str = 'Close',
                 short_col: str = 'sma_short',
                 long_col: str = 'sma_long'):
    
    fig, ax = plt.subplots(figsize=(14,7))

    ax.set_title('SMA Strategy Buy & Sell Positions', fontsize=20)
    ax.plot(df[close_col], label='Close Price', linestyle='-', linewidth=1, alpha=1, zorder=1)
    ax.scatter(x=buy_markers.index, y=df[close_col].loc[buy_markers.index], marker='^', s=100, color='Green', label='Buy Signal', zorder=4)
    ax.scatter(x=sell_markers.index, y=df[close_col].loc[sell_markers.index], marker='v', s=100, color='Red', label='Sell Signal', zorder=5)
    ax.spines[["top", "right"]].set(visible=False)
    ax.grid(alpha=0.3)

    y_min, y_max = ax.get_ybound()

    ax.fill_between(df.index,
                    y_max,
                    y_min,
                    where=(df[short_col] > df[long_col]),
                    color='Green',
                    alpha=0.1,
                    label='In Position')

    ax.fill_between(df.index,
                    y_max,
                    y_min,
                    where=(df[short_col] < df[long_col]),
                    color='Red',
                    alpha=0.1,
                    label='Out of Position')

    # Prevents duplicate keys being added to the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper left")

    return fig, ax


def plot_strategy(df,
                  in_position = None,
                  hold_col: str = 'price_cum_ret',
                  strategy_col: str = 'strategy_cum_ret'):

    """
    Plot strategy returns versus buy & hold returns

        df: A DataFrame Containing Price Data

        in_position: Boolean series indicating when we are in / out of position. Used to highlight position on the chart.

        hold_col: The column within the specified df that contains buy and hold returns
            default = 'price_cum_ret'

        strategy_col: The column within the specified df that contains strategy returns
            default = 'strategy_cum_ret'
    """

    fig, ax = plt.subplots(figsize=(14,7))
    ax.set_title("Buy & Hold vs Strategy Returns Over Time", fontsize=20)
    ax.set_ylabel("Cumulative Return Percentage %", fontsize=12)
    ax.plot(df['price_cum_ret'], label='Buy & Hold Returns')
    ax.plot(df['strategy_cum_ret'], label='Strategy Returns')
    ax.grid(alpha=1, linestyle=":")
    ax.spines[["top", "right"]].set(visible=False)

    if type(in_position) != type(None):

        y_min, y_max = ax.get_ybound()

        ax.fill_between(df.index,
                        y_max,
                        y_min,
                        where=in_position==True,
                        color='Green',
                        alpha=0.1,
                        label='In Position')

        ax.fill_between(df.index,
                        y_max,
                        y_min,
                        where=in_position==False,
                        color='Red',
                        alpha=0.1,
                        label='Out of Position')

    ax.legend(loc="upper left")

    return fig, ax

def backtest_ma_strategy(df_stock: pd.DataFrame = pd.DataFrame(),
                         price_col: str = 'Close',
                         ticker: str = "AAPL",
                         start: str = str(date.today().year - 5) + "-01-01",
                         end: str = str(date.today()),
                         short_window: int = 50,
                         long_window: int = 200,
):
    """
    Backtest a simple moving average trading strategy.

        df: A DataFrame Containing Price Data

        price_col: The column within the specified df that contains ticker price data
            default = 'Close'

        ticker: If a df is not provided then data for this ticker will be downloaded within a specified date range
            default = 'AAPL'

        start: If downloading fresh data then this is the start date of the period for which price data will be pulled
            default = The beginning of the year of today - 5

        end: If downloading fresh data then this is the end date of the period for which price data will be pulled
            default = today

        short_window: The short SMA rolling window length
            defaullt = 50

        long_window: The long SMA rolling window length
            default = 200
    """

    # If a dataframe containing price data is not provided then download the latest data from Yahoo Finance
    if df_stock.empty:
        # Ensure that we have a ticker
        if ticker == None:
            print('Ticker Needed')
            return

        # Download Ticker Price Data
        df_stock = yf.download(ticker, start=start, end=end)

        # Restructure data
        df = df_stock.droplevel(axis=1, level=1)[price_col].to_frame()
    else:
        df = df_stock.copy()

    # Short Signal
    df['sma_short'] = df[price_col].rolling(window=short_window).mean()
    # Long Signal
    df['sma_long'] = df[price_col].rolling(window=long_window).mean()
    # Drop rows where signals are missing due to lack of data
    df.dropna(inplace=True)

    # When the short window closes above the long window, flag a buy signal
    df['signal'] = (df['sma_short'] > df['sma_long']) * 1
    # Position the days trade based on the previous close signal
    df['position'] = df['signal'].shift(1)

    # The daily price change of the stock
    df['price_ret'] = df[price_col].pct_change()
    # The price change of the stock, only accounting for days we are in position
    df['strategy_ret'] = df['position'] * df['price_ret']

    # The return on investment if we had bought and held from the start date
    df['price_cum_ret'] = (1 + df['price_ret']).cumprod()
    # The return on investment if we had traded and held the the stock signal
    df['strategy_cum_ret'] = (1 + df['strategy_ret']).cumprod()

    return df