import datetime as dt

import string
import contractions
import unicodedata

def analyze_date_string(date_string):
    '''
    Analyze date string and return a dictionary with date vaules
    ''' 
    output = {}  
    datetime_object= dt.datetime.strptime(date_string,'%m/%d/%Y')
    return datetime_object

def make_txt_NLP_friendly(text):
    punct_to_remove=string.punctuation
    unicodedata.normalize('NFKD',contractions.fix(text.replace('\n',' ').lower().\
               translate(str.maketrans('','',punct_to_remove)))).encode('ascii','ignore').decode('utf-8','ignore')

