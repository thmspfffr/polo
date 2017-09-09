import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from ftplib import FTP
from coinmarketcap import Market

coinmarketcap = Market()


def poloplot():

    balance = np.loadtxt('allTimeCryptoBalance.txt',delimiter='\t')

    # plot result
    fig = plt.figure()
    plt.plot(balance[:,0],balance[:,1])
    axes = plt.gca()
    fig.set_facecolor((1, 1, 1))
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel('Price [USDT]')
    #xes.set_xlim([0,10080])

    plt.savefig('mybalance.png')

    plt.close()

    ftp = FTP('s610.deinprovider.de')
    ftp.login('web10','IzULi9HE')
    ftp.cwd('html')
               
    ftp.storbinary('STOR mybalance.png', open('mybalance.png','rb')  )  
    ftp.quit()

def make_html(totalPercentChange,totalValue):

    file = open('index.html', 'w')
    file.write('<HTML>\n<HEAD>\n<TITLE>Ticker</TITLE>') 
    file.write('<BODY><P><b>Total value:</b> %d USD' % totalValue)  
 
    if totalPercentChange > 0:
        file.write('<P><b>Total percent change:</b> +%.2f%%' % totalPercentChange) 
    else:
        file.write('<P><b>Total percent change:</b> %.2f%%' % totalPercentChange) 

    file.write('<P><b>ARDR</b>, \t1h: %.2f%% ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_1h'])) 
    file.write('\t1d: %.2f%% / ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_24h'])) 
    file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_7d'])) 

    file.write('<P><b>BAT</b>, \t1h: %.2f%% ' % float(coinmarketcap.ticker('basic-attention-token', limit=3, convert='USD')[0]['percent_change_1h'])) 
    file.write('\t1d: %.2f%% ' % float(coinmarketcap.ticker('basic-attention-token', limit=3, convert='USD')[0]['percent_change_24h'])) 
    file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('basic-attention-token', limit=3, convert='USD')[0]['percent_change_7d'])) 

    file.write('<P><b>IOTA</b>, \t1h: %.2f%% ' % float(coinmarketcap.ticker('IOTA', limit=3, convert='USD')[0]['percent_change_1h'])) 
    file.write('\t1d: %.2f%% ' % float(coinmarketcap.ticker('IOTA', limit=3, convert='USD')[0]['percent_change_24h'])) 
    file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('IOTA', limit=3, convert='USD')[0]['percent_change_7d'])) 

    file.write('<P><b>LISK</b>, \t1h: %.2f%% ' % float(coinmarketcap.ticker('LISK', limit=3, convert='USD')[0]['percent_change_1h'])) 
    file.write('\t1d: %.2f%% ' % float(coinmarketcap.ticker('LISK', limit=3, convert='USD')[0]['percent_change_24h'])) 
    file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('LISK', limit=3, convert='USD')[0]['percent_change_7d'])) 

    file.write('<P><b>NEM</b>, \t1h: %.2f%% ' % float(coinmarketcap.ticker('nem', limit=3, convert='USD')[0]['percent_change_1h'])) 
    file.write('\t1d: %.2f%% ' % float(coinmarketcap.ticker('nem', limit=3, convert='USD')[0]['percent_change_24h'])) 
    file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('nem', limit=3, convert='USD')[0]['percent_change_7d'])) 



    file.write('<br><br><IMG src="mybalance.png" height="400" width="500">')  
    file.write('</BODY></HTML>')  

    file.close()
    ftp = FTP('s610.deinprovider.de')
    ftp.login('web10','IzULi9HE')
    ftp.cwd('html')

    ftp.storbinary('STOR blc.html', open('index.html','rb')  )


    #file.write('ARDR, \t1h: %.2f%% ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_1h'])) 
    #file.write('\t1d: %.2f%% / ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_24h'])) 
    #file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_7d'])) 
    