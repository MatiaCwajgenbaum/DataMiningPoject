from driver import *
from one_tweet import *

from User_Extractor import *
from build_database import *

import argparse


def create_database_and_tables():
    """ create database and tables for first running """
    create_database()
    use_database()
    create_table_hashtag(LENGTH_VARCHAR)
    create_table_hashtag_tweets()
    create_table_link(LENGTH_VARCHAR)
    create_table_link_tweets()
    create_table_tweets(LENGTH_VARCHAR)
    create_table_users(LENGTH_VARCHAR)
    create_table_users_tagged_tweets()


def main(search_term, first_run, quantity_of_tweets, path_csv_file):
    """
    arguments: the term the user wants to type in the search bar, boolean variable to represent if it's the first
    running and need to create the database, the num of tweets the user wants to extract and the path where the csv
    file will be created. Returns the csv file containing the extracted tweets and located in the path as required.
    Update the database with the new information extracted.
    """

    try:
        # extract information
        driver = initialize_driver(search_term)
        tweets = Tweets_extractor(search_term, quantity_of_tweets, path_csv_file)
        records_tweets = tweets.extract_all(driver)
        users = User_extractor(tweets.list_of_publishers_links)
        records_users = users.user_extract(driver)

        # create database and tables if this the first running
        if first_run:
            create_database_and_tables()

        # update tables
        update_table_users(records_users)
        update_table_tweets(records_tweets, search_term)
        driver.quit()
    except ValueError as va:
        print(f'{va}, Make sure you type an integer as second argument !')
    except PermissionError as Pa:
        print(f'{Pa}, Make sure the path you typed really exists or that you have permission to access it! !')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="the text you want to search in twitter", type=str)
    parser.add_argument("first_run", help="check if its the first time you run the code", type=bool)
    parser.add_argument("--number_of_tweets", help="optional number of tweets you need", type=int, required=False)
    parser.add_argument("--pathfile", help="the path for csv file", type=int, required=False)
    try:
        args = parser.parse_args()
        if not args.number_of_tweets:
            args.number_of_tweets = 150
        if not args.pathfile:
            args.pathfile = args.term + '.csv'
        main(args.term, args.first_run, args.number_of_tweets, args.pathfile)
    except SystemExit:
        print('Sorry, you need to type at least one arguments! 1) the text you want to search in twitter')
