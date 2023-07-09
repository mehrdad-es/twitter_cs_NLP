import datetime as dt

def analyze_date_string(date_string):
    '''
    Analyze date string and return a dictionary with date vaules
    ''' 
    output = {}  
    datetime_object= dt.datetime.strptime(date_string,'%m/%d/%Y')
    output['year'],output['month'],output['day']=datetime_object.year,datetime_object.month,datetime_object.day
    return output
