'''
DSC 540 Data Preparation
Final Project
'''

from bs4 import BeautifulSoup
import requests

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
'''

