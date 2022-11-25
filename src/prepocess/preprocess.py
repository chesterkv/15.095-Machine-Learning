import pandas as pd
import numpy as np

from returns import add_return
from moving_average import add_moving_average
from exp_moving_average import add_exp_moving_average
from volatility import add_volatility


def preprocess_prices(df):
    for period in [5,10,30,60]:
        add_return(df,"Close",period)
        add_moving_average(df,"Close",period)
        add_exp_moving_average(df,"Close",period)
        add_volatility(df,"Close",period)
    return df

def main():
    
    # preprocess train
    prices_train = pd.read_csv('../../data/train_files/stock_prices.csv')
    prices_train = preprocess_prices(prices_train)
    prices_train.to_csv('../../data/preprocessed/stock_prices_train.csv', index=False)

    # preprocess test
    prices_test = pd.read_csv('../../data/supplemental_files/stock_prices.csv')
    prices_test = preprocess_prices(prices_test)
    prices_test.to_csv('../../data/preprocessed/stock_prices_supplemental.csv', index=False)

if __name__ == '__main__':
    main()