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
from PIL import Image

time_start=time.time()

# using export command to get username,id,unq and password
eml = os.environ.get('eml')
usr=os.environ.get('usr')
psw=os.environ.get('psw')
unq=os.environ.get('unq')
#print(eml)

chrome_options = ChromeOptions()
#chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless=new")
service = Service(executable_path="chromedriver")
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get('https://twitter.com/') #sometimes another page shows up requiring different login#betterENG
#driver.maximize_window()
print('opened twitter.com')
driver.implicitly_wait(15)
login = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="login"]')
login.click()
time.sleep(2) # for popup to load cause it can be unreliable
popup=driver.find_element(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog' and contains(.,'Sign in')]")
username = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
username.clear()
username.send_keys(eml)
username.send_keys(Keys.ENTER) #change this selecting next button #betterENG
time.sleep(5) #for selenium to update what popup is
#print(popup.get_attribute('innerHTML'))
if 'There was unusual' in popup.text:
    input=driver.find_element(By.CSS_SELECTOR,'input[name="text"]')#betterENG
    input.send_keys(usr)
    input.send_keys(Keys.ENTER)
password=driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
password.send_keys(psw)
driver.find_element(By.CSS_SELECTOR,'div[role="button"][data-testid="LoginForm_Login_Button"]').click()
time.sleep(5)
print('Logged into twitter')
driver.save_screenshot('/home/green/bucket/afterLogin.png')

if  len(driver.find_elements(By.XPATH,"//div[@aria-labelledby='modal-header' and @role='dialog' and contains(.,'Sign in')]"))>0:
    input = popup.find_element(By.TAG_NAME,'input')
    input.send_keys(unq)
    driver.save_screenshot('/home/green/bucket/see.png')
    input.send_keys(Keys.ENTER)
explore=driver.find_element(By.CSS_SELECTOR,'a[href="/explore"][aria-label="Search and explore"]')
#print(driver.find_element(By.TAG_NAME,'body').get_attribute('innerHTML'))
x=driver.execute_script("return document.body.scrollWidth")
print(x)
#width of the ec2 instance is 700px while height is 400px
time.sleep(3)

if explore.size!=0:
    print(explore.size,explore.is_displayed())
    #explore = explore.find_element(By.TAG_NAME,'div')
    explore.click()
    input = input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
else:
    input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search query"]')
input.send_keys('"iPhone 6" (bend) (bent) (lang:en) until:2015-12-31 since:2014-01-01')
input.send_keys(Keys.ENTER)
latest = driver.find_element(By.CSS_SELECTOR,'a[href^="/search?q"][role="tab"][href$="f=live"]')
latest.click()
repo=[]
y=driver.execute_script("return document.body.scrollHeight")
print(y)
for j in range(3):
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, {});".format(j*y))
    time.sleep(3)
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
        row.append(text)    
        repo.append(row)
tweets_database=pd.DataFrame(repo,columns=['name','id','date','text'])
print(tweets_database)#maybe figure out how to add engagement values to this dataframe
time_end=time.time()
print(time_end-time_start)
time.sleep(5)
# driver.quit()

#target the login button and click it
# button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
#     By.CSS_SELECTOR, "button[type='submit']"))).click()

# To learn advanced search command of twitter
#ipad "pro" (tablet) -cookie (#pricy) (from:apple) (to:apple) (@samsung) min_replies:1 min_faves:1 min_retweets:2 lang:en until:2023-01-06 since:2013-01-02