import pandas as pd
config = pd.read_csv('../bucket/config/config.csv',index_col=0)
import sys
sys.path.insert(1,'../src/')
import data_quality_monitoring.data_quality_monitoring as dqm

def test_data_quality_monitoring():
    dqm.check_data_post_etl_and_featureEng()
    dqm.check_embeddings_dataset(file_location='../bucket/iphone6_post_etl_and_featureEng/full_dataset_embeddings.csv')
    dqm.check_chatGPT_opinion()
