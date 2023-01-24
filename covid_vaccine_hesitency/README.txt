# Introduction
This project contains:
-5 python files: general.py, api.py, analyze_api.py, test.py, and run_project.py
-2 folders: main_data, test_data


# How to Run
Everything should be in one place.
The project can be accessed by running the "run_project.py" file.
Please enter the command in terminal: 

python covid_vaccine_hesitency/run_project.py


# Recommended Modules
Here is a list of modules you will need to run the project:

pandas
seaborn
matplotlib.pyplot
geopandas
textblob
wordcloud
re
tweepy


# Breakdown of Every File/Folder
Files:
general.py -- includes analysis, visualizations, and insights from Daily Vaccinations & Annual State Income datasets.
api.py -- accesses the Twitter API, queries 1000 public tweets, and stores information in CSV file.
analyze_api.py -- uses generated CSV file for analysis of Tweets & location of users of those tweets.
run_project.py -- imports previously stated files and runs them in "main" method.
test.py -- contains test methods that uses test data. Includes "main" method directly in file.

Folders:
main_data -- contains four real datasets used for final project analysis
test_data -- contains two fake datasets (self generated), which are shorter and simpler. Used in test.py.