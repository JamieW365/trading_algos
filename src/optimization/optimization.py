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