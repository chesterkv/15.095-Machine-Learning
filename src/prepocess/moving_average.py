import pandas as pd
import numpy as np

def add_moving_average(df,col,period):
    df.loc[:,f"ma_{period}days"] = df.groupby("SecuritiesCode")[col].rolling(period).mean().values