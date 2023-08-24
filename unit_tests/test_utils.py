import sys
sys.path.insert(1,'../src/')
import utils.general_tools as gt
import pandas as pd

def test_general_tools():
    gt.analyze_date_string('2/15/2017')
    gt.make_txt_NLP_friendly("I rather have pizza.")
    gt.make_dataframe_empty(pd.DataFrame([[1,3],[2,3]],columns=['red','blue']))
