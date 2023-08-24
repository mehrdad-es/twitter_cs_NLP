import pandas as pd
config = pd.read_csv('../bucket/config/config.csv',index_col=0)
import sys
sys.path.insert(1,'../src/')
import model_development.model_development as mdv
import model_development.generate_embeddings as gmb
import os
 
def test_model_development():
    gmb.gen_emb(os.environ.get('bearer_token'),\
        '../bucket/iphone6_post_etl_and_featureEng/full_dataset_embeddings.csv')
    gmb.gen_chatGPT_opinion(os.environ.get('bearer_token'))
    mdv.create_data_split()


