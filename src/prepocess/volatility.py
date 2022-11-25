import pandas as pd
import numpy as np

def add_volatility(df,col,period):
    df.loc[:,f"volatility_{period}days"] = np.log(df[col]).groupby(df["SecuritiesCode"]).diff().rolling(period).std()
