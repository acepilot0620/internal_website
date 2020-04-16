from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import requests
import time



def insta_login(celly_id, celly_pw):

    chrome_options = webdriver.ChromeOptions()

    # Instagram 자동로그인
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options = chrome_options) #NAS에 올릴 때
    driver = webdriver.Chrome('/Users/choijungho/Downloads/chromedriver', chrome_options = chrome_options) # 로컬에서 돌릴때
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    driver.implicitly_wait(1)
    email = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
    email.send_keys(celly_id)
    password = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
    password.send_keys(celly_pw,Keys.ENTER)