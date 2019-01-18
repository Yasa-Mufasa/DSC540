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

import pprint

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

'''
# Looking at creating a dictionary record using the zip method. (page 157-163 Data Wrangling with Python)
from csv import reader

data_rdr = reader(open('mn.csv', 'r'))
header_rdr = reader(open('mn_headers.csv', 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

print(len(data_rows[0]))
print(len(header_rows))


print(data_rows[0])
print(header_rows[:2])      # There's a mismatch between where the two records start.

commenting out after verifying that things worked.



# We need to fix the mismatch
bad_rows = []

for h in header_rows:
    if h[0] not in data_rows[0]:
        bad_rows.append(h)      # getting a list of the bad rows

for h in bad_rows:
    header_rows.remove(h)       # getting rid of the bad rows

print(len(header_rows))

# I'm still missing 9 records in my headers. I need to find these 9 records
all_short_headers = [h[0] for h in header_rows]

for header in data_rows[0]:
    if header not in all_short_headers:
        print('mismatch!', header)      # identifying the mismatched headers
# and this gives me the 9 missing headers. They don't match up, in part, because of the uppercase. The data was updated
# using R and saved in mn_headers_updated.csv. Rerunning the code but with the updated reference.
'''


'''
from csv import reader

data_rdr = reader(open('mn.csv', 'r'))
header_rdr = reader(open('mn_headers_updated.csv', 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

# print(len(header_rows))     # checking the length of the headers

all_short_headers = [h[0] for h in header_rows]

skip_index = []

for header in data_rows[0]:
    if header not in all_short_headers:
        index = data_rows[0].index(header)
        skip_index.append(index)

new_data = []

for row in data_rows[1:]:
    new_row =[]
    for i, d in enumerate(row):
        if i not in skip_index:
            new_row.append(d)
    new_data.append(new_row)

zipped_data = []

for drow in new_data:
    zipped_data.append(zip(header_rows, drow))  # zipping the dictionary record together

# pprint.pprint(zipped_data[0])       # looking at the first entry of the dictionary

# There are some issues with the last few entries. Let's take a look to see if the headers match up correctly

data_headers = []
for i, header in enumerate(data_rows[0]):
    if i not in skip_index:
        data_headers.append(header)

header_match = zip(data_headers, all_short_headers)

# pprint.pprint(header_match)     # There is a mismatch in the data order. Dang it.

# We need to reorder the data so both files are in the same order. The zip method needs both to be in the same order to work correctly
'''


# Trying again, but taking the order of the headers into consideration
from csv import reader

data_rdr = reader(open('mn.csv', 'r'))
header_rdr = reader(open('mn_headers_updated.csv', 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

all_short_headers = [h[0] for h in header_rows]

skip_index = []
final_header_rows = []

for header in data_rows[0]:
    if header not in all_short_headers:
        index = data_rows[0].index(header)
        skip_index.append(index)
    else:
        for head in header_rows:
            if head[0] == header:
                final_header_rows.append(head)
                break

new_data =[]

for row in data_rows[1:]:
    new_row = []
    for i, d in enumerate(row):
        if i not in skip_index:
            new_row.append(d)
    new_data.append(new_row)

zipped_data = []

for drow in new_data:
    zipped_data.append(zip(final_header_rows, drow))

# pprint.pprint(zipped_data[0])       # alright, this works! and it's pretty fast, so that's awesome.
# commenting out so I don't print the dictionary record each time I run the code.


'''
Data Formats Readable (page 164 - 165 Data Wrangling with Python)
Using the same dataset as the above example (mn.csv and mn_headers.csv),
use the format method to make output human readable.

Well, the nice this is that it's clarified that I'm to use the mn.csv files here. That's a relief.
'''
