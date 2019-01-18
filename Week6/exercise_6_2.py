'''
Exercise 6.2
Joshua Gardner
'''

'''
Fixing Labels/Headers - (Page 155 - 156 Data Wrangling with Python)

Create a new dictionary for each row to create a new array

I'm not exactly sure which dataset to use. I'm going to go ahead and follow
along with our textbook and use the data sets mn.csv and mn_headers.csv that
our textbook uses.
'''

'''
from csv import DictReader
# Need to change my directory
import os
os.chdir("C:/Users/yasam/OneDrive/Documents/Grad School/DS540 Data Preparation/data-wrangling-master/data/unicef")

# Now I can start importing the data into a dictionary record.
data_rdr = DictReader(open('mn.csv','r'))
header_rdr = DictReader(open('mn_headers.csv', 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

# Let's check on the imported data

print(data_rows[:5])
print(header_rows[:5])        # This works! sweet! Moving to comment as I don't need to double check this portion any more.


# Let's start exploring how we can find matches between the headers

for data_dict in data_rows:
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            for hkey, hval in header_dict.items():
                if dkey == hval:
                    print('match!')         # This takes a while to check each record, but finds many matches



# Now let's create a dictionary record
new_rows = []

for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)

# Now to check to see if this worked
print(new_rows[0])      # This takes a while to work through the data. Let's try the zip method to see if it's any faster

commenting out to keep the code, but to try the zipping method
'''

# Looking at creating a dictionary record using the zip method. (page 157-163 Data Wrangling with Python)
from csv import reader

data_rdr = reader(open('mn.csv', 'r'))
header_rdr = reader(open('mn_headers.csv', 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

print(len(data_rows[0]))
print(len(header_rows))
