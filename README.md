# Data Mininig project
## Maya Yanko & Matia Cwajgenbaum

Goal: scraping tweets from Twitter and storing them into a Database

FILES NEEDED: Tweets_Extractor.py, User_Extractor.py, build_database.py and main.py

Tweets_extractor.py is a class that extracts a specific number of tweets related to a certain search term,
User_Extractor.py is a class that extracts the publishers of the tweets already extracted.

build_database.py is the code that manages the creation of the database and of the tables in it.

main.py is the file from where the user is invited to choose the parameters in order to create instances of the Tweets_extractor and the User_Extractor and then create the database with two tables one for the Tweets and the other for users.

  
  
  

EXPLANATIONS ON HOW TO USE THE MATERIAL:

Users interact only with the main.py file.

The user should insert the following inputs:

* "term": The expression to be typed in the search bar (mandatory argument)
* "--number_of_tweets": The quantity of tweets he wants to extract (optional argument)
  DEFAULT VALUE: 150
* "--pathfile": The path of the csv file to store the extracted tweets- (optional argument)
  DEFAULT VALUE:  "WORD.csv" where WORD = words typed in the search bar.

Running the program: main.py Search expression searched, --number of tweets <-- Optionnal , --pathfile <-- Optionnal . Example: main.py cats 25 






ERD OF THE DATABASE:








![Copy of erd drawio](https://user-images.githubusercontent.com/100132518/159172050-25808e0a-fba2-4efd-b683-5045e2f8249e.png)






