import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
import os
import pandas as pd
import numpy as np
import openai
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.metrics import roc_auc_score
import pomegranate as pg
import warnings
warnings.simplefilter('ignore')
np.random.seed(1)
from tqdm import tqdm
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import sys
import utils.general_tools as gt
import utils.setConfig as sc
config = pd.read_csv(f'../../bucket/config/{sc.select_data_folder()}',index_col=0)

def create_data_split(dataset_path=config.loc['data_postETL_and_featureEng'][0],\
                    to_save=False,\
                    split_index_tuple=(.1,.9)):
    '''
    input: dataset_path, whether to save created split, split index tuple.
    split_index_tuple: slice the model at index percent 1 and 2 to create three slices
    for x_train_labled, x_train_unlabled, and x_test and the same case y data.    
    
    note that it is assumed here that initially there is no label data so it is assumed
    to be -1. This would also be important as the semi-supervised algortithm used requires
    -1 to be the value for untrained x data. 
 
    output: the splitted datasets for x and y
    '''
    dataset = pd.read_csv(dataset_path)
    dataset['label']=[-1]*dataset.shape[0]
    dataset= shuffle(dataset,random_state=1)
    label = dataset['label']
    n = dataset.shape[0]
    dataset.drop(columns=['label'],inplace=True)
    x_train_labled,x_train_unlabled,x_test=np.split(dataset,\
        [int(split_index_tuple[0]*n), int(split_index_tuple[1]*n)])
    y_train_labled,y_train_unlabled,y_test=np.split(label,\
        [int(split_index_tuple[0]*n), int(split_index_tuple[1]*n)])
    if to_save:
        x_train_unlabled.to_csv(config.loc['x_train_unlabled'][0])
        x_train_labled.to_csv(config.loc['x_train_labled'][0])
        x_test.to_csv(config.loc['x_test'][0])
        y_train_unlabled.to_csv(config.loc['y_train_unlabled'][0])
        y_train_labled.to_csv(config.loc['y_train_labled'][0])
        y_test.to_csv(config.loc['y_test'][0])

    return [(x_train_labled,x_train_unlabled,x_test),\
            (y_train_labled,y_train_unlabled,y_test)]

def label_data(x_dataset,y_dataset,y_dataset_path):
    '''
    input: x_dataset,y_dataset,y_dataset_path

    goes through each row in x_dataset and asks for label from user. Then it saves
    their response as 0 if it's not product feedback or 1 if it's product feedback.
    '''
    if x_dataset.shape[0]!=y_dataset.shape[0]:
        print('please try again, x and y are not the same number of rows')
    else:
        for i in tqdm(range(x_dataset.shape[0])):
            user_input = input(f'is | {x_dataset.iloc[i,2]} | product feedback(0=no, 1=yes)?')
            # user_input = input(f'\n{x_dataset.iloc[i,2]}\n')
            if i%5==0: #saves labels every five iterations
                y_dataset.to_csv(y_dataset_path)
            if user_input=='': # one could skip labeling by inputting nothing into input field
                continue
            else:
                y_dataset.iloc[i]=int('yes'==user_input)
        y_dataset.to_csv(y_dataset_path)

# thanks to this author https://www.kaggle.com/code/altprof/basic-semi-supervised-learning-models
def labels_spread_test(kernel, hyperparam, alphas, X_train, X_test, y_train, y_test):
    '''
    input: kernel type, hyperparameter, alphas(degree of influence from neighbors),
    x_train, x_test,y_train,y_test
    output:returns the alpha at which the roc curve is the maximum with a graph
    '''
    plt.figure(figsize=(20,10))
    n, g = 28, 40
    roc_scores = []
    if kernel == 'rbf':
        g = hyperparam
    if kernel == 'knn':
        n = hyperparam
    for alpha in alphas:
        ls = LabelSpreading(kernel=kernel, n_neighbors=n, gamma=g, alpha=alpha, max_iter=10000, tol=0.0001)
        ls.fit(X_train, y_train)
        roc_scores.append(roc_auc_score(y_test, ls.predict_proba(X_test)[:,1]))
    plt.figure(figsize=(16,8));
    plt.plot(alphas, roc_scores);
    plt.title('Label Spreading ROC AUC with ' + kernel + ' kernel')
    plt.show();
    print('Best metrics value is at {}'.format(alphas[np.argmax(roc_scores)]))

# thanks to this author https://www.kaggle.com/code/altprof/basic-semi-supervised-learning-models
def label_prop_test(kernel, params_list, X_train, X_test, y_train, y_test):
    '''
    input: kernel type, hyperparameter list,x_train, x_test,y_train,y_test
    output:returns the alpha at which the roc curve is the maximum with a graph
    '''
    plt.figure(figsize=(20,10))
    n, g = 7, 20
    roc_scores = []
    if kernel == 'rbf':
        for g in params_list:
            lp = LabelPropagation(kernel=kernel, n_neighbors=n, gamma=g, max_iter=100000, tol=0.0001)
            lp.fit(X_train, y_train)
            roc_scores.append(roc_auc_score(y_test, lp.predict_proba(X_test)[:,1]))
    if kernel == 'knn':
        for n in params_list:
            lp = LabelPropagation(kernel=kernel, n_neighbors=n, gamma=g, max_iter=100000, tol=0.0001)
            lp.fit(X_train, y_train)
            roc_scores.append(roc_auc_score(y_test, lp.predict_proba(X_test)[:,1]))
    plt.figure(figsize=(16,8));
    plt.plot(params_list, roc_scores)
    plt.title('Label Propagation ROC AUC with ' + kernel + ' kernel')
    plt.show()
    print('Best metrics value is at {}'.format(params_list[np.argmax(roc_scores)]))