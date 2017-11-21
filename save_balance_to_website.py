import poloniex
import numpy as np
from bittrex import bittrex
import time
from ftplib import FTP
from plot import poloplot
from plot import make_html
from coinmarketcap import Market
import polo_correlation as pc


all_my_coins = []

# reads in rates at which coins where purchased (in BTC)
# todo: read this number from exchanges
all_my_rates = {}
with open("allmyrates.txt") as f:
    for line in f:
       (key, val) = line.split()
       all_my_rates[key] = val

# read this from text file
API = 'W7N7KE0K-86M9X81P-O63WFUJ0-V80HZVHM'
SEC = '477388e772d45639e79495cd183ecc8c15d7d411162a5645c1f4eaee8bf8940a40bd842bf6388a384c27af953f4e3de0a4a26b87c9bb15f8a5cf3ba975c3ef3d'

while True:

    try:
        print('Waking ...')
        
        # connect to bittrex
        bittrex_ticker = bittrex('98db5347b4294f4eb85c3c3fc4169d50','6eb9fd8ee7304e209474a7bced944cec')
        
        myBittrexBalance = bittrex_ticker.get_balance()

        totalBittrexUSDT = 0

        for i in range(0,len(myBittrexBalance)):

            currentCoin = myBittrexBalance['result'][i]
            coinname = str(currentCoin['Currency']['Currency'])

            if currentCoin['Balance']['Balance'] > 5:

                all_my_coins.append(coinname)

                if coinname == 'BTC':

                    currentUSDT = bittrex_ticker.get_market_summary('USDT-BTC')
                    currentValueBTCUSDT = float(currentUSDT['result']['Last'])
                    currentBalance = float(currentCoin['Balance']['Available'])

                    currentValueInUSDT =  currentValueBTCUSDT * currentBalance

                else:

                    marketname = 'BTC-%s' % (coinname)
                    currentMarket = bittrex_ticker.get_market_summary(marketname)
                    currentValueInBTC = float(currentMarket['result']['Last'])

                    currentUSDT = bittrex_ticker.get_market_summary('USDT-BTC')
                    currentValueBTCUSDT = float(currentUSDT['result']['Last'])

                    currentBalance = bittrex_ticker.getbalance(coinname)['Balance']['Available']

                    currentValueInUSDT =  currentValueBTCUSDT * currentValueInBTC * currentBalance

                    current_rate = float(all_my_rates[coinname])

                totalBittrexUSDT =  totalBittrexUSDT + currentValueInUSDT

        # CONNECT TO POLONIEX
        btc_ticker = poloniex.Poloniex(API, SEC)
        balances = btc_ticker.returnBalances()
        prices = btc_ticker.returnTicker()

        b = [float(x) for x in balances.values()]
        IDX = [x for x, i in enumerate(b) if i > 5]
        myCoins =  [balances.keys()[index] for index in IDX]

        all_my_coins.extend(myCoins)

        def getPrice(coinname, balances, prices):
        #def getPrice(coinname, balances, prices):	
            # computes price of currencies defined in 'coinname'

            if coinname == 'USDT':
                outValue = float(balances['USDT'])
                return outValue

            if coinname == 'BTC':
                btcPrice = float(prices['USDT_BTC']['last']) 
                otherBalance = float(balances['BTC']) 
                outValue = otherBalance * btcPrice
                return outValue

            btcPrice = float(prices['USDT_BTC']['last']) 
            other = 'BTC_%s' % coinname
            otherPrice = float(prices[other]['last'])

            if coinname == 'ARDR':
                otherBalance = 15000
            else:    
                otherBalance = float(balances[coinname])  
            
            outValue = btcPrice * otherPrice * otherBalance

            return outValue

        tmp = 0

        for x in range(len(myCoins)):
            tmp = tmp + getPrice(myCoins[x], balances, prices)

        tmp = tmp + getPrice('ARDR', balances, prices) + getPrice('NXT', balances, prices)

        totalPoloniexUSDT = tmp

        coinmarketcap = Market()
        iota_usd = float(coinmarketcap.ticker('IOTA', limit=3, convert='USD')[0]['price_usd'])
        my_iota_value = 1406 * iota_usd

        totalValue = totalPoloniexUSDT + totalBittrexUSDT + my_iota_value

        totalInvested = 3574 + 601 

        totalPercentChange = 100*totalValue/totalInvested-100

        f = open('allTimeCryptoBalance.txt', 'a')
        f.write('%d \t %d\n' % (int(time.time()), totalValue))
        f.close()

        np.savetxt('allmycoins.txt',np.array(all_my_coins),delimiter='\n',fmt = '%s')

        allTimeCryptoBalance = np.loadtxt('allTimeCryptoBalance.txt')
        timeDiff = np.loadtxt('allTimeCryptoBalance.txt')[-2]-np.loadtxt('allTimeCryptoBalance.txt')[0]

        file = open('totalCryptoBalance.txt', 'w')
        file.write('Total value: %d USD\n' % totalValue) 
        if totalPercentChange > 0:
            file.write('Total percent change: +%.2f%%\n\n' % totalPercentChange) 
        else:
            file.write('Total percent change: %.2f%%\n\n' % totalPercentChange) 
        
        make_html(totalPercentChange,totalValue)

        file.close()
        ftp = FTP('s610.deinprovider.de')
        ftp.login('web10','IzULi9HE')
        ftp.cwd('html')    

        ftp.storbinary('STOR blc.txt', open('totalCryptoBalance.txt', 'rb'))  
        ftp.quit() 
        print('Saved txt ...')
        # create plot
        poloplot()
        print('Saved plot ...')
        
        time.sleep(60)
    except Exception as e: print(e)
        #print('Something went wrong...')

        
