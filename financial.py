import pandas as pd


def calculate_return(crypto_data: pd.DataFrame):
    crypto_data["returns"] = crypto_data["price"].pct_change()*100
    return crypto_data


def calculate_volatility(crypto_data: pd.DataFrame):
    crypto_data["volatility"] = crypto_data["returns"].rolling(30).std()
    return crypto_data


def calculate_complete_return(crypto_data: pd.DataFrame):
    start_price = crypto_data[0]
    end_price = crypto_data[-1]
    complete_return = (end_price-start_price)/start_price
    return complete_return


def calculate_complete_volatility(crypto_data: pd.DataFrame):
    complete_volatility = crypto_data.std()
    return complete_volatility

