from selenium.webdriver.chrome.service import Service
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import csv
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

def scroll_down_page(driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
    """The function will try to scroll down the page and will check the current
    and last positions as an indicator. If the current and last positions are the same after `max_attempts`
    the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
    flag will be returned as `True`"""
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region

def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['User', 'Handle', 'PostDate', 'TweetText', 'ReplyCount', 'RetweetCount', 'LikeCount']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)

def create_webdriver_instance():
    options = Options()
    options.headless = True  # hide GUI
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")

    PATH = "/home/maya/Desktop/chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)

    return driver

def change_page_sort(tab_name, driver):
    """Options for this program are `Latest` and `Top`"""
    tab = driver.find_element_by_link_text(tab_name)
    tab.click()

def collect_all_tweets_from_current_view(driver, lookback_limit=25):
    """The page is continously loaded, so as you scroll down the number of tweets returned by this function will
     continue to grow. To limit the risk of 're-processing' the same tweet over and over again, you can set the
     `lookback_limit` to only process the last `x` number of tweets extracted from the page in each iteration.
     You may need to play around with this number to get something that works for you. I've set the default
     based on my computer settings and internet speed, etc..."""
    page_cards = driver.find_elements(By.XPATH,'//div[@data-testid="tweet"]')
    if len(page_cards) <= lookback_limit:
        return page_cards
    else:
        return page_cards[-lookback_limit:]

def main(username, password, search_term, filepath, page_sort='Top'):
    save_tweet_data_to_csv(None, filepath, 'w')  # create file for saving records
    last_position = None
    end_of_scroll_region = False
    unique_tweets = set()

    driver = create_webdriver_instance()
    # logged_in = login_to_twitter(username, password, driver)
    # if not logged_in:
    #     return

    # search_found = find_search_input_and_enter_criteria(search_term, driver)
    # if not search_found:
    #     return
    driver.get('https://twitter.com/search?q=' + search_term)
    #change_page_sort(page_sort, driver)

    list_main_publisher = []
    list_hashtags = []
    list_pages = []
    list_links = []
    list_number_reply = []
    list_number_retweet = []
    list_number_Like = []
    list_times = []
    while not end_of_scroll_region:

        ####            NAMES OF PUBLISHER

        names_of_publisher = driver.find_elements(By.CLASS_NAME,
                                                  "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                                      ' ', '.'))

        for i in range(len(names_of_publisher)):
            list_main_publisher.append(names_of_publisher[i].text)
            # print(names_of_publisher[i].text)




        ####                TEXT INFO

        text_info = driver.find_elements(By.CLASS_NAME,
                                         "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0".replace(
                                             ' ', '.'))

        for i in range(len(text_info)):
            hashtag_list = text_info[i].find_elements(By.CLASS_NAME,
                                                      "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(
                                                          ' ', '.'))
            list_ezer_hashtag = []
            list_ezer_pages = []
            list_ezer_links = []
            for element in hashtag_list:
                if '#' in element.text:
                    list_ezer_hashtag.append(element.text)
                    break
                if '@' in element.text:
                    list_pages.append(element.text)
                    break
                list_links.append(element.text)
            # print(list_ezer)
            list_hashtags.append(list_ezer_hashtag)
            list_pages.append(list_ezer_pages)
            list_links.append(list_ezer_links)




        ####            NUMBERS OF REPLIES, RETWEETS AND LIKES

        number_info = driver.find_elements(By.CLASS_NAME,
                                           "css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws".replace(' ',
                                                                                                                   '.'))

        for i in range(len(number_info)):
            numbers_list = number_info[i].find_elements(By.CLASS_NAME,
                                                        "css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0".replace(
                                                            ' ', '.'))
            list_number_reply.append(numbers_list[0].text)
            list_number_retweet.append(numbers_list[1].text)
            list_number_Like.append(numbers_list[2].text)





        ####       DATES


        TIMES = driver.find_elements(By.TAG_NAME, 'time')
        list_times = []
        for item in TIMES:
            time = item.get_attribute('datetime')
            time = time.replace('T', ' ')
            list_times.append(time.replace('Z', ' '))
        


        #list_time = driver.find_elements(By.CLASS_NAME,
        #                                 "css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0".replace(
        #                                     ' ', '.'))

        #for i in range(len(list_time)):
        #    list_times.append(list_time[i].text)
            # print(list_time[i].text)




        ####           NUMBER OF IMAGES

        list_tweet = driver.find_elements(By.CLASS_NAME,
                                          "css-1dbjc4n r-1ets6dv r-1867qdf r-1phboty r-rs99b7 r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg".replace(
                                              ' ', '.'))
        list_images = []


        for i in list_tweet:
            images_for_tweet = i.find_elements(By.TAG_NAME, "img")
            list_images.append(len(images_for_tweet))








        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)





    rows = zip(list_main_publisher, list_hashtags, list_pages, list_links, list_number_reply, list_number_retweet, list_number_Like,list_times, list_images)
    #rows = zip(list_main_publisher)

    with open("file.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    driver.quit()

if __name__ == '__main__':
    usr = "mayayank95@gmail.com"
    pwd = "MSmaya2035"
    path = 'pysimplegui.csv'
    term = 'GoodNews'#'pysimplegui'

    main(usr, pwd, term, path)
'''
names_of_publisher = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))
list_main_publisher = []
for i in range(len(names_of_publisher)):
    list_main_publisher.append(names_of_publisher[i].text)
    # print(names_of_publisher[i].text)

text_info = driver.find_elements(By.CLASS_NAME,"css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0".replace(' ', '.'))
list_hashtags = []
for i in range(len(text_info)):
    hashtag_list = text_info[i].find_elements(By.CLASS_NAME,
                                   "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(
                                       ' ', '.'))
    list_ezer=[]
    for j in range(len(hashtag_list)):
        list_ezer.append(hashtag_list[j].text)
    # print(list_ezer)
    list_hashtags.append(list_ezer)

number_info = driver.find_elements(By.CLASS_NAME,"css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws".replace(' ', '.'))
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
                                 "css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0".replace(' ', '.'))
list_times = []
for i in range(len(list_time)):
    list_main_publisher.append(list_time[i].text)
    print(list_time[i].text)

driver.close()
'''