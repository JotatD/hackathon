import requests
import pandas as pd
from typing import List, Dict


def process_date(date, delta_days=0):
    try:
        date = pd.Timestamp(date) - pd.Timedelta(days=delta_days)
        date = date.strftime("%Y-%m-%dT%H:%M:%S")
    finally:
        Exception('Date formatted incorrectly')

    return date


def get_url(coin, time_unit, time_measure, initial_time, final_time):

    period_id = time_unit + time_measure
    init_time_delta_string = process_date(initial_time, 30)
    final_time_string = process_date(final_time)

    url = 'https://rest.coinapi.io/v1/ohlcv/' + coin + '/USD/history?' + 'period_id=' + period_id + \
          '&time_start=' + init_time_delta_string + '&time_end=' + final_time_string + '&limit=10000'

    headers = {'X-CoinAPI-Key': 'B8850AA1-7601-4966-9DA6-3906424071BB'}
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'error' in data:
        raise Exception(data['error'])
    elif len(data) == 0:
        raise Exception('Non-existing coin')

    return url


def get_header():
    return {'X-CoinAPI-Key': 'B8850AA1-7601-4966-9DA6-3906424071BB'}


def process_data(data: List[Dict]):
    crypto_data = pd.DataFrame(data)[["time_close", "price_close"]]
    crypto_data = crypto_data.rename(columns={"time_close": "date", "price_close": "price"})
    crypto_data["date"] = pd.to_datetime(crypto_data["date"]).dt.strftime("%Y-%m-%d")
    crypto_data = crypto_data.set_index("date")
    return crypto_data

