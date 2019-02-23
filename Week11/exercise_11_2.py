'''
DSC 540 Data Preparation
Exercise 11.2: Data Wrangling Tools
Joshua Gardner
'''

'''
Exercise 11.2:
Complete the following using Python - make sure to show your work and show the values returned. You can submit via your
notebook or code editor, no need to export your work.

Going back to Chapter 9 (Data Wrangling with Python), let's practice joining numerous data sets - an activity you will
likely run into frequently. Following hte example in your text that starts on page 229 - 233 of Data Wrangling with
Python, work through the example to bring two data sets together. Submit your code and output to the assignment link.
'''

import xlrd
import agate
from xlrd.sheet import ctype_text


text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()


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
        '''
        This will give us the error as it appears. Once we see how the code acts, we can go back in and update the
        exception handling. 
        '''


def float_to_str(val):
    if isinstance(val, float):
        return str(val)
    elif isinstance(val, (str, unicode)):
        print('unicode is', val.encode('utf-8'))
        return val.encode('ascii', errors='replace').strip()
    return val


def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr


def remove_bad_chars(val):
    if val == '-':
        return None
    return val


def reverse_percent(row):
    return 100 - row['Total (%)']


cpi_workbook = xlrd.open_workbook('Data/corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

# for r in range(cpi_sheet.nrows):
#     print(r, cpi_sheet.row_values(r))
# TODO: Remove comment before turning in.


cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]

cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]

cpi_types = get_types(cpi_sheet.row(3))

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

# print(cpi_titles)
# Todo: Remove comment before turning in.

'''
Looks like we have a duplicate in the titles. Looks like 'Country Rank' is listed twice. Either way, I need to fix the
titles so there are only 1. So let's go fix this.
'''

cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_rows = get_new_array(cpi_rows, float_to_str)
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles) # We're remaking the cpi_table here with the updated titles.

# print(cpi_table)
# ToDo: Remove comment before turning in.

'''
Ok, so I have the first table to use in the join... But what about the other table? I need two to join...
Ah, I need the child labor table from earlier in chapter 9. Alright, let's go and get that data and get it formatted
correctly. Then I can get do the join function.
'''

workbook = xlrd.open_workbook('Data/unicef_oct_2014.xls')
sheet = workbook.sheets()[0]
title_rows = zip(sheet.row_values(4), sheet.row_values(5))
titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]    # Getting the titles into the correct format

country_rows = [sheet.row_values(r) for r in range(6, 114)] # Removes the title rows, just has the data

# Now I need the data types. I should be able to reuse the different types that were defined above.

example_row = sheet.row(6)

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


'''
Need to clean the rows before creating the table.
'''


cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)

cleaned_rows = get_new_array(country_rows, remove_bad_chars)

table = agate.Table(cleaned_rows, titles, types)

'''
Alright, I've got the table, but let's work on it a little bit more before trying the join operation. Following along
with the textbook, let's go ahead and try ordering the data in the table.
'''

most_egregious = table.order_by('Total (%)', reverse=True).limit(10)

female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(10)

table.aggregate(agate.Mean('Place of residence (%) Urban'))
has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
has_por.aggregate(agate.Mean('Place of residence (%) Urban'))
first_match = has_por.find(lambda x: x['Rural'] > 50)

'''
Now to get the second table that we're interested in for the join.
'''

ranked = table.compute([('Total Child Labor Rank',
                         agate.Rank('Total (%)', reverse=True)), ])

ranked = table.compute([('Children not working (%)',
                         agate.Formula(number_type, reverse_percent)),
                        ])

ranked = ranked.compute([('Total Child Labor Rank',
                          agate.Rank('Children not working (%)')),
                         ])

'''
Alright, I have the two tables to do the join and they're in the format I want them to be in. Now I can run the join
function. Let's do an inner join.
'''

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print('{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'],
                                r['Total (%)']
                                ))

'''
And that does it. We've joined the two tables together and printed out values from joined table.
'''
