from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import requests
import time 


class Result_node():
    def __init__(self,insta_id,profile_url):
        self.insta_id = insta_id
        # self.profile_img = profile_img
        self.profile_url = profile_url

# 순서유지 LIST 중복 제거
def OrderedSet(list):
    my_set = set()
    res = []
    for e in list:
        if e not in my_set:
            res.append(e)
            my_set.add(e)

    return res

def insta_croller(search):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Instagram 자동로그인
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options = chrome_options) #NAS에 올릴 때
    #driver = webdriver.Chrome('C:/Users/acepi/Downloads/chromedriver.exe', chrome_options = chrome_options) # 로컬에서 돌릴때
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    driver.implicitly_wait(1)
    email = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
    email.send_keys("cellyapply1")
    password = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
    password.send_keys("applycelly123!",Keys.ENTER)

    first_keyword = search
    relevent_keyword_list = []
    result = []
    i = 0

    relevent_keyword_list.append(first_keyword)
    time.sleep(3)
    driver.get('https://www.instagram.com/explore/tags/'+first_keyword)
    time.sleep(1)
    relevent_keyword_obj = driver.find_elements_by_partial_link_text('#')
    for obj in relevent_keyword_obj:
        relevent_keyword_list.append(obj.text[1:])

    while True:
        try:
            keyword = relevent_keyword_list[i]
            driver.get('https://www.instagram.com/explore/tags/'+keyword)    
            url_list = []    
            for a in range(1,4):
                for b in range(1,4):
                    hot_post = WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/article/div[1]/div/div/div['+str(a)+']/div['+str(b)+']/a'))
                    )
                    url_list.append(hot_post.get_attribute('href'))
            influencer_list = []
            profile_img_list = []    
            for url in url_list:
                try:
                    driver.get(url)
                    influencer = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').text

                    if influencer not in influencer_list:
                        influencer_list.append(influencer)
                except TimeoutException:
                    pass 
            driver.get('https://www.instagram.com/explore/tags/'+keyword)
            time.sleep(2)
            relevent_keyword_obj = driver.find_elements_by_partial_link_text('#')
            for obj in relevent_keyword_obj:
                relevent_keyword_list.append(obj.text[1:])
            no_duplication_list = OrderedSet(relevent_keyword_list)
            if len(relevent_keyword_list) != len(no_duplication_list):
                relevent_keyword_list = no_duplication_list
            elif keyword == first_keyword:
                relevent_keyword_list = no_duplication_list
            else:
                break
            i += 1        
        except IndexError:
            break
        except TimeoutException:
            break
        
        influencer_list = list(set(influencer_list))

        for t in range(len(influencer_list)):
            new_node = Result_node(influencer_list[t],'https://www.instagram.com/'+influencer_list[t])
            result.append(new_node)

        if len(result) == 50:
            break
    return result, relevent_keyword_list

