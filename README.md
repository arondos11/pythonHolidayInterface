# pythonHolidayInterface
holidays.json holds the intial 7 json files
file.csv takes input from webscraping the holiday website
the holidayFiles.json file brings in both previous data elements as well as saves changes being made by user>> the full list of holidays is stored here
holidayCode.py takes operates most of the processes, and take in a few urls and apis from the ignored config.py file
a holiday class with string format ouput function exists as well as a container holidayList class
functions to get the data include getting html getHTML, getting the inital json data initialJSON, getting data from previous changes fromJSON, getting data from web scraping webScrape, removeDuplicates to slim down and reduce redundancy in the list of holidays, and writeJSON, which stores all data gatehred up untill that point into a json file.

User input funcitons include adding and removing holidays, filtering by year and week, and saving user changes. A findHoliday function works in the background to find holidays based on their name and date and help the other userInput functions run, but the user never interacts with findHoliday directly
