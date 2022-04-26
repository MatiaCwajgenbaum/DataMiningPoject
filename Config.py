# User has to type here his own id and password for mysql
USER = "maya95"
PASSWORD = "MSmaya2035!"
HOST = "localhost"
DATABASE_NAME = 'Tweets'

LENGTH_VARCHAR = 255
URL = 'https://twitter.com/search?q='
NUM_SECONDS_TO_LOAD = 0.5
MAX_NUM_TWEETS = 100

# This variable is the location of the text file where the user stored his twitter developper keys and tokens
TOKEN_LOCATION = r"/home/maya/PycharmProjects/itc/Twitter_api_mafteah.txt"  # r"C:\Users\matia\OneDrive\Bureau\Twitter_api_mafteah.txt"
USER_FIELDS = "user.fields=description,created_at,public_metrics,verified"

# log file
LOGGING_FILE = "Tweets.log"
FORMAT = '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s'
