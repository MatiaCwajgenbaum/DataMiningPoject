import sys
from Tweets_Extractor import *


def main(search_term, path_web, quantity_of_tweets, path_file):
    tweets = Tweets_extractor(search_term, path_web, quantity_of_tweets, path_file)
    driver = tweets.initialize_driver()
    tweets.Extract_ALL(driver)
    driver.quit()


if __name__ == '__main__':
    term = sys.argv[1]  # 'GoodNews'  # #'GoodNews'#'pysimplegui'
    number_of_tweets = sys.argv[2]
    pathweb = sys.argv[3]
    if len(sys.argv) == 5:
        pathfile = sys.argv[4]
    else:
        pathfile = term + '.csv'

    main(term, pathweb, number_of_tweets, pathfile)
