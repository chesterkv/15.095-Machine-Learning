import pandas as pd
import numpy as np

def add_return(df,col,period):
    df.loc[:,f"return_{period}days"] = df.groupby("SecuritiesCode")[col].pct_change(period)
