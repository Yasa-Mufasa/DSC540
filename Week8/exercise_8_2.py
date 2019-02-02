'''
DSC 540
Joshua Gardner

Exercise 8.2:
Complete the following using Python -- make sure to show your work and show the values returned. You can submit via your
notebook or code editor, no need to export your work.

    * Connect to the internet using Python Library urllib (Data Wrangling with Python pg 298 - 300), follow the example
      in the book to connect to the same website or a different website and submit your code
    * Reading a Web Page with Beautiful Soup - following the example starting on page 300 - 304 of Data Wrangling with
      Python, use the Beautiful Soup Python library to scrap a web page. The result should be data and output in an
      organized format. Each of the data entries should be in its own dictionary with matching keys.
    * Web scraping with Selenium - Follow along with your book starting on page 318 - 329 of Data Wrangling with Python.
      At the end of the exercise, you should be able to go to a site, fill out a form, submit the form, and then scroll
      through the results with the code you wrote. Make sure to submit the code and your output.

'''

import urllib
import urllib2
import requests

'''
Alright, first thing first, I need to import the various packages I'll need for this assignment.
As a side note, both urllib and urllib2 are part of the built in packages of Python 2.7. There is no need to use the pip
installer, we just need to import it into our code.

Part 1:
Connect to the internet using Python LIbrary urllib (Data Wrangling with Python page 298 - 300), follow the example in
the book to connect to the same website or a different website and submit your code.

Now to start answering the first portion of the exercise. I need to connect to the internet using urllib. Why not try to
connect to Google?
'''

google = urllib2.urlopen('http://google.com')
google = google.read()
# print('Section 1:')
# print('')
# print(google[:200])     # prints the first 200 characters
# TODO: Remove comment before turning in

url = 'http://google.com?q='
url_with_query = url + urllib.quote_plus('python web scraping')

'''
Huh, that's actually pretty cool. Would it work for any website? Let's try it on Bellevue's main page.
'''

bell = urllib2.urlopen('http://www.bellevue.edu')
bell = bell.read()
# print('')
# print("Bellevue's Web Page")
# print(bell[:200])
# TODO: Remove comment before turning in

'''
It really does work! But let's now move on with looking at some of the things you can do with the request library
'''

google = requests.get('http://google.com')
# print('Status Codes:')
# print(google.status_code)
# print('')
# print('First 200 Characters:')
# print(google.content[:200])
# print('')
# print('Headers:')
# print(google.headers)
# print('')
# print('Cookies:')
# print(google.cookies.items())
# TODO: Remove comments before turning in. Use Ctrl + / to mass comment/uncomment

'''
That's cool, and helps give more information than I was thinking it would. And this concludes the first part of the
assignment.

Now to move onto Part 2:
Reading a Web Page with Beautiful Soup - following the example starton page 300 - 304 of Data Wrangling with Python, use
the Beautiful Soup Python library to scrap a web page. The result should be data and output in an organized format. Each
of the data entries should be in its own dictionary with matching keys.
'''
