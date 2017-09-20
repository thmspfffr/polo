from coinmarketcap import Market
import pandas as pd
import time
import numpy as np
import os

def write_prices():

    coinmarketcap = Market()

    coins = ['ARDOR','basic-attention-token','IOTA','lisk','nem']

    val = np.zeros(5)
    icoin = 0
    t = int(time.time())

    for coin in coins:

        val[icoin] = float(coinmarketcap.ticker(coin, limit=3, convert='USD')[0]['price_usd'])
        icoin = icoin + 1

    labels = ['ARDR','BAT','IOTA','LSK','XEM']


    df = pd.DataFrame(data=[val] ,index=[t],columns=labels)
    df.index.name = 'Timestamp'

    if os.path.isfile('output/prices.csv'):
        with open('output/prices.csv', 'a') as f:
            df.to_csv(f,header=False)

    else:
        with open('output/prices.csv', 'w') as f:
            df.to_csv(f)


while True:
    try:

        print("Writing current USD prices to CSV...")
        write_prices()
        time.sleep(120)

    except:
        print("ERROR")




