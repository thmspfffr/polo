# reddit_crypto_analysis
import pandas as pd

def get_reddit_subs(coinname,timeframe):

            # load data
    nsubs       = pd.read_csv('~/Dropbox/reddit/reddit_crypto/output/reddit_subs.csv')
    marketcap   = pd.read_csv('~/Dropbox/reddit/reddit_crypto/output/reddit_marketcap.csv')

    # prct change 
    prct_nsubs      = 100*(nsubs.diff()[1:].reset_index()/nsubs[1:].reset_index())
    prct_marketcap  = 100*(marketcap.diff()[1:].reset_index()/marketcap[0:-1].reset_index())

    #r = np.corrcoef(prct_nsubs['ARDR'],prct_marketcap['ARDR'])

    # compute the change in percent
    prct_change = prct_nsubs[-timeframe:].sum().sort_values().dropna()[coinname]
    # compute change relative to the mean change in subs
    rel_prct_change = int(round(100*(prct_nsubs[-timeframe:].sum()[coinname]/prct_nsubs[-timeframe:].drop(['index'],axis=1).sum().mean()-1)))
    # compute subscriptions per usd marketcap
    subs_per_usd = nsubs[coinname][-1:].iloc[0]/marketcap[coinname][-1:].iloc[0]
    # return number of subscriptions
    number_of_subs = nsubs[coinname][-1:].iloc[0]
    # subscription rank
    rank_of_subs = nsubs[-1:].rank(axis=1,ascending=0,method='min').T.dropna().T[coinname].iloc[0]
    
    return (prct_change, rel_prct_change, subs_per_usd, number_of_subs, rank_of_subs)
