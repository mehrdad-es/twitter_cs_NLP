import pandas as pd
import great_expectations as ge
import seaborn as sns
import sys

config = pd.read_csv('../bucket/config/config.csv',index_col=0)

def check_data_post_etl_and_featureEng(file_location=config.loc['iphone6_data_post_etl_and_featureEng'][0]):
    '''
    input:dataset location
    output: boolean if all the tests have passed
    '''
    
    dataset= ge.read_csv(file_location)
    meets_criteria= dataset.expect_column_distinct_values_to_be_in_set('has_url',value_set=[0,1]).success and\
    dataset.expect_column_min_to_be_between('tweet_count_perID_fromStart',strict_min=1).success and\
    dataset.expect_column_values_to_be_of_type('name',type_='str').success and\
    dataset.expect_column_values_to_be_of_type('id',type_='str').success and\
    dataset.expect_column_values_to_be_of_type('text',type_='str').success and\
    dataset.expect_column_values_to_be_of_type('has_url',type_='int').success and\
    dataset.expect_column_values_to_be_of_type('tweet_count_perID_fromStart',type_='int').success
    return meets_criteria

def check_embeddings_dataset(file_location):
    '''
    input: embeddings dataset location
    output: boolean if all the tests have passed
    '''
    dataset_embeddings = ge.read_csv(file_location,index_col=0)
    column0_type_validation=dataset_embeddings.expect_column_values_to_be_of_type('0',type_='float').success
    for i in range(1,1536):
        matched=column0_type_validation and dataset_embeddings.expect_column_values_to_be_of_type(\
            f'{str(i)}',type_='float').success
        if matched:
            multi_column_type_validation=matched
        else:
            multi_column_type_validation=matched
            break  
    meets_criteria=dataset_embeddings.expect_table_column_count_to_equal(1536).success and\
          multi_column_type_validation
    return meets_criteria

def check_chatGPT_opinion(file_location=config.loc['iphone6_ChatGPT_opinion'][0]):
    '''
    input: chatgpt opinion dataset location
    output: boolean if all the tests have passed
    '''
    chatGPT_opinions= ge.read_csv(file_location)
    meets_criteria=chatGPT_opinions.expect_column_values_to_be_of_type('text',type_='str').success and\
    chatGPT_opinions.expect_column_values_to_be_of_type('chatGPT_opinion',type_='str').success
    return meets_criteria

