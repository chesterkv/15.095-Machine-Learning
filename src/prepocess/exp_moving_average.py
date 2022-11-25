import pandas as pd
import numpy as np

def add_exp_moving_average(df,col,period):
    df.loc[:,f"ema_{period}days"] = df.groupby("SecuritiesCode")[col].ewm(span=period,adjust=False).mean().values