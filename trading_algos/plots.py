from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import numpy as np
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

def plot_summary(data,
                 plots: list=['rr', 'sharpe'],
                 ncols: int=2):
    
    '''
    Take a summary table and plot a dynamic grid of requested summary charts
    '''

    # Ensure that the input dataset is never overwritten within this function
    _data = data.copy()

    # Check input type
    if type(plots) == str:
        plots = [plots]

    # Defualt list of valid plots
    valid_plots = ['rr', 'sharpe']
    # Check input list for invalid plot types and remove them
    invalid_plots = [x for x in plots if x not in valid_plots]
    # Remove invalid plots as well as any duplicates
    plots = list(set(plots) - set(invalid_plots))
    # Restore original order
    plots = [x for x in plots if x in plots]

    # Flag any invalid plots that have been ignored
    if invalid_plots != []:
        print(invalid_plots, 'plots are invalid and will be skipped')
    # Error if no valid plot types have passed into the function
    if plots == []:
        raise Exception('Pass in atlease one valid plot type', valid_plots)

    # Do not need more columns in the grid than we have plots
    ncols = min(ncols, len(plots))

    # Calculate the number of columns required within the subplot
    # Dependent on the number of columns specified and the number of plots required to be shown
    nrows = int(np.ceil(len(plots) / ncols))

    # Generate a new figure with reference axes
    fig, ax = plt.subplots(nrows, ncols, figsize=(6*ncols, 6*nrows), tight_layout=True)

    # Set a figure title if creating a multi-plot grid
    if len(plots) > 1:
        fig.suptitle('Summary Plots')

    for i, plot in enumerate(plots):
        # Determine the row within the subplot grid to place the current plot
        sp_row = int(i/ncols)
        # Determine the column within the subplot grid to place the current plot
        sp_col = i%ncols
        # Axes reference will change dependent on the number of columns and rows which will effect iteration logic
        sp_ax = ax if (nrows == 1 and ncols == 1) else\
                ax[sp_row] if ncols == 1 else\
                ax[sp_col] if nrows == 1 else\
                ax[sp_row, sp_col]
        
        # Plot charts dependent on listed order position
        match plot:
            # Risk/Return scatter
            case 'rr':
                plot_risk_return(_data, ax=sp_ax)

            # Sharpe bar chart
            case 'sharpe':
                plot_sharpe(_data, ax=sp_ax)
                            
    # Determine how many empty plots there are on the last row of the figure
    num_empty_plots = nrows * ncols - len(plots)
    if num_empty_plots > 0:
        for i in range(1, num_empty_plots + 1):
            # Hide empty plots
            ax[nrows, ncols - i].set_axis_off()

    return fig, ax

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
