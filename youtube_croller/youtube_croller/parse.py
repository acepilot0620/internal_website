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

    def __init__(self,channel_name, subscriber_num,not_int_subscriber_num, channel_avg_visit_num, profile_url):
        self.channel_name = channel_name
        self.subscriber_num = subscriber_num
        self.not_int_subscriber_num = not_int_subscriber_num
        self.channel_avg_visit_num = channel_avg_visit_num
        self.profile_url = profile_url

def croller(search):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    # Youtube 접속
    #driver = webdriver.Chrome('C:/Users/acepi/Downloads/chromedriver.exe', chrome_options = chrome_options) # 로컬에서 돌릴때
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options = chrome_options) #NAS에서 돌릴 때
    driver.get('https://www.youtube.com/')
    driver.implicitly_wait(1)


    # 검색
    youtube_search = search
    search_url = urllib.parse.quote(youtube_search)
    #필터를 채널, 조회순 정렬로 변경하면서 검색
    driver.get('https://www.youtube.com/results?search_query='+search_url+'&sp=CAMSAhAB')
    time.sleep(1)


    # 계정 이름 리스트
    channel_name_list = []

    # 동영상 목록 리스트
    ten_video_visit_num_list = []

    # 최근 10개 동영상 평균 조회수 리스트
    channel_avg_visit_num = []

    # 구독자 수 리스트
    subscriber_num_list = []

    # 조회수 리스트
    visit_num_list = []

    # 채널 프로필 URL 리스트
    profile_url_list = []

    # 채널 프로필 url 리스트
    channel_url_list = []

    not_int_subscriber_num = []

    #스크롤 미리 내려서 충분한 유튜버 확보
    number_of_scroll = 15
    body = driver.find_element_by_tag_name('body')

    while number_of_scroll:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        number_of_scroll -= 1



    # 모든 동영상 리스트
    channel_list = driver.find_elements_by_xpath('//*[@id="text"]/a')
    for i in channel_list:
        channel_url_list.append(i.get_attribute('href'))

    delay =1
    
    for url in channel_url_list:
        driver.get(url)


        #채널 이름
        channel_name = driver.find_element_by_class_name('style-scope ytd-channel-name')
        if channel_name.text in channel_name_list:
            pass
        else:
            channel_name_list.append(channel_name.text)
            

            #구독자 수
            subscriber_num = driver.find_element_by_xpath('//*[@id="subscriber-count"]').text
            subscriber_num = subscriber_num[4:]
            not_int_subscriber_num.append(subscriber_num)
            subscriber_num = subscriber_num[:-1]
            if subscriber_num == '':
                subscriber_num = '  '    
            if subscriber_num[-1] == '만':
                subscriber_num = subscriber_num[:-1]
                subscriber_num = float(subscriber_num)*10000
            elif subscriber_num[-1] == '천':
                subscriber_num = subscriber_num[:-1]
                subscriber_num = float(subscriber_num)*1000
            elif subscriber_num[-1] == ' ':
                subscriber_num = 0
            else:
                subscriber_num = float(subscriber_num)        

            subscriber_num_list.append(subscriber_num)



            #최근 업로드 동영상 10개 평균 조회수
            to_video_list = driver.find_element_by_xpath('//*[@id="tabsContent"]/paper-tab[2]/div')
            to_video_list.click()
            time.sleep(1)

            ten_video_visit_num_object = driver.find_elements_by_xpath('//*[@id="metadata-line"]/span[1]')
            stop = 0
            for i in ten_video_visit_num_object:
                try:
                    text = i.text
                    ten_video_visit_num_list.append(text[4:-1])
                    stop += 1
                    if stop == 10:
                        break
                except StaleElementReferenceException:
                    break        

            visit_num_sum = 0
            for i in ten_video_visit_num_list:
                i = i.replace(',','')
                if i == '':
                    i = '  '    
                if i[-1] == '만':
                    i = i[:-1]
                    i = float(i)*10000
                elif i[-1] == '천':
                    i = i[:-1]
                    i = float(i)*1000
                elif i[-1] == '억':
                    i = i[:-1]
                    i = float(i)*100000000
                elif i[-1] == ' ':
                    i = 0
                else:
                    i = float(i)

                visit_num_sum += i
            
            

            avg_visit_num = visit_num_sum/len(ten_video_visit_num_list)
            #평균 10개 동영상 조회수 리스트 삽입
            channel_avg_visit_num.append(round(avg_visit_num))
            ten_video_visit_num_list = []
            visit_num_sum = 0



    result_list = []

    for i in range(len(channel_name_list)):
        new_node = Result_node(channel_name_list[i],subscriber_num_list[i],not_int_subscriber_num[i],channel_avg_visit_num[i],channel_url_list[i])
        result_list.append(new_node)



    driver.close()

    return result_list
