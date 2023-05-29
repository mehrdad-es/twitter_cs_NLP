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
def iphone6_tweets_per_month(m):
    m = int(m)
    time_start=time.time()
    df = pd.read_csv('cron_parameters.csv',index_col=0)
    tw_db = pd.read_csv('tweets_database.csv')
    # print(df.shape)
    date = dt.datetime.now().strftime('%Y %m %d | %H:%M')
    try:
        m-=1
        year = m//12+2017
        # year_0= (m-1)//12 + 2017
        month = m%12+1
        # month_0=(m-1)%12
        m_day = cl.monthrange(year,month)[1]

        # using export command to get username,id,unq and password
        eml = os.environ.get('eml')
        usr=os.environ.get('usr')
        psw=os.environ.get('psw')
        unq=os.environ.get('unq')

        chrome_options = ChromeOptions()
        # chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless=new")
        service = Service(executable_path="chromedriver")
        driver = webdriver.Chrome(service=service,options=chrome_options)

        driver.get('https://twitter.com/') #sometimes another page shows up requiring different login#betterENG
        # print('opened twitter.com')
        driver.implicitly_wait(15)
        login = driver.find_element(By.XPATH, '//span[contains(text(),"Log in")]')
        login.click()
        time.sleep(2) # for popup to load cause it can be unreliable
        popup=driver.find_element(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog' and contains(.,'Sign in')]")
        username = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
        username.clear()
        username.send_keys(eml)
        username.send_keys(Keys.ENTER) #change this selecting next button #betterENG
        time.sleep(3) #for selenium to update what popup is
        #print(popup.get_attribute('innerHTML'))
        if 'There was unusual' in popup.text:
            input=driver.find_element(By.CSS_SELECTOR,'input[name="text"]')#betterENG
            input.send_keys(usr)
            input.send_keys(Keys.ENTER)
        password=driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
        password.send_keys(psw)
        driver.find_element(By.CSS_SELECTOR,'div[role="button"][data-testid="LoginForm_Login_Button"]').click()
        time.sleep(3)
        # print('Logged into twitter')
        # driver.save_screenshot('/home/green/bucket/afterLogin.png')

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
        advanced_search=f'"iPhone 6" (bend) (bent) (lang:en) until:{year}-{month}-{m_day} since:{year}-{month}-01'
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
                    # print(row)
                    row.remove('·') # maybe change this to remove third element#betterENG
                    # print(row)
                    row.insert(0,m+1)
                    row.append(text)
                    tw_date= dt.datetime.strptime(row[3],'%b %d, %Y')
                    # print(row,'\n',tw_date)
                    if tw_date.year !=year or tw_date.month!=month:
                        break
                    if row not in repo:
                        repo.append(row)
                if tw_date.year !=year or tw_date.month!=month:
                    break
                # print(f'{count}, {len(repo)}, {y_0}=={y_1}')
                if y_1==y_0:
                    break
                y_0=y_1
        else:
            df.loc[m+1]=['success/no results',date,time.time()-time_start,'None']
            df.to_csv('cron_parameters.csv')            
            return -1
        repo_df=pd.DataFrame(repo,index=range(tw_db.shape[0],tw_db.shape[0]+len(repo)),columns=['month','name','id','date','text'])
        # print(repo_df,'\n')
        tw_db = pd.concat([tw_db,repo_df])
        # print('\n',tw_db)
        tweets_database=tw_db.set_index('month')
        # print('\n\n',tweets_database)
        tweets_database.to_csv('tweets_database.csv')
        # print(tweets_database)#maybe figure out how to add engagement values to this dataframe
        time_end=time.time()
        process_runtime=time_end-time_start
        df.loc[m+1]= ['success',date,process_runtime,'None']
        df.to_csv('cron_parameters.csv')
        # print(time_end-time_start)
    except Exception as error:
        df.loc[m+1]=['failure',date,time.time()-time_start,error]
        df.to_csv('cron_parameters.csv')

if __name__=='__main__':
    iphone6_tweets_per_month(sys.argv[1])

# print(iphone6_tweets_per_month(14))
# driver.quit()

#target the login button and click it
# button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
#     By.CSS_SELECTOR, "button[type='submit']"))).click()

# To learn advanced search command of twitter
#ipad "pro" (tablet) -cookie (#pricy) (from:apple) (to:apple) (@samsung) min_replies:1 min_faves:1 min_retweets:2 lang:en until:2023-01-06 since:2013-01-02