# Data Mininig project
## Maya Yanko & Matia Cwajgenbaum

Goal: scraping tweets from Twitter and storing them into a Database

Files needed: Tweets_Extractor.py, User_Extractor.py, build_database.py and main.py

Tweets_extractor.py is a class that extracts a specific number of tweets related to a certain search term,
User_Extractor.py is a class that extracts all the users related to the tweets already extracted
build_database.py is the code that manages the creation of the database and of the tables in it.
main.py is the file from where the user is invited to choose the parameters in order to create instances of the Tweets_extractor and the User_Extractor and then create the database with two tables one for the Tweets and the other for users.

  
  
  

Explanation on how to use the material:

Users interact only with the main.py file.

The user should insert the following inputs:

* "term": The expression to be typed in the search bar (mandatory argument)
* "--number_of_tweets": The quantity of tweets he wants to extract (optional argument)
  DEFAULT VALUE: 150
* "--pathfile": The path of the csv file to store the extracted tweets- (optional argument)
  DEFAULT VALUE:  "WORD.csv" where WORD = words typed in the search bar.

Running the program: main.py Search expression searched, --number of tweets <-- Optionnal , --pathfile <-- Optionnal . Example: main.py cats 25 

The following informations from each tweet will be stored into a table called "Tweets":

* Names of publishers - string
* Related hashtags - list 
* Tagged Users -list
* Number of replies - int
* Number of retweets - int 
* Number of likes - int
* Number of images -integer
* Date - specific date format 

The following informations from each tweet will be stored into a table called "Users":

* Names of Users - string
* Number of followers -int
* Number of followed users - int


