import sys
sys.path.insert(1,'../src/')
import etl.etl as etl
import pandas as pd

config = pd.read_csv('../bucket/config/config.csv',index_col=0)

def test_etl():
    p_e=etl.perform_etl()
    post_data=etl.feature_addition(p_e)
    etl.save_post_etl_and_featureEng(post_data)