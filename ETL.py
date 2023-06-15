import pandas as pd
import datetime as dt
import calendar

dt_lake = pd.read_csv('./bucket/old_tweets_database.csv')
# print(dt_lake.loc[1],'\n\n',dt.datetime.strptime(dt_lake.loc[1].date,'%b %d, %Y').weekday())
weekend_vs_weekend=[]
date=[]
txt=[]
for i in range(dt_lake.shape[0]):
    weekend_vs_weekend.append('w_day' if dt.datetime.strptime(dt_lake.loc[i].date,'%b %d, %Y').weekday()<5 else 'w_end')
    date.append(dt.datetime.strptime(dt_lake.loc[i].date,'%b %d, %Y').strftime('%d/%m/%Y'))
    txt.append(dt_lake.loc[i].text.replace(',','').replace('\n',' '))
dt_lake['Weekday_vs_Weekend']=weekend_vs_weekend
dt_lake= dt_lake.set_index('month')
dt_lake.drop(columns=['date','text'],inplace=True)
dt_lake['date'] = date
dt_lake['text'] = txt
dt_lake.to_csv('./bucket/etl/transformed_db.csv')