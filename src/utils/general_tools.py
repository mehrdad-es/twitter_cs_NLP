import datetime as dt
import pandas as pd
import string
import contractions
import unicodedata
import os

def analyze_date_string(date_string):
    '''
    Analyze date string and return a dictionary with date vaules
    ''' 
    output = {}  
    datetime_object= dt.datetime.strptime(date_string,'%m/%d/%Y')
    return datetime_object

def make_txt_NLP_friendly(text):
    '''
    make input text NLP friendly
    '''
    punct_to_remove=string.punctuation
    return unicodedata.normalize('NFKD',contractions.fix(text.replace('\n',' ').lower().\
               translate(str.maketrans('','',punct_to_remove)))).encode('ascii','ignore').decode('utf-8','ignore')
    
def make_dataframe_empty(df):
    '''
    input: pandas dataframe
    output: empty dataframe just with the columns
    '''
    return df.head(0)

def make_data_directory_empty(main_path):
    for subfolder in os.listdir(path=main_path):
        for file in os.listdir(path=main_path+subfolder):
            make_dataframe_empty(pd.read_csv(main_path+subfolder+\
            '/'+file,index_col=0)).to_csv(main_path+subfolder+'/'+file)

