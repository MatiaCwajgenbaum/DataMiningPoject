from selenium.webdriver.chrome.service import Service
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")

PATH = "/home/maya/Desktop/chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)
# driver = webdriver.Chrome()
# driver.get("https://twitter.com/search?q=%23UkraineRussiaWar&src=trend_click&vertical=trends")
# driver.get("https://twitter.com/IndiaToday/status/1498588282950717440")
driver.get("https://twitter.com/search?q=%23GoodNews&src=typeahead_click")

# wait for page to load
# element = WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]')))
# print(driver.page_source)

driver.implicitly_wait(10)

names_of_publisher = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))
list_main_publisher = []
for i in range(len(names_of_publisher)):
    list_main_publisher.append(names_of_publisher[i].text)
    # print(names_of_publisher[i].text)

text_info = driver.find_elements(By.CLASS_NAME,
                                 "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0".replace(
                                     ' ', '.'))
list_hashtags = []
for i in range(len(text_info)):
    hashtag_list = text_info[i].find_elements(By.CLASS_NAME,
                                              "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(
                                                  ' ', '.'))
    list_ezer = []
    for j in range(len(hashtag_list)):
        list_ezer.append(hashtag_list[j].text)
    # print(list_ezer)
    list_hashtags.append(list_ezer)

number_info = driver.find_elements(By.CLASS_NAME,
                                   "css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws".replace(' ', '.'))
list_number_reply = []
list_number_retweet = []
list_number_Like = []

for i in range(len(number_info)):
    numbers_list = number_info[i].find_elements(By.CLASS_NAME,
                                                "css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0".replace(
                                                    ' ', '.'))
    list_number_reply.append(numbers_list[0].text)
    list_number_retweet.append(numbers_list[1].text)
    list_number_Like.append(numbers_list[2].text)

list_time = driver.find_elements(By.CLASS_NAME,
                                 "css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0".replace(
                                     ' ', '.'))
list_times = []
for i in range(len(list_time)):
    list_main_publisher.append(list_time[i].text)
    print(list_time[i].text)

driver.close()
