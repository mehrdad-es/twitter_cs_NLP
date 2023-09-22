from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import sys   
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import os    
import pandas as pd
import datetime as dt
import calendar as cl
import utils.general_tools as gt
import utils.setConfig as setConfig
import re

def initiate_chrome(use_existing_profile=False,headless=False):
    '''
    opens a chrome instance and returns a driver instance. Note that local chrome version and the chromedriver
    in the working directory should match. Also note that selenium webscraping 
    is finicky and needs continuous updating due to code changes or front end changes 
    on the website being scraped. 
    '''
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless=new") # so chrome doesn't open every single time
    if use_existing_profile:
        chrome_options.add_argument("--remote-debugging-port=9014")#opens created profile not to login again
        # chrome_options.add_experimental_option("debuggerAddress","localhost:9014") # alternative way to decalre port for created profile
        cwd=os.getcwd()
        chrome_options.add_argument(f'--user-data-dir={cwd}/tw_profile')#better change to absolute path if encountered errors # this line opens your profile which is already logged into twitter
    chrome_options.add_experimental_option("detach", True) # to sometimes help with chrome tab stay open 
    service = Service(executable_path="../../chromedriver")
    driver=webdriver.Chrome(service=service,options=chrome_options)
    return driver

def login_to_twitter(driver,eml,usr,psw,unq):
    '''
    logins to twitter with the credentials provided (this could be done with environment
    variables). See below:
    eml = os.environ.get('email')
    usr=os.environ.get('username')
    psw=os.environ.get('password')
    unq=os.environ.get('unexpected_twitter_login_code')


    eml is email, usr is username, psw is password, unq is the unique code twitter
    sends in case it notices suspicious logins to your account(it also happens 
    when you login too many times into your twitter account).
    '''
    driver.get('https://twitter.com/')
    driver.implicitly_wait(15)
    # login = driver.find_element(By.XPATH, '//span[contains(text(),"Log in")]')
    # login.click()
    time.sleep(2) # for popup to load cause it can be unreliable
    main=driver.find_element(By.XPATH,"//main[@role='main']")
    sign_in=main.find_element(By.XPATH,'./div/div/div[1]/div[1]/div/div[3]/div[5]/a/div')
    sign_in.click()
    popup=driver.find_element(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog']")
    username = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
    username.clear()
    username.send_keys(eml)
    username.send_keys(Keys.ENTER) #change this selecting next button #betterENG
    time.sleep(2) #for selenium to update what popup is
    if 'There was unusual' in popup.text:
        input=driver.find_element(By.CSS_SELECTOR,'input[name="text"]')#betterENG
        input.send_keys(usr)
        input.send_keys(Keys.ENTER)
    password=driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
    password.send_keys(psw)
    driver.find_element(By.CSS_SELECTOR,'div[role="button"][data-testid="LoginForm_Login_Button"]').click()
    time.sleep(2)
    # print('Logged into twitter')

def find_tweets(driver,date,exact_search_term='iphone 6',threshold=20,num_days=1,
        minRetweets=1):
    '''
    input: takes in driver instance, date to get tweets from,search term, number of days
    ahead it can search for tweets and threshold for number of tweets to get.
    minRetweets is a parameter used to fine-tune the search.
    Note that date should be in numerical for all month/day/year format.

    output: gets the tweets and stores in main repository for the tweets, the success/no-results/failure
    status of scan is stored in scan summary file. The locations for these two files is stored in
    config.csv file. 
    '''

    # variable initialization
    months=['Jan ','Feb ','Mar ','Apr ','May ','Jun ','Jul ','Aug ','Sep ','Oct ','Nov ','Dec ']
    config= pd.read_csv(f'../../bucket/config/{setConfig.select_data_folder()}',index_col=0)
    phone_model,date=exact_search_term,gt.analyze_date_string(date)
    day_after = date+dt.timedelta(days=num_days)
    year,month,day=date.year,date.month,date.day
    day_after_year,day_after_month,day_after_day=day_after.year,day_after.month,day_after.day
    scan_summary = pd.read_csv(config.loc['scan_summary'][0])
    all_tweets_repo = pd.read_csv(config.loc['tweets_repository'][0])
    today = dt.datetime.now().strftime('%Y %m %d | %H:%M')
    repo=[]
    time_start=time.time()

    #scrape twitter
    try: # implemented specifically due to scraping twitter being finicky    
        driver.get('https://twitter.com')
        time.sleep(2)
        explore=driver.find_element(By.CSS_SELECTOR,'a[href="/explore"][aria-label="Search and explore"]')
        #width of the ec2 instance is 700px while height is 400px
        if explore.size!=0:
            # print(explore.size,explore.is_displayed())
            explore.click()
            input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
        else:
            input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
        advanced_search=f'"{phone_model}" min_retweets:{minRetweets} (lang:en) until:{day_after_year}-{day_after_month}-{day_after_day} since:{year}-{month}-{day}'
        input.send_keys(advanced_search)
        input.send_keys(Keys.ENTER)
        latest = driver.find_element(By.CSS_SELECTOR,'a[href^="/search?q"][role="tab"][href$="f=live"]')
        latest.click()
        y_0=driver.execute_script("return document.body.scrollHeight")
        count=0
        count2=1
        if_no_articles=bool(len(driver.find_elements(By.XPATH,f'//div[contains(.,"No results for") and contains(.,"Try searching for something else")]')))
        if if_no_articles==False:
            while count2<=threshold:
                print('{}% has been done'.format(round(count2/threshold,2)*100))
                tweet_elements=driver.find_elements(By.TAG_NAME,'article')
                for i in range(len(tweet_elements)):
                    if tweet_elements[i].text=='This Tweet is unavailable.':
                        continue
                    text=''
                    elements=tweet_elements[i].text.split('\n')
                    if '·' not in elements[:4]: #identifies ad posts
                        continue
                    else:
                        elements.remove('·')
                        for k in range(1,len(elements)):
                                if elements[k][:4] in months or \
                                    bool(re.compile('\A[0-2][0-9]h').match(elements[k])):
                                    date_index= k
                                    break
                        for j in range(date_index+1,len(elements)):
                            text+=elements[j]    
                        row = elements[:date_index+1]
                        row[date_index]=tweet_elements[i].find_element(By.TAG_NAME,'time').get_attribute('datetime')[:10]
                        tw_date= dt.datetime.strptime(row[date_index],'%Y-%m-%d').strftime("%b %d, %Y")
                        if len(row)==2:
                            row.insert(0,'No Name')    
                        row.append(text)
                        if (row not in repo) and (row not in all_tweets_repo.values.tolist()):
                            repo.append(row)
                            count2+=1
                    if count2>threshold:
                        break
                count+=1
                driver.execute_script("window.scrollTo(0, {});".format(count*y_0))
                time.sleep(3)
                if_pls_retry=bool(len(driver.find_elements(By.XPATH,f'//div[contains(.,"Something went wrong. Try reloading") and contains(.,"Retry")]')))
                if if_pls_retry:
                    time.sleep(900)
                    driver.find_element(By.XPATH,f'//div[@role="button" and contains(.,"Retry")]').click()
                y_1= driver.execute_script("return document.body.scrollHeight")
                if y_1==y_0:
                    time_of_break = time.time()
                    break
                y_0=y_1      
        else:
            scan_summary.loc[scan_summary.shape[0]]=['success/no results',today,time.time()-time_start,'n/a']
            scan_summary.to_csv(config.loc['scan_summary'][0])            
            # print('break')
        repo_df=pd.DataFrame(repo,columns=['name','id','date','text'])
        all_tweets_repo = pd.concat([all_tweets_repo,repo_df],ignore_index=True)
        all_tweets_repo.to_csv(config.loc['tweets_repository'][0],index=False)
        time_end=time.time()
        process_runtime=time_end-time_start
        scan_summary.loc[scan_summary.shape[0]]= ['success',today,process_runtime,'n/a']
        scan_summary.to_csv(config.loc['scan_summary'][0],index=False)
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        scan_summary.loc[scan_summary.shape[0]]=['failure',date,time.time()-time_start,'line '+str(exc_tb.tb_lineno)+' | '+str(error)]
        scan_summary.to_csv(config.loc['scan_summary'][0])