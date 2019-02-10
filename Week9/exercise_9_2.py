'''
DSC 540
Exercise 9.2: Pulling Data from APIs
Joshua Gardner
'''

import oauth2
import json
import tweepy
import dataset

'''
Complete the following using Python - make sure to show your work and show the values returned. YOu can submit via your
notebook or code editor, no need to export your work.

In this exercise, you will create a twitter account (if you don't already have one, or don't wish to use your personal
account) and practice pulling data from Twitter's publically available API. You can delete the twitter account as soon
as you have completed the exercise. Include your code and output for each step.
    1. Create a Twitter API Key and Access Token (Data Wrangling with Python, pg 365 - 366)
    2. Do a single data pull from Twitter's REST API (Data Wrangling with Python, pg 366 - 368)
    3. Execute multiple queries at a time from Twitter's REST API (Data Wrangling with Python, pg 368 - 371)
    4. Do a data pull from Twitter's Streaming API (Data Wrangling with Python, pg 372 - 374)
'''

'''
Part 1 - Create a Twitter API Key and Access Token (Data Wrangling with Python, pg 365 - 366)

The first step to working on this is that you need to have an account with Twitter. I don't want to use my personal
Twitter account for this yet, so I'm creating an account at https://twitter.com/signup. This is taking more time than
I was expecting it to. I didn't realize that the request needed to go through a verification process with Twitter now.
I started this project on Saturday with it due tomorrow, so I may or may not gain access to Twitter's API in time. Once
I have those values, I will put them here.
'''

API_KEY = ''
API_SECRET = ''
TOKEN_KEY = ''
TOKEN_SECRET = ''

'''
And that will complete this section for now.
'''

'''
Part 2 - Do a single data pull from Twitter's REST API (Data Wrangling with Python, pg 366 - 368)

This is going to depend on which API_KEY, API_SECRET, TOKEN_KEY, and TOKEN_SECRET I get from Twitter. Once I have those,
I can run the following to actually request information from Twitter.
'''

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content


url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23childlabor'
data = oauth_req(url, TOKEN_KEY, TOKEN_SECRET)
print(data)     # This prints out the obtained data to verify the program worked. It should return it as in JSON format

'''
This should display the data as a string. We could try to parse through the string, or we can use the json library to
import the data as it's a .json file.
'''
data = json.loads(data)     # This reloads the data using the json library and rewrite the data variable.
print(type(data))           # This should return a Python dictionary.

with open('tweet_data.json', 'wb'):     # This will write the data to a file so I can parse through it later.
    data_file.write(data)

'''
If I want to parse through this, Chapter 3 of Data Wrangling with Python has a great walk through of how to do so.

This also concludes Part 2 of the assignment.
'''


'''
Part 3 - Execute multiple queries at a time from Twitter's REST API (Data Wrangling with Python, pg 368 - 371)

The first thing we should do is reset our API_KEY, API_SECRET, TOKEN_KEY, and TOKEN_SECRET. This will reset them and
undo any changes that were made to them in the previous section.
'''

API_KEY = ''
API_SECRET = ''
TOKEN_KEY = ''
TOKEN_SECRET = ''

# auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
# auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)
# api = tweepy.API(auth)
# query = '#childlabor'
# cursor = tweepy.Cursor(api.search, q=query, lang="en")

'''
We now need a place to save the data. An easy way to do this is to create a directory called data in the same directory
as the script and run 'mkdir data' in the command line. Since I'm using PyCharm, I can just make the file here.

Once the data directory is made, we can iterate over the different pages of Twitter data and save it.
'''

# for page in cursor.pages():
#     tweets = []
#     for item in page:
#         tweets.append(item._json)
#
# with open('data/hashchildlabor.json', 'wb') as outfile:
#     json.dump(tweets, outfile)


def store_tweet(item):
    db = dataset.connect('sqlite:///data_wrangling.db')
    table = db['tweets']
    item_json = item._json.copy()
    for k, v in item_json.items():
        if isinstance(v, dict):
            item_json[k] = str(v)
    table.insert(item_json)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

api = tweepy.API(auth)
query = '#childlabor'
cursor = tweepy.Cursor(api.search, q=query, lang="en")

for page in cursor.pages()
    for item in page:
        store_tweet(item)


'''
Alright, and that concludes this section.
'''

'''
Part 4 - Do a data pull from Twitter's Streaming API (Data Wrangling with Python, pg 372 - 374)

Everything up to now has been working with Twitter's REST API. Now let's take a look at Twitter's Streaming API.
'''
