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
driver.get("https://twitter.com/afrowatch199/status/1498577623424897026")

# wait for page to load
# element = WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]')))
# print(driver.page_source)

driver.implicitly_wait(10)

names_of_publisher = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))
main_publisher = names_of_publisher[0].text

# hashtag_list = driver.find_elements(By.CLASS_NAME,
#                                     "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(
#                                         ' ', '.'))
hashtag_list = driver.find_elements(By.CLASS_NAME,
                                    "css-901oao r-18jsvk2 r-37j5jr r-1blvdjr r-16dba41 r-vrz42v r-bcqeeo r-bnwqim r-qvutc0".replace(
                                        ' ', '.'))
print(hashtag_list[0].find_element(By.NAME, "/hashtag/WhatIsCryptoBetting?src=hashtag_click"))
hashtag = hashtag_list[0].text

number_list = driver.find_elements(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-b88u0q.r-bcqeeo.r-qvutc0")
retweets = number_list[0].text
likes = number_list[1].text

list_time = driver.find_elements(By.CLASS_NAME,
                                 "css-901oao.r-14j79pv.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-1b7u577.r-bcqeeo.r-qvutc0")
time = list_time[0].text
driver.close()
"""
for item in list2:
    print(item.text)

# hashtag
 list6 = driver.find_elements(By.CLASS_NAME, "css-1dbjc4n r-1s2bzr4".replace(' ', '.'))
for item in list6:
    list6[list6.index(item)] = item.text

    # print(item.text[0])
    print(item.text)
print(list6)

# hashtag
list5 = driver.find_elements(By.CLASS_NAME,"css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(' ', '.'))

for item in list5:
    list5[list5.index(item)] = item.text

    # print(item.text[0])
    print(item.text)
print(list5)

####### NAMES OF PUBLISHER

list1 = driver.find_elements(By.CLASS_NAME,
                             "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(' ',
                                                                                                                 '.'))

for item in list1:
    list1[list1.index(item)] = item.text

    # print(item.text[0])
    # print(item.text)
print(list1)
# <span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">@salvadorilla</span>


# gives number of replies, number of rretweets and number of likes
list2 = driver.find_elements(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-b88u0q.r-bcqeeo.r-qvutc0")
for item in list2:
    print(item.text)

##### EVERYTHING THAT IS WRITTEN ON THE TWEET
# list4 = driver.find_elements(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
# for item in list4:
#     print(item.text)

# <span class="css-901oao.css-16my406.css-bfa6kz.r-poiln3.r-bcqeeo.r-qvutc0"><span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">кіборгиня </span><img alt="💫" draggable="false" data-emoji-text="💫" src="https://abs-0.twimg.com/emoji/v2/72x72/1f4ab.png" class="r-4qtqp9 r-dflpy8 r-sjv1od r-zw8f10 r-10akycc r-h9hxbl"><img alt="🌿" draggable="false" data-emoji-text="🌿" src="https://abs-0.twimg.com/emoji/v2/72x72/1f33f.png" class="r-4qtqp9 r-dflpy8 r-sjv1od r-zw8f10 r-10akycc r-h9hxbl"></span>


# gives the date of the tweet
list3 = driver.find_elements(By.CLASS_NAME,
                             "css-901oao.r-14j79pv.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-1b7u577.r-bcqeeo.r-qvutc0")
for item in list3:
    print(item.text)

driver.close()
# from parsel import Selector
# sel = Selector(text=driver.page_source)
# parsed = []
# for item in sel.xpath("//div[contains(@class,'tw-tower')]/div[@data-target]"):
#    parsed.append({
#        'time': item.css('h3::text').get(),
#        'username': item.css('.qvutc0::text').get(),
#        'likes': item.css('. r-poiln3 r-bcqeeo r-qvutc0 ::text').get(),
#        'viewers': ''.join(item.css('.tw-media-card-stat::text').re(r'(\d+)')),
#    })

# number of messages: css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0
# num of retweets css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0

# class for the retweets logo  <div class="css-1dbjc4n r-18u37iz r-1h0z5md"><div aria-expanded="false" aria-haspopup="menu" aria-label="54042 Retweets. Retweet" role="button" tabindex="0" class="css-18t94o4 css-1dbjc4n r-1777fci r-bt1l66 r-1ny4l3l r-bztko3 r-lrvibr" data-testid="retweet"><div dir="ltr" class="css-901oao r-1awozwy r-14j79pv r-6koalj r-37j5jr r-a023e6 r-16dba41 r-1h0z5md r-rjixqe r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0" style=""><div class="css-1dbjc4n r-xoduu5"><div class="css-1dbjc4n r-1niwhzg r-sdzlij r-1p0dtai r-xoduu5 r-1d2f490 r-xf4iuw r-1ny4l3l r-u8s1d r-zchlnj r-ipm5af r-o7ynqc r-6416eg"></div><svg viewBox="0 0 24 24" aria-hidden="true" class="r-4qtqp9 r-yyyyoo r-1xvli5t r-dnmrzs r-bnwqim r-1plcrui r-lrvibr r-1hdv0qi"><g><path d="M23.77 15.67c-.292-.293-.767-.293-1.06 0l-2.22 2.22V7.65c0-2.068-1.683-3.75-3.75-3.75h-5.85c-.414 0-.75.336-.75.75s.336.75.75.75h5.85c1.24 0 2.25 1.01 2.25 2.25v10.24l-2.22-2.22c-.293-.293-.768-.293-1.06 0s-.294.768 0 1.06l3.5 3.5c.145.147.337.22.53.22s.383-.072.53-.22l3.5-3.5c.294-.292.294-.767 0-1.06zm-10.66 3.28H7.26c-1.24 0-2.25-1.01-2.25-2.25V6.46l2.22 2.22c.148.147.34.22.532.22s.384-.073.53-.22c.293-.293.293-.768 0-1.06l-3.5-3.5c-.293-.294-.768-.294-1.06 0l-3.5 3.5c-.294.292-.294.767 0 1.06s.767.293 1.06 0l2.22-2.22V16.7c0 2.068 1.683 3.75 3.75 3.75h5.85c.414 0 .75-.336.75-.75s-.337-.75-.75-.75z"></path></g></svg></div><div class="css-1dbjc4n r-xoduu5 r-1udh08x"><span data-testid="app-text-transition-container" style="transform: translate3d(0px, 0px, 0px); transition-property: transform; transition-duration: 0.3s;"><span class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"><span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">54K</span></span></span></div></div></div></div>

# print(parsed)
"""
