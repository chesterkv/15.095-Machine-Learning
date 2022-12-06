import pandas as pd
import os

def add_external_features():
    limit_sectors = {
        'Foods':'Retail trade',
        '-':'-',
        'Commercial & wholesale trade':'Retail trade',
        'Construction & materials':'Construction & materials',
        'Steel & nonferrous metals':'Construction & materials',
        'Energy resources':'Energy resources',
        'It & services, others':'It & services, others',
        'Machinery':'Machinery',
        'Pharmaceutical':'Pharmaceutical',
        'Real estate':'Real estate',
        'Transportation & logistics':'Transportation & logistics',
        'Financials （ex banks）':'Banks',
        'Retail trade':'Retail trade',
        'Raw materials & chemicals':'Construction & materials',
        'Electric appliances & precision instruments':'Machinery',
        'Automobiles & transportation equipment':'Transportation & logistics',
        'Banks':'Banks',
        'Electric power & gas':'Energy resources'
    }
    stock_list = pd.read_csv("data/stock_list.csv")
    stock_list["Sector"] = [s.rstrip().lower().capitalize() for s in stock_list["17SectorName"]]
    stock_list["Sector"] = stock_list["Sector"].map(limit_sectors)
    stock_list["Capitalization"] = (stock_list["MarketCapitalization"] - stock_list["MarketCapitalization"].mean()) / stock_list["MarketCapitalization"].std()
    stock_list["Shares"] = (stock_list["IssuedShares"] - stock_list["IssuedShares"].mean()) / stock_list["IssuedShares"].std()
    return stock_list[["SecuritiesCode", "Sector", "Capitalization", "Shares"]]