from utils import get_url, process_date, get_header, process_data
from financial import calculate_return, calculate_volatility
import requests
import pandas as pd


def financial_metrics_calculation(coin_a, coin_b, time_unit, time_measure, initial_time, final_time):

    start_time = process_date(initial_time)
    end_time = process_date(final_time)

    coin_a_url = get_url(coin_a, time_unit, time_measure, initial_time, final_time)
    coin_b_url = get_url(coin_b, time_unit, time_measure, initial_time, final_time)
    header = get_header()

    info_coin_a = requests.get(coin_a_url, headers=header).json()
    info_coin_a = process_data(info_coin_a)
    info_coin_b = requests.get(coin_b_url, headers=header).json()
    info_coin_b = process_data(info_coin_b)

    info_coin_a = calculate_return(info_coin_a)
    info_coin_a = calculate_volatility(info_coin_a)
    info_coin_a = info_coin_a.loc[start_time:end_time]

    info_coin_b = calculate_return(info_coin_b)
    info_coin_b = calculate_volatility(info_coin_b)
    info_coin_b = info_coin_b.loc[start_time:end_time]

    returns_df = pd.DataFrame([])
    returns_df[coin_a] = info_coin_a["returns"]
    returns_df[coin_b] = info_coin_b["returns"]

    volatility_df = pd.DataFrame([])
    volatility_df[coin_a] = info_coin_a["volatility"]
    volatility_df[coin_b] = info_coin_b["volatility"]

    return returns_df, volatility_df
