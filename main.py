import sys
from Tweets_Extractor import *


def main(search_term, quantity_of_tweets, path_CSVfile):
    """
    arguments: the term the user wants to type in the search bar, the num of tweets the user wants to extract
     and the path where the csv file will be created.
     Returns the csv file containing the extracted tweets and located in the path as required.
    """
    try:
        tweets = Tweets_extractor(search_term, quantity_of_tweets, path_CSVfile)
        driver = tweets.initialize_driver()
        tweets.Extract_ALL(driver)
        driver.quit()
    except ValueError as va:
        print(f'{va}, Make sure you type an integer as second argument !')
    except PermissionError as Pa:
        print(f'{Pa}, Make sure the path tou typed really exists or that you have permission to access it! !')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Sorry, you need to type at least two arguments ! 1) the text you want to search in twitter and\
    2) the number of tweets you need')
    term = sys.argv[1]  # 'GoodNews'  # #'GoodNews'#'pysimplegui'
    number_of_tweets = sys.argv[2]
    if len(sys.argv) >= 4:
        pathfile = sys.argv[3]
    else:
        pathfile = term + '.csv'
    main(term, number_of_tweets, pathfile)
