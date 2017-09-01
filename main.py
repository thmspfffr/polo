from polo import poloniex
import numpy as np
from bittrex import bittrex
import time
from ftplib import FTP

API = 'O1O0O76T-Z2M0ZOQM-15NPVFG0-AUKH3WKH'
SEC = 'c12cfb5fa7bb7506e190ed7b0a48a864eb2179f4ddc8793321b75154752325c77f472b98abc756cc390d37c553c0ffd5bed88dbe247f2bb41af5c641cc1408eb'

while True:
    try:
        print "Receiving data from exchanges ..."
        # connect to poloniex 
        btc_ticker = poloniex(API, SEC)

        balances = btc_ticker.returnBalances()
        prices = btc_ticker.returnTicker()

        b = [float(x) for x in balances.values()]
        IDX = [x for x, i in enumerate(b) if i > 0]
        myCoins =  [balances.keys()[index] for index in IDX]

        # connect to bittrex
        bittrex_ticker = bittrex('98db5347b4294f4eb85c3c3fc4169d50','6eb9fd8ee7304e209474a7bced944cec')
        myBittrexBalance = bittrex_ticker.getbalances()
        totalBittrexUSDT = 0

        for i in range(0,len(myBittrexBalance)):

            currentCoin = myBittrexBalance[i]
            coinname = str(currentCoin['Currency'])

            if coinname == 'BTC':

                currentUSDT = bittrex_ticker.getmarketsummary('USDT-BTC')
                currentValueBTCUSDT = currentUSDT[0]['Last']
                currentBalance = bittrex_ticker.getbalance(coinname)['Available']

                currentValueInUSDT =  currentValueBTCUSDT * currentBalance

            else:

                marketname = 'BTC-%s' % (coinname)
                currentMarket = bittrex_ticker.getmarketsummary(marketname)
                currentValueInBTC = currentMarket[0]['Last']

                currentUSDT = bittrex_ticker.getmarketsummary('USDT-BTC')
                currentValueBTCUSDT = currentUSDT[0]['Last']

                currentBalance = bittrex_ticker.getbalance(coinname)['Balance']

                currentValueInUSDT =  currentValueBTCUSDT * currentValueInBTC * currentBalance

            totalBittrexUSDT =  totalBittrexUSDT + currentValueInUSDT



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

        totalValue = totalPoloniexUSDT + totalBittrexUSDT

        totalInvested = 3574

        totalPercentChange = 100*totalValue/totalInvested-100

        f = open('allTimeCryptoBalance.txt', 'a')
        f.write('%d \t %d\n' % (int(time.time()), totalValue))
        f.close()

        allTimeCryptoBalance = np.loadtxt('allTimeCryptoBalance.txt')
        timeDiff = np.loadtxt('allTimeCryptoBalance.txt')[-2]-np.loadtxt('allTimeCryptoBalance.txt')[0]

        file = open('totalCryptoBalance.txt', 'w')
        file.write('Total value: %d USD\n' % totalValue) 
        if totalPercentChange > 0:
            file.write('Total percent change: +%.2f%%' % totalPercentChange) 
        else:
            file.write('Total percent change: %.2f%%' % totalPercentChange) 
        file.close()

        ftp = FTP('s610.deinprovider.de')
        ftp.login('web10','IzULi9HE')
        ftp.cwd('html')

        fileToSend = open('totalCryptoBalance.txt','rb')                  
        ftp.storbinary('STOR blc.txt', fileToSend)  
        fileToSend.close()                                    
        ftp.quit() 

        time.sleep(60)
    except:
        print "Something went wrong..."