def getPrice(coinname, balances, prices):
#def getPrice(coinname, balances, prices):	
    # computes price of currencies defined in 'coinname'
    btcPrice = float(prices['USDT_BTC']['last']) 
    other = 'BTC_%s' % coinname
    otherPrice = float(prices[other]['last'])

    if coinname == 'ARDR':
        otherBalance = 14000
    elif coinname == 'NXT':
        otherBalance = 5439
    else:    
        otherBalance = float(balances[coinname])  
    
    outValue = btcPrice * otherPrice * otherBalance








