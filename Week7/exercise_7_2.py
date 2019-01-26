'''
DCS 540
Exercise 7.2: Importing, Exploring, and Charting Data
Joshua Gardner
'''

'''
Part I:
Importing Data - (Data Wrangling with Python, Page 219 - 228)
Create a function to take an empty list, interate over the columns and create a full list of all the column types for
the dataset. Then load into agate table - make sure to clean the data if you get an error. Follow along with the example
in the book on the pages listed.
'''

'''
The data used is from UNICEF's child labor summary data.
'''

import xlrd
import agate
import pprint

workbook = xlrd.open_workbook('data/unicef_oct_2014.xls')
#print(workbook.nsheets)         # Prints the number of sheets in the Excel file
#print(workbook.sheet_names())   # Prints the sheet names of the Excel file.
#TODO: Remove comment before turning in.

sheet = workbook.sheets()[0]
#print(sheet.nrows)
#print(sheet.row_values(0))
#for r in range(sheet.nrows):
#    print(r, sheet.row(r))
#TODO: Remove comment before turning in.

'''
So I know that I'm able to read the different rows of the Excel file and I know how Python is reading each line. Let's
start off by getting the headers. Looking at the output from above and by looking at the original Excel file, I know
that the headers are on rows 4 and 5. Hmm, having the headers on both lines is going to make things interesting. Let's
take a look at just the headers.
'''

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
#print('Taking a look at the headers:')
#pprint.pprint(title_rows)
#TODO: remove comment before turning in

'''
That doesn't quite get everything imported over correctly. Looks like whenever there is a merged cell in Excel, Python
isn't applying the merged cell to the next row. But this is good enough for exploration. It doesn't need to be perfect
to start exploring it.
'''

titles = [t[0] + ' ' + t[1] for t in title_rows]    # combines the first two rows into a single string
#print(titles)
#TODO: remove comment before turning in
titles = [t.strip() for t in titles]        # Removes the leading and trailing spaces from the titles.

'''
From previous explorations, we know that we are interested in lines 6 - 114, and that we only want the data for the
countries, not the continent totals.
'''

country_rows = [sheet.row_values(r) for r in range(6,114)]

'''
Using agate, we need to figure out what our data types are, or define them beforehand. Let's start working through that
'''

from xlrd.sheet import ctype_text

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

example_row = sheet.row(6)
#print(example_row)

#print(example_row[0].ctype)
#print(example_row[0].value)
#print(ctype_text)
#TODO: remove comments befor turning in

types = []
for v in example_row:
    value_type = ctype_text[v.ctype]
    if value_type == 'text':
        types.append(text_type)
    elif value_type == 'number':
        types.append(number_type)
    elif value_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)     # This means that if we can't identify the data type, it defaults to text_type.

'''
Now to try zipping the titles with the data types
'''

# table = agate.Table(country_rows, titles, types)
'''
This gives an error due to unclean data. There is a '-' somewhere in one of the columns. Will need to remove the '-'
before we can make the agate.Table().
'''

# This will remove the '-' characters
def remove_bad_chars(val):
    if val == '-':
        return None     # replaces the '-' with None
    return val

cleaned_rows = []       # making a new list to put the cleaned data into

for row in country_rows:    # Cleaning our data by removing the '-'
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)


'''
Let's write a function over what we've done so far. It will take an array and what function you would like to use to
clean the old array.
'''
def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr

'''
Now that we have our function, let's try it out to see how it works.
'''

table = agate.Table(cleaned_rows, titles, types)
#print(table)
#TODO: Remove comment before turning in.

'''
Huh. That actually works. Sweet! I didn't know you would really use a function as part of the call of another function.
It makes sense, I just hadn't thought of trying that yet. I've been writing everything into a single function, or have
each function change a variable and the next function use the modified variable.

And that finishes out Part I.
'''


'''
Part II:
Exploring Table Functions - (Data Wrangling with Python, Page 225 - 228)
1. Which countries have the highest rate of child labor?
2. Which countries have the most girls working?
3. What is the average percentage of child labor in cities?
4. Find a  row with more than 50% of rural child labor.
5. Rank the worst offenders in terms of child labor percentages by country.
6. Calculate the percentage of children not involved in child labor.
'''

'''
If we're looking for the highest rates, why not sort the rates and look at which is top of the list?
'''

table.column_names
most_egregious = table.order_by('Total (%)', reverse=True).limit(10)
#print('Part II - Question 1: Which countries have the highest rate of child labor?')
#for r in most_egregious.rows:
#    print(r)
#TODO: Remove comments before turning in

'''
This function gives us which countries have the highest rates of child labor. In fact, it gives us the top 10. They are,
in order from highest to lowest:
Somalia
Cameroon
Zambia
Burkina Faso
Guinea-Bissau
Ghana
Nepal
Peru
Niger
Central African Republic

This answers the first question of Part II

Moving onto question 2, we can do something similar to find which countries have the most girls working.
'''

most_females = table.order_by('Female', reverse=True).limit(10)
#for r in most_females.rows:
#    print('{}: {}%'.format(r['Countries and areas'], r['Female']))      # This adds in formatting to our answer
#TODO: Remove comments before turing in

'''
The 10 countries with the most girls working are, from highest to lowest:
Cabo Verde
Chile
Ecuador
Somalia
Cameroon
Zambia
Nepal
Guinea-Bissau
Peru
Burkina Faso

Except these have some None values. Let's rerun this to take the None values out
'''

female_data = table.where(lambda r: r['Female'] is not None)
most_female = female_data.order_by('Female', reverse=True).limit(10)
#print('Part II - Question 2: Which countries have the most girls working?')
#for r in most_females.rows:
#    print('{}: {}%'.format(r['Countries and areas'], r['Female']))
#TODO: Remove comment before turning in.

'''
And here we see the list of the top 10 countries with the most girls working.

Now to move onto Question 3. We need to find the average percentage of child labor in cities. This won't be done using a
sort method.
'''

#print('Percentage of girls working in cities:')
#print(round(table.aggregate(agate.Mean('Place of residence (%) Urban')),4))
#TODO: Remove comment before turning in

'''
This still has some None values, so let's take care of them.
'''

has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
#print('Part II - Question 3: What is the average percentage of child labor in cities?')
#print(round(has_por.aggregate(agate.Mean('Place of residence (%) Urban')),4))
#TODO: Remove comment before turning in

'''
We get the same answer of 10.412%, but without any of the warnings about missing values.

Now time to move onto Question 4. Looks like agate has a find feature.
'''

first_match = has_por.find(lambda x: x['Rural'] > 50)
#print('Part II - Question 4: Find a row with more than 50% of rural child labor:')
#print(first_match['Countries and areas'])
#TODO: Remove comment before turning in

'''
Looks like the first match of a row with more than 50% of rural child labor is Bolivia.

Now let's look for the worst offenders.
'''

ranked = table.compute([('Total Child Labor Rank',
                         agate.Rank('Total (%)', reverse=True)), ])
#print('Part II - Question 4: Rank the worst offenders in terms of child labor percentages by country.')
#for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
#    print(row['Countries and areas'],row['Total (%)'], row['Total Child Labor Rank'])
#TODO: Remove comment before turning in

'''
Looks like the worst offenders are:
Somalia
Caeroon
Zambia
Burkina Faso
Guinea-Bissau
Ghana
Nepal
Peru
Niger
Central African Republic

Now to look for the percentage of children not involved with child labor. This is just the inverse of the percentages.
But we can still calculate and rank them with the following:
'''

def reverse_percent(row):
    return 100 - row['Total (%)']

ranked = table.compute([('Children not working (%)',
                         agate.Formula(number_type, reverse_percent)),
                        ])
ranked = ranked.compute([('Total Child Labor Rank',
                          agate.Rank('Children not working (%)')),
                         ])
print('Part II - Question 5: Calculate the percentage of children not involved in child labor.')
for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Countries and areas'],row['Total (%)'], row['Total Child Labor Rank'])





'''
Part III:
Charting with matplotlib - (Data Wrangling with Python, page 255 - 258)
* Chart the perceived corruption scores compared to the child labor percentages.
* Chart the perceived corruption scores compared to the child labor percentages using only the worst offenders.
'''

