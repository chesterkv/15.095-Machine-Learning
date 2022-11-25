import numpy as np
import pandas as pd
from decimal import *

def generate_adjusted_close(df):
    """
    Args:
        df (pd.DataFrame)  : stock_price for a single SecuritiesCode
    Returns:
        df (pd.DataFrame): stock_price with AdjustedClose for a single SecuritiesCode
    """
    # sort data to generate CumulativeAdjustmentFactor
    df = df.sort_values("Date", ascending=False)
    # generate CumulativeAdjustmentFactor by taking the cumulative product of AdjustmentFactor
    df.loc[:, "CumulativeAdjustmentFactor"] = df["AdjustmentFactor"].cumprod()
    # generate AdjustedClose
    df.loc[:, "AdjustedClose"] = (
        df["CumulativeAdjustmentFactor"] * df["Close"]
    ).map(lambda x: float(
        Decimal(str(x)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    ))
    # reverse order
    df = df.sort_values("Date")
    # to fill AdjustedClose, replace 0 into np.nan
    df.loc[df["AdjustedClose"] == 0, "AdjustedClose"] = np.nan
    # forward fill AdjustedClose
    df.loc[:, "AdjustedClose"] = df.loc[:, "AdjustedClose"].ffill()
    return df

def adjust_price(price):
    """
    Args:
        price (pd.DataFrame)  : pd.DataFrame include stock_price
    Returns:
        price DataFrame (pd.DataFrame): stock_price with generated AdjustedClose
    """
    # copy to edit
    price = price.copy()

    # generate AdjustedClose
    price = price.sort_values(["SecuritiesCode", "Date"])
    price = price.groupby("SecuritiesCode").apply(generate_adjusted_close).reset_index(drop=True)

    return price