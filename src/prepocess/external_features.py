import pandas as pd
import os

def add_external_features():
    stock_list = pd.read_csv("data/stock_list.csv")
    stock_list["Sector"] = [s.rstrip().lower().capitalize() for s in stock_list["17SectorName"]]
    stock_list["Capitalization"] = (stock_list["MarketCapitalization"] - stock_list["MarketCapitalization"].mean()) / stock_list["MarketCapitalization"].std()
    stock_list["Shares"] = (stock_list["IssuedShares"] - stock_list["IssuedShares"].mean()) / stock_list["IssuedShares"].std()
    return stock_list[["SecuritiesCode", "Sector", "Capitalization", "Shares"]]