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
    
def bar_plot(timescale):
    """
    Makes bar plot, containing the hourly/daily/weekly/all-time changes
    of all currencies that are currently held
    Timescale: 'percent_change_1h','percent_change_24h','percent_change_7d'
    """
    all_col = ['r','g']
    currencies = ['ARDOR','basic-attention-token','IOTA','LISK','NEM']
    delta_price = list()
    colors = list()

    for icurr in currencies:

        val = float(coinmarketcap.ticker(icurr, limit=3, convert='USD')[0][timescale])
        delta_price.append(val)
        colors.append(all_col[int(val>0)])

    tl = ['ARDR','BAT','IOTA','LSK','XEM']
    fig, ax = plt.subplots()
    fig.set_facecolor((1, 1, 1))
    ax.bar([0.5,2,3.5,5,6.5],delta_price,width=1,color=colors,linewidth=0)

    ax.set_ylabel('Change [%]')
    ax.set_xticks([.5,2,3.5,5,6.5])
    ax.set_xticklabels((tl))

    if np.max(np.abs(delta_price)) < 5:
        ax.set_ylim([-5,5])
    elif np.max(np.abs(delta_price)) < 10 and np.max(np.abs(delta_price)) > 5:
        ax.set_ylim([-10,10])
    elif np.max(np.abs(delta_price)) < 25 and np.max(np.abs(delta_price)) > 10:
        ax.set_ylim([-25,25])
    elif np.max(np.abs(delta_price)) < 50 and np.max(np.abs(delta_price)) > 25:
        ax.set_ylim([-50,50])
    elif np.max(np.abs(delta_price)) < 100 and np.max(np.abs(delta_price)) > 50:
        ax.set_ylim([-100,100])
    else:
        ax.set_ylim([-200,200])

    ax.grid('on',axis='y')
    ax.set_title('%s' % timescale)
    plt.savefig('plots/bar_plot_%s.png' % timescale)
    plt.close()

    ftp = FTP('s610.deinprovider.de')
    ftp.login('web10','IzULi9HE')
    ftp.cwd('html')

    ftp.storbinary('STOR bar_plot_%s.png' %timescale, open('plots/bar_plot_%s.png' %timescale,'rb'))  
    ftp.quit()
    

def make_html(totalPercentChange,totalValue):

    file = open('index.html', 'w')
    file.write('<HTML>\n<HEAD>\n<TITLE>Ticker</TITLE>') 
    file.write('<BODY><P><b>Total value:</b> %d USD' % totalValue)  
 
    if totalPercentChange > 0:
        file.write('<P><b>Total percent change:</b> +%.2f%%' % totalPercentChange) 
    else:
        file.write('<P><b>Total percent change:</b> %.2f%%' % totalPercentChange) 

    #file.write('<br><br><IMG src="mybalance.png" height="400" width="500">') 

    bar_plot('percent_change_1h')
    file.write('<br>')
    file.write('<br><IMG src="bar_plot_percent_change_1h.png" height="300" width="400">')  
    bar_plot('percent_change_24h')
    file.write('<IMG src="bar_plot_percent_change_24h.png" height="300" width="400">') 
    bar_plot('percent_change_7d')
    file.write('<IMG src="bar_plot_percent_change_7d.png" height="300" width="400">') 

    file.write('</BODY></HTML>')  

    file.close()
    ftp = FTP('s610.deinprovider.de')
    ftp.login('web10','IzULi9HE')
    ftp.cwd('html')

    ftp.storbinary('STOR blc.html', open('index.html','rb')  )


    #file.write('ARDR, \t1h: %.2f%% ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_1h'])) 
    #file.write('\t1d: %.2f%% / ' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_24h'])) 
    #file.write('\t7d: %.2f%%\n' % float(coinmarketcap.ticker('ARDOR', limit=3, convert='USD')[0]['percent_change_7d'])) 
    