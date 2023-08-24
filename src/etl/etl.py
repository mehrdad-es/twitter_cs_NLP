import pandas as pd
import datetime as dt
import calendar
import string
import contractions
import unicodedata
import sklearn as sk

config = pd.read_csv('../bucket/config/config.csv',index_col=0)

def perform_etl(file_path=config.loc['iphone6_tweets_repository'][0]):
    '''
    input:file path
    output: etl dataframe
    '''
    
    punct_to_remove=string.punctuation
    raw_data = pd.read_csv(file_path)
    raw_data=raw_data.sort_values(by='date',ascending=False).reset_index(drop=True)
    has_url=[] # technically could be part of feature engineering but because text cleanup reshapes url it is done here
    txt=[]

    #to sort by date, raw_date is three-letter-month day, year format string rather than datetime
    raw_data['date']=pd.to_datetime(raw_data['date'])
    raw_data=raw_data.sort_values(by='date',ascending=True).reset_index(drop=True)
    raw_data['date']=raw_data['date'].apply(lambda _: dt.datetime.strftime(_,'%b %d, %Y'))

    # cleaning text for NLP and checking if tweet has url
    for i in range(raw_data.shape[0]):
        has_url.append(int('http://' in raw_data.loc[i].text or 'https://' in raw_data.loc[i].text))# checks if tweets has a link
        txt.append(unicodedata.normalize('NFKD',contractions.fix(raw_data.loc[i].text.replace('\n',' ').lower().\
                translate(str.maketrans('','',punct_to_remove)))).encode('ascii','ignore').decode('utf-8','ignore'))# text cleanup 
    etl_data=raw_data.copy()
    etl_data.drop(columns=['date','text'],inplace=True) #current iteration of the model doesn't use date in feature embedding; in future iterations it should because it enhances the count_perID feature
    etl_data['text'] = txt
    etl_data['has_url']=has_url
    return etl_data

def feature_addition(etl_data):
    '''
    input: etl dataframe
    output: dataframe with features from feature engineering
    '''
    
    count_values=etl_data['id'].value_counts(sort=False)
    etl_data['tweet_count_perID_fromStart'] = [0]*etl_data.shape[0]
    for i in range(etl_data.shape[0]-1,-1,-1):
        etl_data.loc[i,'tweet_count_perID_fromStart']= count_values[etl_data.loc[i,'id']]
        count_values[etl_data.loc[i,'id']]-=1
    return etl_data

def save_post_etl_and_featureEng(data_post_etl_and_featureEng,save_path=config.loc['iphone6_data_post_etl_and_featureEng'][0]):
    '''
    input: dataframe with etl and feature engineering and save_path
    
    saves input dataframe to save_path location
    '''
    
    data_post_etl_and_featureEng.to_csv(save_path,index=False)