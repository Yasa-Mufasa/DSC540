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

'''
Part 1: Replace Headers (Data Wrangling with Python 154 - 163)

All of the variable names are already both human and machine readable, but I don't like that they're all in caps. I'm
going to modify them so that they are all lowercase.
'''

headers = []
for x in rows[0]:
    headers.append(x.lower())
# print(headers)    #TODO: Remove comment before turning in.

'''
Alright, that worked just fine. I have all of my headers in lowercase. And this answers the first part of the Midterm.
'''

'''
Part 2: Format Data to a Readable Format (Data Wrangling with Python pg. 164 - 168)

This one is going to be more challenging. Right now, I have everything in Python as a list of lists. To format the data,
I can iterate through each row and correct what data I need to in order to make the data more readable. offense_type_id
and offense_category_id have dashes rather than spaces. I could remove the dashes to make it more human readable.
is_crime and is_traffic are both booleans and should be changed to True / False for readability.

So, now the question is, how to iterate through rows to correct each entry? Let's try to iterate over the rows and use
the replace() function
'''

for row in rows:
    x = row[4].replace('-', ' ')
    y = row[5].replace('-', ' ')
    z = row[16].replace('-', ' ')   # This column also has dashed to replace
    row[4] = x
    row[5] = y
    row[16] = z
# print(rows[150])    # Checking one of the rows down the list for correction
# TODO: Remove comment before turning in.

'''
I've checked the 151st row to make sure that the function worked down the road. Let's also check the last row to ensure
it is correct as well.
'''

# print(rows[-1])   # The last row looks fine, except that we need to change the last two columns.
#TODO: Remove comment before turning in.

'''
After much fiddling, I can now fix the booleans to reflect True/ False with the following:
'''

for row in rows[1:]:    # Need to skip the header row. I could throw an else in last and say continue for the first row, but this works just as well
    if row[-2] == '1':
        x = 'True'
        row[-2] = x
    elif row[-2] == '0':
        x = 'False'
        row[-2] = x

for row in rows[1:]:
    if row[-1] == '1':
        x = 'True'
        row[-1] = x
    elif row[-1] == '0':
        x = 'False'
        row[-1] = x

# pprint.pprint(rows[0:5])
#TODO: Remove comment before turning in.

'''
Ok, that fixes those problems. But what about the dates? They are stings at the moment. Do I want to format them so they
are datetime objects?

Columns 6, 7, and 8 are dates with the time as well. In order to take the strings apart to tell what each day, month,
year, hour, and minute are, I would need to develop some sort of logic to tear the string apart. For now I will leave
the dates as strings and move onto the next section.
'''


'''
Part 3: Identify Outliers and Bad Data (Data Wrangling with Python pg. 169 - 174)

I initially started this project in Jupyter Notebook, but found that I ended up crashing both Jupyter Notebook and my
computer when I attempted to put my list into a dictionary record. I'm hoping that I'll have better luck using PyCharm.

I'm beginning to wonder if I should put the data into a pandas dataframe. I wonder if doing so from the beginning would
have caused fewer headaches.

Looks like I could have started off using pandas.read_csv(), but I don't want to use that now because it would ignore
all of the changes I've made to rows. Looks like I have two options. I could create lists of each variable to combine
them into a dataframe, or I could make an ordered dictionary and follow through with the book somehow.
'''

drows = rows[1:]
# print('headers:', headers)
# print('data:', drows[0:2])
#TODO: Remove comment

'''
Ok, I have my two lists with all of the formatted data. Now to try zipping them together into a dictionary record. I am
leaving out a lot of my exploration of how to complete this next step, but here's the working code:
'''


crime = []
for i in range(1, len(rows[1:])+1):
    x = {}
    x = dict(zip(headers, rows[i]))
    crime.append(x)

# print(crime[150])
#TODO: remove comment

'''
After a lot of playing around and trying different things, I was able to figure out the above thanks to advice I found on
StackOverflow's question "Convert a list to a dictionary in Python" found at:
https://stackoverflow.com/questions/4576115/convert-a-list-to-a-dictionary-in-python

After cross checking with the original .csv file, I verified that the last record matches with the original record. The
last record is crime[452478]. The index is 2 less than the full length of rows as the index is 1 less than the length,
and we've removed the header row. 452480 - 2 = 452478, the index of the last record.

Now, I can move onto Part 3 and find the Outliers and Bad Data. And better yet, because the data is in a dictionary, I
can follow along with the textbook now.

First thing first, the data is coming from Kaggle, so I'm fairly certain the data has been previously cleaned and
processed. The data was collected from Denver, Co's Open Data Catalog. The data, before it was collected, was dynamic,
so any incorrect entries could have been corrected. The data is generated based on the National Incident Based Reporting
System. If there is any bias contained within the data, it would be due to societal bias, which could be the purpose of
analysis.

Next thing to worry about is if there is any missing data. I'm fairly confident that the data imported correctly after
checking the first few rows, a subset in the middle, and the last few rows against the original data. Everything matched.
But what about NaN values? This isn't going to be the most elegant of solutions, but I can check the NA values this way.
I also know that some missing values are entered in as ''. I'll check for both.
'''

def Missing(name):
    na_count = 0
    missing = 0
    for y in [x[name] for x in crime]:
        if y == 'NA':
            na_count += 1
        elif y == '':
            missing += 1
    print(name + ' # of NA: ' + str(na_count) + '\n  ' + name + ' # of missing values ' + str(missing))

#for y in headers:
#    Missing(y)
#TODO: Remove comments

'''
Looks like there are no NA values, but there are missing values, but there are blank, or missing, values. Looks like
there are 308,900 missing values for last_occurrence_date, but that would make sense. The missing values would mean that
this is the first occurrence of the crime. I wish it was closer to all of the data, but roughly 3/5 of the data is the
first occurrence.

44,507 occurances are missing incident_address, 3,671 are missing geo_x, geo_y, geo_lon, and geo_lat. I'm assuming that
these values either do not have an address or that geo location was not available at the time the data was entered into
the database. Or it could be that there was no exact location available.

It would be nice to have this information, but what I would do with the missing values would depend on the analysis I
want to complete. With the location data missing, if I were to make a heat-map of where crimes have been occurred, I
would exclude the missing data. But the missing data for last_occurrence_date tells us that this is the first occurrence,
which could be used to find how many crimes are the first crime, which as mentioned above is roughly 3/5 of them.

Following the textbook, let's check what data type each value is. I'll look at crime[600] for this.
'''

#for name in headers:
#    print(name, type(crime[0][name]))

#print(crime[600])
#TODO: Remove comments

'''
All of the variables are entered as strings. Normally, I would want numbers to be either integers or floats, but in this
case, all of the numbers are categorical, not continual, so they don't necessarily need to be converted to numbers. For
now, I'm going to leave them as they are and will change them if I need to later on. As far as I can tell, the data
looks ok.
'''


'''
Part 4: Find Duplicates (Data Wrangling with Python pg 175 - 178)¶

With the data coming from Kaggle, I don't think there will be any duplicates, but it will still be good to check. One
way I can check is to check the incident_id's to see if any of them are duplicates. As a matter of interest, I can also
check to see how many offense_id's are duplicates as well.
'''
