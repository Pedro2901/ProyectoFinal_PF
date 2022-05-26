from copyreg import pickle
import pandas as pd
import pickle as p

'''
    Saving the sample as separate object to work better with it.
'''

df = pd.read_csv('data/20202.csv')
sample = df.sample(n=10000)
with open('data/sample10000.p','wb') as f:
    p.dump(sample,f)