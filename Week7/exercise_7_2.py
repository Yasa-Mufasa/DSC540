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
from xlrd.sheet import ctype_text
import matplotlib.pyplot as plt
import json
import numpy as np

workbook = xlrd.open_workbook('data/unicef_oct_2014.xls')
print(workbook.nsheets)         # Prints the number of sheets in the Excel file
print(workbook.sheet_names())   # Prints the sheet names of the Excel file.


sheet = workbook.sheets()[0]
print('Part I ---------------------------------------')
print('----------------------------------------------')
print('')
print(sheet.nrows)
print(sheet.row_values(0))
for r in range(sheet.nrows):
    print(r, sheet.row(r))


'''
So I know that I'm able to read the different rows of the Excel file and I know how Python is reading each line. Let's
start off by getting the headers. Looking at the output from above and by looking at the original Excel file, I know
that the headers are on rows 4 and 5. Hmm, having the headers on both lines is going to make things interesting. Let's
take a look at just the headers.
'''

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
print('')
print('Taking a look at the headers:')
pprint.pprint(title_rows)


'''
That doesn't quite get everything imported over correctly. Looks like whenever there is a merged cell in Excel, Python
isn't applying the merged cell to the next row. But this is good enough for exploration. It doesn't need to be perfect
to start exploring it.
'''

titles = [t[0] + ' ' + t[1] for t in title_rows]    # combines the first two rows into a single string
print('')
print(titles)

titles = [t.strip() for t in titles]        # Removes the leading and trailing spaces from the titles.

'''
From previous explorations, we know that we are interested in lines 6 - 114, and that we only want the data for the
countries, not the continent totals.
'''

country_rows = [sheet.row_values(r) for r in range(6, 114)]

'''
Using agate, we need to figure out what our data types are, or define them beforehand. Let's start working through that
'''


text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

example_row = sheet.row(6)
print('')
print(example_row)

print(example_row[0].ctype)
print(example_row[0].value)
print(ctype_text)


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
# print('')
# print(table)


'''
Huh. That actually works. Sweet! I didn't know you would really use a function as part of the call of another function.
It makes sense, I just hadn't thought of trying that yet. I've been writing everything into a single function, or have
each function change a variable and the next function use the modified variable.

And that finishes out Part I.
'''

'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
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
print('')
print('Part II -----------------------')
print('-------------------------------')
print('')
table.column_names
most_egregious = table.order_by('Total (%)', reverse=True).limit(10)
print('Part II - Question 1: Which countries have the highest rate of child labor?')
# for r in most_egregious.rows:
#    print(r)


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
print('')
most_females = table.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print('{}: {}%'.format(r['Countries and areas'], r['Female']))      # This adds in formatting to our answer


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
print('')
female_data = table.where(lambda r: r['Female'] is not None)
most_female = female_data.order_by('Female', reverse=True).limit(10)
print('Part II - Question 2: Which countries have the most girls working?')
for r in most_females.rows:
    print('{}: {}%'.format(r['Countries and areas'], r['Female']))


'''
And here we see the list of the top 10 countries with the most girls working.

Now to move onto Question 3. We need to find the average percentage of child labor in cities. This won't be done using a
sort method.
'''
print('')
print('Percentage of girls working in cities:')
print(round(table.aggregate(agate.Mean('Place of residence (%) Urban')), 4))


'''
This still has some None values, so let's take care of them.
'''

print('')
has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
print('Part II - Question 3: What is the average percentage of child labor in cities?')
print(round(has_por.aggregate(agate.Mean('Place of residence (%) Urban')), 4))


'''
We get the same answer of 10.412%, but without any of the warnings about missing values.

Now time to move onto Question 4. Looks like agate has a find feature.
'''

print('')
first_match = has_por.find(lambda x: x['Rural'] > 50)
print('Part II - Question 4: Find a row with more than 50% of rural child labor:')
print(first_match['Countries and areas'])


'''
Looks like the first match of a row with more than 50% of rural child labor is Bolivia.

Now let's look for the worst offenders.
'''

print('')
ranked = table.compute([('Total Child Labor Rank',
                         agate.Rank('Total (%)', reverse=True)), ])
print('Part II - Question 4: Rank the worst offenders in terms of child labor percentages by country.')
for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Countries and areas'], row['Total (%)'], row['Total Child Labor Rank'])


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
print('')
print('Part II - Question 5: Calculate the percentage of children not involved in child labor.')
for row in ranked.order_by('Total (%)', reverse=False).limit(20).rows:
    print(row['Countries and areas'], row['Total (%)'], row['Total Child Labor Rank'])


'''
And here we see the ranked percentages of children not involved in child labor. They are:
Trinidad and Tobago
Romania
Belarus
Jordan
Lebanon
Tunisia
Kazakhstan
Ukraine
Bhutan
Jamaica

And this concludes Part II.
'''

'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
'''


'''
Part III:
Charting with matplotlib - (Data Wrangling with Python, page 255 - 258)
1. Chart the perceived corruption scores compared to the child labor percentages.
2. Chart the perceived corruption scores compared to the child labor percentages using only the worst offenders.
'''

'''
Before jumping right into answering the question, I need to import the perceived corruption scores. I'm going to run
through the code to import the data.
'''
print('')
print('Part III -------------------------------------------')
print('----------------------------------------------------')
print('')
cpi_workbook = xlrd.open_workbook('data/corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

# for r in range(cpi_sheet.nrows):
#    print(r, cpi_sheet.row_values(r))
# Ok, this is working.

cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]


def get_types(example_row):
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
            types.append(text_type)
    return types


def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)


cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]
cpi_types = get_types(cpi_sheet.row(3))

cpi_titles[0] = cpi_titles[0] + ' Duplicate'
# cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)


def float_to_str(x):
    try:
        return str(x)
    except:
        print('Could not convert float to str')
    return x


cpi_rows = get_new_array(cpi_rows, float_to_str)
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

# print(cpi_table)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)
print(cpi_and_cl.column_names)
for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print('{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'], r['Total (%)']))
# Well, this is working. That's good to see. The join worked.

'''
Alright, now that I have the two tables joined together, I can start answering the questions in Part III. I have all of
the countries listed in my variable rather than isolating out just the African countries.
'''


plt.plot(cpi_and_cl.columns['CPI 2013 Score'],
         cpi_and_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('Chart 1: CPI & Child Labor Correlation')
plt.show()


'''
And that's the chart for the first requested chart.

Now I need to make the chart for the top offenders. But first, I need to select the top offenders.
To select the top offenders, I can rank 'CPI 2013 Score' and then plot it against the 'Child Labor Percentage'.
'''

worst_offenders = cpi_and_cl.order_by('CPI 2013 Score', reverse=True).limit(20)
for r in worst_offenders.rows:
    print('{} {} {}%'.format(r['Country / Territory'],
                             r['CPI 2013 Score'],
                             r['Total (%)']))
# Ok, I have the 20 worst offenders in one place. Now I can make the plot.

plt.plot(worst_offenders.columns['CPI 2013 Score'],
         worst_offenders.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title("Chart 2: Worst Offender's CPI & Child Labor Correlation")
plt.show()

'''
Alright, and here is the chart for the worst offenders using all of the data.

For more practice, I'm going to isolate out just the records for the countries in Africa.
First, I need to get the continent data into my table
'''


country_json = json.loads(open('data/earth.json', 'r').read())
country_dict = {}
for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(country_row):
    return country_dict.get(country_row['Country / Territory'].lower())


cpi_and_cl = cpi_and_cl.compute([('continent',
                                  agate.Formula(text_type, get_country)),
                                 ])


africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')
for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
    print("{}: {}% - {}".format(r['Country / Territory'],
                                r['Total (%)'],
                                r['CPI 2013 Score']))


print(np.corrcoef(
    [float(t) for t in africa_cpi_cl.columns['Total (%)'].values()],
    [float(c) for c in africa_cpi_cl.columns['CPI 2013 Score'].values()])[0, 1])

cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))
cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))


def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False


highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

'''
Alright, now I have just the countries in Africa. Now to make the two graphs again, but using just the countries in Africa
'''

plt.plot(africa_cpi_cl.columns['CPI 2013 Score'],
         africa_cpi_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('Chart 1: CPI & Child Labor Correlation')
plt.show()

'''
Alright, that's the first chart. Now for the second one.
'''

plt.plot(highest_cpi_cl.columns['CPI 2013 Score'],
         highest_cpi_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Chile Labor Percentage')
plt.title("Chart 2: Worst Offender's CPI & Child Labor Correlation")
plt.show()

'''
And here is the second Chart using countries from Africa.
'''
