# Data Mininig project
## Maya Yanko & Matia Cwajgenbaum

Goal: scraping tweets from Twitter

Files needed: Tweets_Extractor.py and main.py
The first one is the code of the Tweets_extractor class, the second file main.py is the file from where the user is invited to choose the parameters in order to create an instance of the class.

  
  
  

Explanation on how to use the material:

Users interact only with the main.py file.

The user should insert the following inputs:
* Words or expression to be typed in the search bar
* the quantity of tweets he wants to extract
* the path of the csv file - which is optional. If no input inserted: the csv file will be saved as "WORD.csv" where WORD = words typed in the search bar.

Running the program: main.py Search expression searched, number of tweets, (path) <-- Optionnal . Example: main.py cats 25 

The following informations from each tweet will be saved:

* Names of publishers - string
* Related hashtags - list 
* Tagged Users -list
* Number of replies - float
* Number of retweets - float
* Number of likes - float
* Number of images -integer
* Date - specific date format 


Other functionality of the class:
The user can also extract only one specific feature for all tweets using one of the following methods:
            self._Extract_Names(driver)
            self._Extract_hashtags_userstagged_links(driver)
            self._Extract_NumReplies_retweets_likes(driver)
            self._Extract_Dates(driver)
            self._Extract_Num_images(driver)
