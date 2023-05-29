import pandas as pd
from datetime import datetime as dt
import sys
def update_cron_parameter():
    df = pd.read_csv('cron_parameters.csv',index_col=0)
    # print(df.shape)
    n = df.shape[0]+1
    if n >=49:
        print(n)
        return
    else:
        df=pd.concat([df,pd.DataFrame([['','',0,'']],index=[n],columns=df.columns)])
        df.index.name='month'
        df.to_csv('cron_parameters.csv')
        print(n)
        
if __name__=='__main__':
    update_cron_parameter()
