'''
DSC 540 Midterm
Joshua Gardner
'''

'''
Denver Crime Data

I've decided to use the denver crime data obtained from Kaggle (https://www.kaggle.com/paultimonthymooney/denver-crime-data)
for my midterm project. There are 19 variables with 452,479 observations, meaning this dataset falls within the midterm
requirements. The data is in a .csv file format. I was hoping to find a good JSON file to test myself with, but then
found this dataset that caught my attention.

On another note, the .csv file is too large for me to add it to my GitHub repository. I will not be able to add it to my
data folder within this project folder. As such, please download the .csv file and format your pathway correctly on your
machine prior to running this code.

Glancing over the data, there are several variables that have missing data, specifically LAST_OCCURANCE_DATE,
INCIDENT_ADDRESS, GEO_X, GEO_Y, GEO_LON, and GEO_LAT. I will most likely need to deal with the missing data in some form
during this project.

Before getting too far ahead of myself, I need to import modules i will be using.
'''

import sys
import csv
import pprint
import os
os.chdir('C:/Users/yasam/OneDrive/Documents/Grad School/DS540 Data Preparation/Midterm/Denver Crime Data')
# Update this file path to reflect where the .csv file is saved before running on your machine.


'''
First step is to get the data into python. Here's a function I wrote for DSC 510 to import the data into a list. By using
this function, I'm importing the data into the rows variable and checking the 151st record to se if it imported correctly.
'''

rows = []
def readRows(inputCSV):
    with open(inputCSV, 'r') as read:
        readCSV = csv.reader(read)
        for row in readCSV:
            rows.append(row)
        # print(rows[152])

readRows('crime.csv')

'''
Looks like it imported the data without any issues, as far as I can tell. Let's take a look at the first row to see how
the headers were imported.
'''

# print(len(rows[0]))
# print(rows[0])        # TODO: Commenting out so I don't keep reprint this. Uncomment and rerun before turning in.

'''
Alright, looks like all 19 variables were imported into 19 different columns and each column matches up with the title of
each variable.
'''


