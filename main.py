from Driver import *
from Tweets_Extractor import *
from API import *
from User_Extractor import *
from build_database import *

import argparse
import logging


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
        logging.info("initialize the driver for scraping")
        driver = initialize_driver(search_term)
        logging.info("build instance of the Tweets class")
        tweets = Tweets_extractor(search_term, quantity_of_tweets, path_csv_file)
        logging.info("scraping Tweets")
        records_tweets = tweets.extract_all(driver)
        logging.info("build instance of the Users class")
        users = User_extractor(tweets.list_of_publishers_links)
        logging.info("scraping Tweets")
        records_users = users.user_extract(driver)

        # create database and tables if this the first running
        if first_run:
            logging.info("create database and tables for first running")
            create_database_and_tables()
        use_database()
        # update tables
        logging.info("update tables in the database with the new info get from scraping")
        update_table_users(records_users)
        update_table_tweets(records_tweets, search_term)
        driver.quit()

        # API
        logging.info("get extra information on user using Twitter API")
        # add columns to User table if this the first running
        try:
            add_columns(cursor)
        except pymysql.err.OperationalError as err:
            print('columns already created')
        record_api = get_list_usernames_from_table(cursor)
        logging.info("update User' table with new info get from Twitter API")
        fill_new_columns(record_api, cursor)
    except PermissionError as Pa:
        logging.error("the user insert wrong type of parameters")
        print(f'{Pa}, Make sure the path you typed really exists or that you have permission to access it! !')


if __name__ == '__main__':
    logging.basicConfig(filename=LOGGING_FILE, format=FORMAT, level=logging.INFO)
    logging.info("get parameters from the user")
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="the text you want to search in twitter", type=str)
    parser.add_argument("first_run", help="check if its the first time you run the code", type=bool)
    parser.add_argument("--number_of_tweets", help="optional number of tweets you need", type=int, required=False)
    parser.add_argument("--pathfile", help="the path for csv file", type=int, required=False)
    try:
        args = parser.parse_args()
        if not args.number_of_tweets:
            args.number_of_tweets = MAX_NUM_TWEETS
        if not args.pathfile:
            args.pathfile = args.term + '.csv'
        if not isinstance(args.number_of_tweets, int):
            logging.error("the user insert wrong type of parameters")
            print(f'Make sure you type an integer as number_of_tweets!')
        else:
            main(args.term, args.first_run, args.number_of_tweets, args.pathfile)
    except SystemExit:
        logging.error("the user insert wrong number of parameters")
        print('Sorry, you need to type at least one arguments! 1) the text you want to search in twitter')