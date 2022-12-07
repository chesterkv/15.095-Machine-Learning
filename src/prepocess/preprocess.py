import pandas as pd
import numpy as np
import logging
import argparse
import coloredlogs

from returns import add_return
from moving_average import add_moving_average
from exp_moving_average import add_exp_moving_average
from volatility import add_volatility
from price_adjustment import adjust_price

from drawdown import add_drawdown

from external_features import add_external_features


def preprocess_prices(df):
    logging.debug("Converting dates")
    df.loc[: ,"Date"] = pd.to_datetime(df.loc[: ,"Date"], format="%Y-%m-%d")
    # Adjust close price
    logging.debug("Calculating adjusted close price")
    df = adjust_price(df)
    df.sort_values(by=['SecuritiesCode', 'Date'], ascending=[True, True], inplace=True)
    df.set_index("Date", inplace=True)

    for period in [5,10,30,60]:
        logging.debug(f"Calculating features for period {period} days")
        add_return(df,"AdjustedClose",period)
        add_moving_average(df,"AdjustedClose",period)
        add_exp_moving_average(df,"AdjustedClose",period)
        add_volatility(df,"AdjustedClose",period)

    df = add_drawdown(df)
    df = df.drop(columns=['RowId','ExpectedDividend','AdjustmentFactor','SupervisionFlag',
                         'Close', 'CumulativeAdjustmentFactor'],axis=1).fillna(0)
    df.reset_index(inplace=True)

    logging.debug(f"Adding external features, inital shape : {df.shape}")
    df = df.merge(add_external_features(), on = "SecuritiesCode", how = "left")
    logging.debug(f"Final shape : {df.shape}")

    return df

def _parse_args():
    parser = argparse.ArgumentParser(
        description="Arguments for preprocessing the dataset"
    )
    parser.add_argument(
        "--verbose", "-v", help="Sets the label of verbose", action="store_true"
    )
    return parser.parse_args()

def main(args):
    
    # preprocess train
    logging.info("Loading train data")
    prices_train = pd.read_csv('../../data/train_files/stock_prices.csv')
    logging.info("Preprocessing train data")
    prices_train = preprocess_prices(prices_train)
    logging.info("Saving train data")
    prices_train.to_csv('../../data/preprocessed/stock_prices_train_5_10_30_60.csv', index=False)


    # preprocess test
    logging.info("Loading test data")
    prices_test = pd.read_csv('../../data/supplemental_files/stock_prices.csv')
    logging.info("Preprocessing test data")
    prices_test = preprocess_prices(prices_test)

    logging.info("Saving test data")
    prices_test.to_csv('../../data/preprocessed/stock_prices_supplemental_5_10_30_60.csv',
                       index=False)


if __name__ == '__main__':
    args = _parse_args()
    level = "INFO" if not args.verbose else "DEBUG"
    config = dict(
        fmt="[[{relativeCreated:7,.0f}ms]] {levelname} [{module}] {message}",
        style="{",
        level=level,
    )
    coloredlogs.DEFAULT_LEVEL_STYLES["debug"] = {"color": 201}
    coloredlogs.DEFAULT_LEVEL_STYLES["warning"] = {
        "color": "red",
        "style": "bright",
        "bold": True,
        "italic": True,
    }
    coloredlogs.DEFAULT_FIELD_STYLES["levelname"] = {
        "color": "blue",
        "style": "bright",
        "bold": True,
    }
    coloredlogs.DEFAULT_FIELD_STYLES["relativeCreated"] = {
        "color": 10,
        "style": "bright",
    }
    coloredlogs.install(**config)
    main(args)