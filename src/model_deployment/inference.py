import pickle
import os
import openai
import sys
import warnings
from tqdm import tqdm
import time
import utils.general_tools as gt
import utils.setConfig as sc
import pandas as pd
config = pd.read_csv(f'../../bucket/config/{sc.select_data_folder()}',index_col=0)
warnings.simplefilter("ignore")

def model_inference(bearer_token,\
                    model_pickle_path,\
                    verbose=True):
    loaded_model=pickle.load(open(model_pickle_path,'rb'))
    term=input('put in your tweet text:\n')
    openai.api_key=bearer_token
    txt2vec=openai.Embedding.create(
        model="text-embedding-ada-002",
        input=term
    )
    emb= txt2vec['data'][0]['embedding']
    result = loaded_model.predict([emb])
    if verbose:
        print('1 means is product feedback and 0 mean it is not')
    print(f"output is {result[0]}")
    return result[0]

def create_inference_dataset(bearer_token,model_pickle_path,\
        emeddings_datasePath,inference_datasetPath,\
        start_from_scratch=True):
    openai.api_key=bearer_token
    loaded_model=pickle.load(open(model_pickle_path,'rb'))
    embeddings=pd.read_csv(emeddings_datasePath,index_col=0)
    inference_dataset=pd.read_csv(inference_datasetPath,index_col=0)
    if start_from_scratch:
        inference_dataset=gt.make_dataframe_empty(inference_dataset)
    for i in tqdm(range(inference_dataset.shape[0],embeddings.shape[0])):
        emb = embeddings.loc[i]
        # print(emb)
        inference_dataset.loc[i]=loaded_model.predict([emb])
        time.sleep(0.5) # this is for not breaching openai api hit rate limit; this depends on one's openai payment plan
        if i%50==0:# essentially a checkpoint where it saves embeddings every 50 iterations 
                pd.DataFrame(inference_dataset).to_csv(\
                inference_datasetPath)
    pd.DataFrame(inference_dataset).to_csv(\
            inference_datasetPath)

