import pandas as pd
import numpy as np 

N_rows = np.shape(pd.read_csv('output/prices.csv'))[0]
N_cols = np.shape(pd.read_csv('output/prices.csv'))[1]

labels = ['ARDR','BTC','IOTA','LSK','TOTAL_MARKET_CAP']

df_to_append = pd.DataFrame(data=np.zeros([N_rows,np.size(labels)]),columns=labels)  

df_orig = pd.read_csv('output/prices.csv')

df = pd.merge(df_orig, df_to_append,how='left')

df.to_csv('output/prices.csv')


