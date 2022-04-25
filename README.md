# Data Mininig project
## Maya Yanko & Matia Cwajgenbaum

Goal: scraping tweets from Twitter and storing them into a Database

FILES NEEDED: Config.py, Driver.py, Tweets_Extractor.py, User_Extractor.py, build_database.py, API.py and main.py 

Tweets_extractor.py is a class that extracts a specific number of tweets related to a certain search term,
User_Extractor.py is a class that extracts the publishers of the tweets already extracted.
build_database.py is the code that manages the creation of the database and of the tables in it.
API.py is a code that manages the api access to get more features for the users tables.
main.py is the file from where the user is invited to choose the parameters in order to create instances of the Tweets_extractor and the User_Extractor and then create the database.

  
  
  

EXPLANATIONS ON HOW TO USE THE MATERIAL:

1) !!!! User should first change his mysql id and password in the Config.py file.

2) In order to use the Api, the user has to open a twitter developper account and generate and save in a text file his keys and tokens for authentication when accessing the api.
Here are the steps to get such an account: https://tweetfull.com/steps-to-create-a-developer-account-on-twitter
When it's done, it remains to put in the Config.py file the path to this file.

3) From there, User should interact only with the main.py file.

The user should insert the following inputs:

* "term": The expression to be typed in the search bar (mandatory argument)
* "first_run": True if this is the first run and there is a need to create the database, False if not. 
* "--number_of_tweets": The quantity of tweets he wants to extract (optional argument)
  DEFAULT VALUE: 150
* "--pathfile": The path of the csv file to store the extracted tweets- (optional argument)
  DEFAULT VALUE:  "WORD.csv" where WORD = words typed in the search bar.

Running the program: main.py Search expression searched, True/False, --number of tweets <-- Optionnal , --pathfile <-- Optionnal . Example: main.py cats True 25 






ERD OF THE DATABASE:![erd](https://user-images.githubusercontent.com/100132518/163449331-3e7f62b1-4241-4214-90d1-fa2075761407.png)






