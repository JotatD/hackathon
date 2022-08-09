import requests
import time
import pandas as pd
import json
# url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=10DAY&time_start=2022-01-01T00:00:00&time_end=2022-02-01T00:00:00'
# headers = {'X-CoinAPI-Key' : 'B8850AA1-7601-4966-9DA6-3906424071BB'}
# response = requests.get(url, headers=headers)

# for price in response.json():
#     print(price["time_open"]) 
#     print("\n") # example usage

exampleTime = '2022-01-01'
exampleTime2 = '2022-01-02'

def getUrl(coin, timeUnit, timeMeasure, initialTime, finalTime):
    period_id = timeUnit + timeMeasure
    try: 
        init_time_string = pd.Timestamp(initialTime).strftime("%Y-%m-%dT%H:%M:%S")
        final_time_string = pd.Timestamp(finalTime).strftime("%Y-%m-%dT%H:%M:%S")
    except:
        print('Date formated incorrectly')
        return ''

    url = 'https://rest.coinapi.io/v1/exchangerate/'+ coin + '/USD/history?' + 'period_id=' + period_id+'&time_start=' + init_time_string + '&time_end=' + final_time_string

    headers = {'X-CoinAPI-Key' : 'B8850AA1-7601-4966-9DA6-3906424071BB'}
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'error' in data:
        raise Exception(data['error'])
    elif (len(data) == 0) :
        raise Exception('Non-existing coin')

    return url

url = getUrl('BTC', '2', 'HRS', exampleTime, exampleTime2)
print(url)

headers = {'X-CoinAPI-Key' : 'B8850AA1-7601-4966-9DA6-3906424071BB'}
response = requests.get(url, headers=headers)
data = response.json()


for datum in data:
    print(datum)
