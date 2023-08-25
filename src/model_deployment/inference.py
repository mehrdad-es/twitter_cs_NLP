import pickle
import os
import openai
import sys
import warnings

warnings.simplefilter("ignore")

def model_inference(bearer_token=os.environ.get('bearer_token'),\
                    model_pickle_path='./label_spread_rbf_with_ChatGPT.sav',\
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

if __name__=='__main__':
    model_inference()
