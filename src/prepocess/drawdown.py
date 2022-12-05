import pandas as pd
import numpy as np

def add_drawdown(df):
    """
    compute the drawdown for each stock in df per day N, that's to say for each stock,
    the difference between the maximum of the returns between day 0 and day N-1 and the return of day N for this stock


    Args:
        df:

    Returns:

    """
    df = df.sort_values(by = ['SecuritiesCode', 'Date'], ascending = [True, True])
    df['Drawdown'] = df.groupby('SecuritiesCode')['Target'].apply(lambda x: x.cummax() - x)

    return df