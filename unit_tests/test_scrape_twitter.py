import sys
sys.path.insert(1,'../src/')
import scraper_twitter.get_tweets as get_tweets
import pytest
import os

def test_get_tweets():
    '''
    Since the following functions don't return anything
    you have to look at them visually and validate.
    '''
    driver=get_tweets.initiate_chrome()
    eml = os.environ.get('email')
    usr=os.environ.get('username')
    psw=os.environ.get('password')
    unq=os.environ.get('unexpected_twitter_login_code')
    get_tweets.login_to_twitter(driver,eml,usr,psw,unq)
    get_tweets.scrape_twitter(driver,'3/3/2017','iphone 6',threshold=2)
