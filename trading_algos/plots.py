from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

from trading_algos.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

def plot_returns(data: pd.DataFrame,
                 figsize: tuple=(12,6),
                 normalize: bool=False,
                 rolling_window: int=1,
                 highlight: list=None,
                 save_plot: str=None):

    if highlight == None:
        highlight = data.Close.columns
    highlight = set(highlight)

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_title('Normalized Returns' if normalize else 'Stock Price')

    for stock in data.Close:
        ax.plot(data.Close[stock]\
                .div(data.Close[stock].iloc[0] if normalize else 1)\
                    .mul(100 if normalize else 1)\
                        .sub(100 if normalize else 0)\
                            .rolling(rolling_window)\
                                .mean(),
                label=stock,
                alpha=1 if stock in highlight else 0.25,
                linewidth=1.5 if stock in highlight else 1)
        
    if normalize:
        ax.yaxis.set_major_formatter(PercentFormatter())
        
    ax.legend(labels=data.Close.columns)
    ax.grid(alpha=0.3)
    ax.spines[['top', 'right']].set_visible(False)

    return plt.show();


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
