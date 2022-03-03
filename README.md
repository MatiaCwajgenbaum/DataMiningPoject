# Data Mininig project
## Maya Yanko & Matia Cwajgenbaum

Goal: scraping information from website
The chosen website: twitter

First downlowd chromedriver.exe from the following website: [https://www.youtube.com/watch?v=Xjv1sY630Uc] and save the path you put the file.
The user should insert the follwing inputs:
* hashtag
* the quantity of tweets he wish to analysis
* the path of the .exe file
* the path to save the csv file - this optional, if no input insert, it will save as "hashtag.csv"
Running the program: main.py hashtag, number, path. example: main.py cats 25 /home/maya/Desktop/chromedriver.exe
Then he will get the following information on the tweets connect to the specific hashtag on csv file:

* The name of publisher - string
* The related hashtags - list 
* The related pages -list
* The number of replies - float
* The number of retweets - float
* The number of likes - float
* The number of images -integer
* Date - the date

All those features and the function of extraction is order by class

Another function of the class: extracting a specific feature
