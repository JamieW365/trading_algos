from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns

from trading_algos.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def plot_returns(data: pd.DataFrame,
                 returns: bool=False,
                 figsize: tuple=(12,6),
                 normalize: bool=False,
                 rolling_window: int=1,
                 highlight: list=None,
                 save_plot: str=None):

    if returns:
        data = (1 + data).cumprod()

    if highlight == None:
        highlight = data.columns
    highlight = set(highlight)

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_title('Normalized Returns' if normalize else 'Stock Price')

    for stock in data:
        ax.plot(data[stock]\
                .div(data[stock].iloc[0] if normalize else 1)\
                    .mul(100 if normalize else 1)\
                        .sub(100 if normalize else 0)\
                            .rolling(rolling_window)\
                                .mean(),
                label=stock,
                alpha=1 if stock in highlight else 0.25,
                linewidth=1.5 if stock in highlight else 1)
        
    if normalize:
        ax.yaxis.set_major_formatter(PercentFormatter())
        
    ax.legend(labels=data.columns)
    ax.grid(alpha=0.3)
    ax.spines[['top', 'right']].set_visible(False)

    return plt.show();

def plot_risk_return(data,
                     figsize: tuple=(8, 8),
                     ax=None,
                     save_plot: str=None):

    '''
    Plot Risk/Return
    
    Takes a summary table and plots risk verus return in a scatter plot
    '''
    
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    
    for asset in data.index:
        ax.annotate(asset, xy=[data.loc[asset, 'Risk']+0.002, data.loc[asset,'Return']+0.002])

    sns.scatterplot(data=data,
                    x='Risk',
                    y='Return',
                    hue='Sharpe',
                    size='Sharpe',
                    palette=sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True), 
                    ax=ax)
    # ax.scatter(data=data, x='Risk', y='Return')

    ax.set_title('Risk/Return')
    ax.set_ylabel('ann. Return')
    ax.set_xlabel('ann. Risk')
    ax.set_aspect('equal')
    ax.grid(alpha=0.3)
    ax.legend().remove()

    return ax

def plot_sharpe(data,
                sorted: bool=True,
                ax=None):
    
    '''
    Bar plot of Sharpe ratio

    Takes a summary table and plots the Sharpe ratio of each asset in a bar plot
    '''

    # Ensure that the input dataset isnt overwritten by this function
    _data = data.copy()

    if sorted:
        _data.sort_values('Sharpe', ascending=False, inplace=True)

    if ax is None:
        fig, ax = plt.subplots()

    # sns.color_palette
    sns.barplot(x='Sharpe', 
                y=_data.index, 
                data=_data, 
                hue='Sharpe', 
                palette=sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True), 
                ax=ax)
    
    for asset in data.index:
        ax.annotate(text=round(data.loc[asset,'Sharpe'],2),
                    xy=[data.loc[asset,'Sharpe'] + 0.02, asset])

    ax.set_title('Sharpe')
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.legend().remove()

    return ax



@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
