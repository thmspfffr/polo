import pandas as pd
from scipy.stats.stats import pearsonr    
import numpy as np

def get_correlations():

    COINS = ['ARDR','IOTA','LSK']

    # one hour / one day / one week
    N = [30, 720, 7*720]
    r = np.zeros((3,3,3))

    for idur in range(0,3):

        size = sum(1 for l in open('output/prices.csv'))
        df = pd.read_csv('output/prices.csv', skiprows=range(1, size - N[idur]-1))

        for i in range(0,3):
            for j in range(0,3):
            
                tmp=pearsonr(df[COINS[i]],df[COINS[j]])
                r[i,j,idur]=tmp[0]

                
    return r













