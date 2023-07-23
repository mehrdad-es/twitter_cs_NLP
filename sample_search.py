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
import sys
from update_cron_parameter import update_cron_parameter as update_cron
import general_tools as gt

config= pd.read_csv('./config.csv',index_col=0)

'''
ADD LOOP FUNCTIONALITY 

'''



def get_phone_tweets(phone_model,start_date,end_date):
    end_datetime=gt.analyze_date_string(end_date)
    start_datetime=gt.analyze_date_string(start_date)
    end_year,end_month,end_day=end_datetime['year'],end_datetime['month'],end_datetime['day']
    start_year,start_month,start_day=start_datetime['year'],start_datetime['month'],start_datetime['day']
    m = end_month-start_month
    time_start=time.time()
    df = pd.read_csv(config.loc['iphone6_scan_summary'][0],index_col=0)
    tw_db = pd.read_csv(config.loc['iphone6_tweets_repository'][0])
    # print(df.shape)
    date = dt.datetime.now().strftime('%Y %m %d | %H:%M')
    try:
        # m+=8
        # year = m//12+2016
        # # year_0= (m-1)//12 + 2017
        # month = m%12+1
        # # month_0=(m-1)%12
        # m_day = cl.monthrange(year,month)[1]

        # using export command to get username,id,unq and password
        eml = os.environ.get('email')
        usr=os.environ.get('username')
        psw=os.environ.get('password')
        unq=os.environ.get('unexpected_twitter_login_code')

        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--headless=new")
        service = Service(executable_path="./chromedriver")
        driver = webdriver.Chrome(service=service,options=chrome_options)
        driver.get('https://twitter.com/') #sometimes another page shows up requiring different login#betterENG
        
        print('opened twitter.com')
        driver.implicitly_wait(15)
        # login = driver.find_element(By.XPATH, '//span[contains(text(),"Log in")]')
        # login.click()
        time.sleep(2) # for popup to load cause it can be unreliable
        popup=driver.find_element(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog' and contains(.,'Sign in')]")
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

        print('Logged into twitter')
        if  len(driver.find_elements(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog' and contains(.,'Sign in')]"))>0:
            input = popup.find_element(By.TAG_NAME,'input')
            input.send_keys(unq)
            # driver.save_screenshot('/home/green/bucket/see.png')
            input.send_keys(Keys.ENTER)
        explore=driver.find_element(By.CSS_SELECTOR,'a[href="/explore"][aria-label="Search and explore"]')
        #width of the ec2 instance is 700px while height is 400px
        if explore.size!=0:
            # print(explore.size,explore.is_displayed())
            explore.click()
            input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
        else:
            input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
        advanced_search=f'"{phone_model}" (lang:en) until:{end_year}-{end_month}-{end_day} since:{start_year}-{start_month}-{start_day}'
        input.send_keys(advanced_search)
        input.send_keys(Keys.ENTER)
        latest = driver.find_element(By.CSS_SELECTOR,'a[href^="/search?q"][role="tab"][href$="f=live"]')
        latest.click()
        repo=[]
        y_0=driver.execute_script("return document.body.scrollHeight")
        count=0

        # print(advanced_search)
        # print('before loop')
        if_no_articles=bool(len(driver.find_elements(By.XPATH,f'//div[contains(.,"No results for") and contains(.,"Try searching for something else")]')))
        if if_no_articles==False:
            while True:
                count+=1
                driver.execute_script("window.scrollTo(0, {});".format(count*y_0))
                time.sleep(3)
                y_1= driver.execute_script("return document.body.scrollHeight")
                tweet_elements=driver.find_elements(By.TAG_NAME,'article')
                for i in range(len(tweet_elements)):
                    text=''
                    text_elm=tweet_elements[i].find_element(By.CSS_SELECTOR,'div[data-testid="tweetText"]')
                    for j in range(len(text_elm.find_elements(By.TAG_NAME,'span'))):
                        text += text_elm.find_elements(By.TAG_NAME,'span')[j].text 
                    # print(text)
                    row = tweet_elements[i].text.split('\n')[:4]
                    print(row)
                    if '·' not in row:
                        continue
                    else:
                        row.remove('·') # maybe change this to remove third element#betterENG
                    # print(row)
                        tw_date= dt.datetime.strptime(row[1],'%b %d, %Y')
                        row.insert(0,tw_date.month+1)
                        row.append(text)
                    # print(row,'\n',tw_date)
                    # if tw_date.year !=year or tw_date.month!=month:
                    #     break
                        if row not in repo:
                            repo.append(row)
                # if tw_date.year !=year or tw_date.month!=month:
                #     break
                # print(f'{count}, {len(repo)}, {y_0}=={y_1}')
                if y_1==y_0:
                    break
                y_0=y_1
        else:
            df.loc[start_month+1]=['success/no results',date,time.time()-time_start,'None']
            df.to_csv(config.loc['iphone6_scan_summary'][0])            
            return -1
        repo_df=pd.DataFrame(repo,index=range(tw_db.shape[0],tw_db.shape[0]+len(repo)),columns=['month','name','id','date','text'])
        # print(repo_df,'\n')
        tw_db = pd.concat([tw_db,repo_df])
        # print('\n',tw_db)
        tweets_database=tw_db.set_index('month')
        # print('\n\n',tweets_database)
        tweets_database.to_csv(config.loc['iphone6_tweets_repository'][0])
        # print(tweets_database)#maybe figure out how to add engagement values to this dataframe
        time_end=time.time()
        process_runtime=time_end-time_start
        df.loc[m+1]= ['success',date,process_runtime,'None']
        df.to_csv(config.loc['iphone6_scan_summary'][0])
        # print(time_end-time_start)
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        df.loc[m+1]=['failure',date,time.time()-time_start,'line '+str(exc_tb.tb_lineno)+' | '+str(error)]
        df.to_csv(config.loc['iphone6_scan_summary'][0])

get_phone_tweets('iphone 6',config.loc['iphone6_tweets_start_date'][0],config.loc['iphone6_tweets_end_date'][0])

# if __name__=='__main__':
#     get_phone_tweets(sys.argv[1],sys.argv[2],sys.argv[3])

# print(iphone6_tweets_per_month(14))
# driver.quit()

#target the login button and click it
# button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
#     By.CSS_SELECTOR, "button[type='submit']"))).click()

# To learn advanced search command of twitter
#ipad "pro" (tablet) -cookie (#pricy) (from:apple) (to:apple) (@samsung) min_replies:1 min_faves:1 min_retweets:2 lang:en until:2023-01-06 since:2013-01-02