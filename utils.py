import pandas as pd
import requests
from typing import List, Dict


def process_date(date, delta_days=0):
    try:
        date = pd.Timestamp(date) - pd.Timedelta(days=delta_days)
        date = date.strftime("%Y-%m-%dT%H:%M:%S")
    finally:
        Exception('Date formatted incorrectly')

    return date


def get_url(coin):

    url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={coin}&tsym=USD&limit=2000'

    return url


def get_data(coin):
    coin_url = get_url(coin)

    info_coin = requests.get(coin_url).json()

    if 'error' in info_coin:
        raise Exception(info_coin['error'])
    elif len(info_coin) == 0:
        raise Exception('Non-existing coin')

    info_coin = process_data(info_coin['Data']['Data'])
    info_coin.columns.name = coin
    return info_coin


def process_data(data: List[Dict]):

    crypto_data = pd.DataFrame(data)
    crypto_data = crypto_data.rename(columns={'time': 'date', 'close': 'price'})
    crypto_data = crypto_data[['date', 'price']]
    crypto_data['date'] = pd.to_datetime(crypto_data['date'], unit='s')
    crypto_data = crypto_data.set_index('date')

    return crypto_data

