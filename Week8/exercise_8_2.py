'''
DSC 540

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
from bs4 import BeautifulSoup
from lxml import html
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver

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
print('Section 1:')
print('')
print(google[:200])     # prints the first 200 characters

url = 'http://google.com?q='
url_with_query = url + urllib.quote_plus('python web scraping')

'''
Huh, that's actually pretty cool. Would it work for any website? Let's try it on Bellevue's main page.
'''

bell = urllib2.urlopen('http://www.bellevue.edu')
bell = bell.read()
print('')
print("Bellevue's Web Page")
print(bell[:200])

'''
It really does work! But let's now move on with looking at some of the things you can do with the request library
'''

google = requests.get('http://google.com')
print('Status Codes:')
print(google.status_code)
print('')
print('First 200 Characters:')
print(google.content[:200])
print('')
print('Headers:')
print(google.headers)
print('')
print('Cookies:')
print(google.cookies.items())

'''
That's cool, and helps give more information than I was thinking it would. And this concludes the first part of the
assignment.

Now to move onto Part 2:
Reading a Web Page with Beautiful Soup - following the example starting on page 300 - 304 of Data Wrangling with Python, use
the Beautiful Soup Python library to scrap a web page. The result should be data and output in an organized format. Each
of the data entries should be in its own dictionary with matching keys.
'''

page = requests.get('http://www.enoughproject.org/take_action')
bs = BeautifulSoup(page.content, features="html.parser")
print('Title:')
print(bs.title)
print('')
print("All a's:")
print(bs.find_all('a'))
print('')
print("All p's:")
print(bs.find_all('p'))

'''
That's a lot but shows that you can grab what you need with the right requests.

Now let's look at the family relationships in the HTML
'''

header_children = [c for c in bs.head.children]
# print('Header Children')
# print(header_children)

navigation_bar = bs.find(id="globalNavigation")

# for d in navigation_bar.descendants:
#     print(d)
#
# for s in d.prevous_siblings:
#     print(s)

'''
Looks like these won't work because there is nothing in navigation_bar. Looks like the website has been updated since
our textbook was published and all of the "globalNavigation" have been removed. I double checked the website as well.
Searching for "global" finds 1 location, and searching for "navigation" finds 6, but no instances of "globalNavigation".
'''

page = requests.get('http://www.enoughproject.org/take_action')
bs = BeautifulSoup(page.content, "lxml")
ta_divs = bs.find_all("div")    # removed the "class_='views-row'" option. This caused it to work.
print(len(ta_divs))
for ta in ta_divs:
    title = ta.h2
    link = ta.a
    about = ta.find_all('p')
    print(title, link, about)

'''
Hmmmm, I'm getting that there are no ta_divs. Let's check the website to see how many there are.
Huh, I see that there are 124 "div" within the HTML. So why didn't it find them all?

By removing the "class_='views-row'", I was now able to find 100 instances of this.
'''

all_data = []
# for ta in ta_divs:
#     data_dict = {}
#     data_dict['title'] = ta.h2.get_text()
#     data_dict['link'] = ta.a.get('href')
#     data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
#     all_data.append(data_dict)
#
# print(all_data)
# Commenting out to try completing the same thing using the lxml package
'''
Looks like the website has been updated even more. I'm running into the same issue as before, but in this case, there are
no h2 attributes. But that completes this section of the textbook. Before moving on, though, I want to try to complete
this section, but by using the lxml package.
'''

# page = html.parse('http://enoughproject.org/take_action')
# root = page.getroot()
# ta_divs = root.cssselect('div.views-row')
# all_data = []
# for ta in ta_divs:
#     data_dict = {}
#     title = ta.cssselect('h2')[0]
#     data_dict['title'] = title.text_content()
#     data_dict['link'] = title.find('a').get('href')
#     data_dict['about'] = [p.text_content() for p in ta.cssselect('p')]
#     all_data.append(data_dict)
# print(all_data)

'''
Looks like I'm running into another issue. The parser isn't able to find the website. Well, that's irritating. I wonder
if it would work using a different website? But which one? Why not Bellevue's webiste again?
'''

page = html.parse('http://www.bellevue.edu')
root = page.getroot()
ta_divs = root.cssselect('div.views-row')
all_data = []
for ta in ta_divs:
    data_dict = {}
    title = ta.cssselect('h2')[0]
    data_dict['title'] = title.text_content()
    data_dict['link'] = title.find('a').get('href')
    data_dict['about'] = [p.text_content() for p in ta.cssselect('p')]
    all_data.append(data_dict)
print(all_data)

'''
Well, it sort of works. This produces an empty list of dictionaries, unfortunately. This could be because this script is
not personalized to Bellevue's website. Either that, or the 'views-row' command isn't doing what I'm expecting it to.
Anyway, this completes this section

Now it's time to move onto Part 3:
Web scraping with Selenium - Follow along with your book starting on page 318 - 329 of Data Wrangling with Python. At
the end of the exercise, you should be able to go to a site, fill out a form, submit the form, and then scroll through
the results with the code you wrote. Make sure to submit teh code and your output.
'''

browser = webdriver.Chrome()
browser.get('http://www.fairphone.com/we-are-fairphone/')
browser.maximize_window()

'''
Looks like this website isn't available. I'm being redirected to https://www.fairphone.com/en/community/ instead. Let's
see if it can still work, though.
'''

iframe = browser.find_element_by_xpath('//iframe')
new_url = iframe.get_attribute('src')
browser.get(new_url)

all_data = []
all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')

for elem in all_bubbles:
    elem_dict = {'full_name': None,
                 'short_name': None,
                 'text_content': None,
                 'picture': None,
                 'timestamp': None,
                 'original_link': None,
                 }
    content = elem.find_element_by_css_selector('div.content')
    try:
        elem_dict['full_name'] = content.find_element_by_css_selector('div.fullname').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['short_name'] = content.find_element_by_css_selector('div.name').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['text_content'] = content.find_element_by_css_selector('div.twine-description').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['timestamp'] = elem.find_element_by_css_selector('div.when').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['original_link'] = elem.find_element_by_css_selector('div.when a').get_attribute('href')
    except NoSuchElementException:
        pass
    try:
        elem_dict['picture'] = elem.find_element_by_css_selector('div.picture img').get_attribute('src)')
    except NoSuchElementException:
        pass
    all_data.append(elem_dict)

print(all_data)
browser.quit()


'''
Alright, this is giving me another blank list, which isn't surprising. I'm not looking at the same page and the page I'm
looking at isn't set up the same. But let's go ahead and finish up this section when following the textbook.
'''


def find_text_element(html_element, element_css):
    try:
        return html_element.find_element_by_css_selector(element_css).text
    except NoSuchElementException:
        pass
    return None


def find_attr_element(html_element, element_css, attr):
    try:
        return html_element.find_element_by_css_selector(element_css).get_attribute(attr)
    except NoSuchElementException:
        pass
    return None


def get_browser():
    browser = webdriver.Chrome()
    return browser


def main():
    browser = get_browser()
    browser.get('http://apps.twinesocial.com/fairphone')

    all_data = []
    browser.implicitly_wait(10)
    try:
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
    except WebDriverException:
        browser.implicitly_wait(5)
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
    for elem in all_bubbles:
        elem_dict = {}
        content = elem.find_element_by_css_selector('div.content')
        elem_dict['full_name'] = find_text_element(content, 'div.fullname')
        elem_dict['short_name'] = find_attr_element(content, 'div.name', 'innerHTML')
        elem_dict['text_content'] = find_text_element(content, 'div.twine-description')
        elem_dict['timestamp'] = find_attr_element(elem, 'div.when a abbr.timeago', 'title')
        elem_dict['original_link'] = find_attr_element(elem, 'div.when a', 'src')
        elem_dict['picture'] = find_attr_element(content, 'div.picture img', 'src')
        all_data.append(elem_dict)
    browser.quit()
    return all_data


if __name__ == '__main__':
    all_data = main()
    print(all_data)

browser = webdriver.Chrome()
browser.get('http://www.google.com')
inputs = browser.find_elements_by_css_selector('from input')
for i in inputs:
    if i.is_displayed():
        search_bar = i
        break

search_bar.send_keys('web scraping with python')
search_button = browser.find_element_by_css_selector('form button')
search_button.click()
browser.implicitly_wait(10)
results = browser.find_elements_by_css_selector('div h3 a')
for r in results:
    action = webdriver.ActionChains(browser)
    action.move_to_element(r)
    action.perform()
    sleep(2)
browser.quit()
