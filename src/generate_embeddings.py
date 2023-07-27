import openai
import os
import pandas as pd
import time
import sys
import scipy
import string
import contractions
import unicodedata
import general_tools as gt

config = pd.read_csv('../bucket/config/config.csv',index_col=0)

def gen_emb(openai_api_bearer_token,\
            embeddings_path,\
            start_from_scratch=True,\
            dataset_path=config.loc['iphone6_data_post_etl_and_featureEng'][0]):
    '''
    input: openai bearer token, embeddings path, dataset path, and boolean to 
    to see if the embeddings should be appended to or refilled from scratch.

    bearer token can also be loaded with environment variables.
    
    gets embeddings for each row in dataset and appends to embeddings file.
    '''
    openai.api_key= openai_api_bearer_token
    dataset = pd.read_csv(dataset_path)
    embeddings=pd.read_csv(embeddings_path,index_col=0)
    if start_from_scratch:
        embeddings=gt.make_dataframe_empty(embeddings)
    for i in range(embeddings.shape[0],dataset.shape[0]):
        start = time.time()
        term = str(list(dataset.loc[i])) # giving the list with its brackets in string format found to make the most sense
        # print(i, term)
        txt2vec=openai.Embedding.create(
                model="text-embedding-ada-002",
                input=term
        )
        emb= txt2vec['data'][0]['embedding']
        embeddings.loc[i]=emb
        end = time.time()
        time.sleep(0.5) # this is for not breaching openai api hit rate limit; this depends on one's openai payment plan
        if i%50==0:# essentially a checkpoint where it saves embeddings every 50 iterations 
                pd.DataFrame(embeddings).to_csv(\
                embeddings_path)
    pd.DataFrame(embeddings).to_csv(\
            embeddings_path)
    
def gen_chatGPT_opinion(openai_api_bearer_token,\
            opinions_path=config.loc['iphone6_ChatGPT_opinion'][0],\
            start_from_scratch=True,\
            dataset_path=config.loc['iphone6_data_post_etl_and_featureEng'][0],\
            exact_search_term='iphone 6'):
    '''
    input: openai bearer token, opinion path, dataset path, and boolean to 
    to see if the opinions should be appended to or refilled from scratch.

    bearer token can also be loaded with environment variables.

    Note that chatGPT opinion runs about 10times slower than embedding generation
    and is prone to server errors due to high demand of the service.
    
    gets opinion for each row in dataset and appends to opinion file.
    '''
    openai.api_key= openai_api_bearer_token
    dataset = pd.read_csv(dataset_path)
    chatGPT_opinions=pd.read_csv(opinions_path,index_col=0)
    if start_from_scratch:
        chatGPT_opinions=gt.make_dataframe_empty(chatGPT_opinions)
    for i in range(chatGPT_opinions.shape[0],dataset.shape[0]):
        start = time.time()
        tweet=dataset.loc[i].text
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are an unbiased smartphone product analyst"},
                {"role": "user", "content": "Briefly describe whether product feedback is being\
                given about {} in the following tweet: {}".format(exact_search_term,tweet)}
        ]
        )
        chatGPT_response=gt.make_txt_NLP_friendly(completion.choices[0].message.content)
        chatGPT_opinions.loc[i]=[tweet,chatGPT_response]
        # print(i,[tweet,chatGPT_response])
        end = time.time()
        time.sleep(0.5) # this is for not breaching openai api hit rate limit; this depends on one's openai payment plan
        if i%50==0:# essentially a checkpoint where it saves embeddings every 50 iterations 
            pd.DataFrame(chatGPT_opinions).to_csv(\
                opinions_path)
    pd.DataFrame(chatGPT_opinions).to_csv(\
            opinions_path)
    