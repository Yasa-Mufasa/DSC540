'''
DSC 540 Data Preparation
Final Project
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

'''
During the course, you will be working on a term project to either pull data from an API or scrape a web page. You will
need to select either an API (different from Twitter) or a Webpage and create a process in Python that will extract data
into a formatted data set.

There are no restrictions on what API ro Webpage you use, other than you cannot use Twitter or the Webpages used in the
exercises from your book.

The following is ude submitted to the assignment link or submit a link to you r GitHub repository to the assignment
link:
    * Your formatted dataset with at least 15-20 variables (if the ApI or WEbpage you selected doesn't have that many
      fields available on it, you will want to search again, or do multiple!)
    * Your code or screenshots of your code outlining the steps and process you had to take to pull data from the API or
      web page and the steps you took to format the data
    * 2 Data Transformation / Clean-up Steps (can be any that we learned in class)
    * A 250-word paper summarizing your steps and any challenges you ran into during the project. Discuss the importance
      and relevance of this type of process if you were a data scientist. How often do you thik you would have to do
      this to get the data you need?
'''

'''
For this final project, I am planning on scrapping web pages for information. After checking the /robots.txt files for
the web pages I initially wanted to scrape, I found out they ask scraping to not be done for this purpose. As such, I
will be scraping information from books.toscrape.com and quotes.toscrape.com, two web pages intended to be scraped for
practice and learning. I will need to scrape both for this project as neither web page has enough variables alone.

I will be using the BeautifulSoup package to do most of my web scraping.

I will be starting with books.toscrape.com.
'''

page = requests.get('http://books.toscrape.com/')
bs = BeautifulSoup(page.content, 'lxml')    # scrapes the web page

image_containers = bs.find_all('div', class_='image_container')  # gets all of the image_containers

link = []   # puts the image containers into a list so we can iterate over it.
for image in image_containers:
    link.append(image.a)

strings = []    # formats the list contents as strings
for a in link:
    strings.append(str(a))

stripped_strings = []   # splits the strings along the " so we can just grab the portion we want.
for string in strings:
    stripped_strings.append(string.split('"'))

cat_placement = []  # Gets three of the variables I want into different lists so I can combine them
title = []
pic_name = []
for i in range(20):
    cat_placement.append(stripped_strings[i][1])
    title.append(stripped_strings[i][3])
    pic_name.append(stripped_strings[i][7])

'''
I have the first 3 variables for this assignment gathered. Now I need to grab a few more. I'll get the price and if the
book is in stock or not.
'''

price_containers = bs.find_all('div', class_='product_price')

prices = []  # Putting the items into an iterable list
for price in price_containers:
    prices.append(price.p)

strings = []    # Formatting each item in the list as a string so we can pull out just the part we need
for p in prices:
    strings.append(str(p))

stripped_strings = []   # Splitting the strings to make it easier to get what we need
for string in strings:
    stripped_strings.append(string.split('>'))

book_price = []  # Just getting the portion of the split string that we need.
for i in range(20):
    book_price.append(stripped_strings[i][1])

books = []  # Adding some additional format to get rid of the </p at the end of each string
for i in book_price:
    books.append(i.strip('</p'))

'''
I know have the prices. Now to look at the availability.
'''

availability = bs.find_all('p', class_='instock availability')

first_step = []  # Getting the items into an iterable list as strings.
for a in availability:
    first_step.append(str(availability))

avail = []  # Selecting only the portion we need by slicing the string
for i in range(20):
    avail.append(first_step[i][70:79])

'''
Now I have the availability of the books. Let's take a look at the ratings.
'''

ratings = bs.find_all('article', class_='product_pod')

first_step = []  # Getting the items into an iterable list as strings and split by the " character
for i in range(20):
    first_step.append(str(ratings[i]).split('"'))

book_ratings = []   # Selecting only the portion of the split strings that we need.
for i in range(20):
    book_ratings.append(first_step[i][13])

'''
Now that I have the book ratings, let's look to see if I can add them to the shopping cart.
'''

button = bs.find_all('div', class_='product_price')

first_step = []  # Getting the split strings into an iterable list
for i in range(20):
    first_step.append(str(button[i]).split('>'))

second_step = []    # Removing the unneeded portion of the string.
for i in range(20):
    second_step.append(first_step[i][9].strip('/button'))

button_stat = []    # For whatever reason, I couldn't strip the last character in step 2 without removing the last needed character. Doing this to remove the last character.
for i in range(20):
    button_stat.append(second_step[i][:-1])

d = {'title': title, 'category_placement': cat_placement, 'picture_name': pic_name, 'price': books,
     'availability': avail, 'rating': book_ratings, 'button_status': button_stat}
scraped_books = pd.DataFrame(d)  # Adding everything into the DataFrame.
print(scraped_books)

'''
Now to get to the second scraping set. This set will be scraped from http://quotes.toscrape.com/
I'm not going to notate what I'm doing, but the steps I'm following will be similar to the above example.
'''

page = requests.get('http://quotes.toscrape.com/')
bs = BeautifulSoup(page.content, 'lxml')

quote_containers = bs.find_all('div', class_='quote')

item_type = []
for i in range(10):
    item_type.append(str(quote_containers[i])[42:72])

# Getting a new quote_container
quote_container = bs.find_all('span', class_='text')

first_step = []
for i in range(10):
    first_step.append(str(quote_container[i]).split('"'))

second_step = []
for i in range(10):
    second_step.append(first_step[i][4].strip('>"').strip('"</span>'))

quote = []
for i in range(10):
    quote.append(second_step[i][1:-1])

d = {'quote': quote, 'item_type': item_type}
scraped_quotes = pd.DataFrame(d)

tag_container = bs.find_all('div', class_='tags')

first_step = []  # This is only selecting the first tagged item, which works for what I'm doing on this one.
for tag in tag_container:
    first_step.append(tag.a)

second_step = []
for i in first_step:
    second_step.append(str(i).split('/'))

first_tag = []
for i in second_step:
    first_tag.append(i[2])

scraped_quotes['first_tag'] = first_tag

'''
Looking at how to grab the rest of the tags, I can reuse tag_container to pull the data.
'''

first_step = []
for i in tag_container:
    first_step.append(str(i).split('/'))

second_tag = []
for i in range(10):
    try:
        second_tag.append(first_step[i][9])
    except:
        second_tag.append('No Tag')

scraped_quotes['second_tag'] = second_tag

third_tag = []
for i in range(10):
    try:
        third_tag.append(first_step[i][15])
    except:
        third_tag.append('No Tag')

scraped_quotes['third_tag'] = third_tag

fourth_tag = []
for i in range(10):
    try:
        fourth_tag.append(first_step[i][21])
    except:
        fourth_tag.append('No Tag')

scraped_quotes['fourth_tag'] = fourth_tag

fifth_tag = []
for i in range(10):
    try:
        fifth_tag.append(first_step[i][27])
    except:
        fifth_tag.append('No Tag')

scraped_quotes['fifth_tag'] = fifth_tag

'''
Now to get the author of the quote.
'''

author_container = bs.find_all('small', class_='author')

first_step = []
for i in author_container:
    first_step.append(str(i).split('>'))

authors = []
for i in range(10):
    authors.append(first_step[i][1].strip('</small'))

scraped_quotes['author'] = authors
print(scraped_quotes)

'''
Now I need to complete two clean-up actions to complete this assignment. I'm going to change the rating variable to be
integers and drop the Euro sign and change the price variable to be floats.
'''

step_one = scraped_books['rating']

step_two = []
for i in range(20):
    step_two.append(step_one[i].split(' '))

step_three = []
for i in range(20):
    step_three.append(step_two[i][1])

step_four = []
for i in range(20):
    if step_three[i] == 'One':
        step_four.append(int(1))
    elif step_three[i] == 'Two':
        step_four.append(int(2))
    elif step_three[i] == 'Three':
        step_four.append(int(3))
    elif step_three[i] == 'Four':
        step_four.append(int(4))
    elif step_three[i] == 'Five':
        step_four.append(int(5))

scraped_books['rating'] = step_four

'''
This cleaned up the ratings and puts the ratings into integers. Now let's clean up the price.
'''

step_one = scraped_books['price']

step_two = []
for i in range(20):
    step_two.append(step_one[i][2:])

step_three = []
for i in range(20):
    step_three.append(float(step_two[i]))

scraped_books['price'] = step_three

'''
And this cleans up the price variable.
'''

print(scraped_books)

'''
The last thing I would like to do is save the scraped data into a file.
'''

scraped_books.to_csv('Data/scraped_book_data.csv', sep=',')
scraped_quotes.to_csv('Data/scraped_quotes_data.csv', sep=',')
