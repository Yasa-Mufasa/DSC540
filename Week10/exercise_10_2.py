'''
DSC 540
Exercise 10.2: Logging and Automation
'''

'''
Complete the following using Python - make sure to show your work and show the values returned. You can submit via your
notebook or code editor, no need to export your work.

Part 1:
Add python logging to previous code that yu have written. In your logging, include a note to yourself with the area of
the code writing the message so you know where the error occurred. Incldue your code and output in your submitted
assignment. An example of this can be found on page 406 - 408 of your text, Data Wrangling with Python.

Part 2:
Add an automated message to previous code that you have written. You can choose to do an email, text, or call. Make sure
to include the failure/ success in your message. Include your code and output in your submitted assignment. An example
of this can be found on page 408 - 412 of your text Data Wrangling with Python.
'''

'''
Part 1:
Add Python logging to previous code that you have written. In your logging, include a note to yourself with the area of
the code writing the message so you know where the error occurred. Include your code and output in your submitted
assignment. An example of this can be found on page 406 - 408 of your text, Data Wrangling with Python

To start with, I'm going to follow along with the book's examples. Once I've run through the examples of the book, I
will either come up with some new code, or grab a portion of code used in a previous exercise.
'''

import logging
from datetime import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import ConfigParser
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver


def start_logger():
    logging.basicConfig(filename='C:\Users\yasam\OneDrive\Documents\Workspaces\DSC540\Week10\Logs\Logs_report_%s.log' %
                        datetime.strftime(datetime.now(), '%m%d%Y_%H%S'),
                        level = logging.DEBUG,
                        format = '$(asctime)s %(message)s',
                        datefmt = '%m-%d %H:%M:%S')


# def main():
#     start_logger()
#     logging.debug("SCRIPT: I'm starting to do things!")
#
#     try:
#         20 / 0
#     except Exception:
#         logging.exception('SCRIPT: We had a problem!')
#         logging.error('SCRIPT: Issue with division in the main() function')
#
#     logging.debug('SCRIPT: About to wrap things up')



# if __name__ == '__main__':
#     main()

# Commenting out section so I don't rerun it each time.

'''
Alright, seems to be working. The above example creates the log where I want it to. Why not reuse some code from
exercise_8_2.py? I will need to add the logging comments to each part.
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
    start_logger()
    logging.debug('SCRIPT: Getting browser')
    browser = get_browser()
    browser.get('http://apps.twinesocial.com/fairphone')

    all_data = []
    browser.implicitly_wait(10)
    try:
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
        logging.debug('SCRIPT: find_elements_by_css_selector for div.twine-item-border successful')
    except WebDriverException:
        browser.implicitly_wait(5)
        logging.error('ERROR: initial find_elements_by_css_selector unsuccessful, trying again after waiting 5 seconds')
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
    for elem in all_bubbles:
        logging.debug('SCRIPT: Developing dictionary record')
        elem_dict = {}
        content = elem.find_element_by_css_selector('div.content')
        logging.debug('SCRIPT: adding div.content')
        elem_dict['full_name'] = find_text_element(content, 'div.fullname')
        logging.debug('SCRIPT: adding div.fullname')
        elem_dict['short_name'] = find_attr_element(content, 'div.name', 'innerHTML')
        logging.debug('SCRIPT: adding div.name and innerHTML')
        elem_dict['text_content'] = find_text_element(content, 'div.twine-description')
        logging.debug('SCRIPT: adding div.twine-description')
        elem_dict['timestamp'] = find_attr_element(elem, 'div.when a abbr.timeago', 'title')
        logging.debug('SCRIPT: adding div.when a abbr.timeago and title')
        elem_dict['original_link'] = find_attr_element(elem, 'div.when a', 'src')
        logging.debug('SCRIPT: adding div.when a and src')
        elem_dict['picture'] = find_attr_element(content, 'div.picture img', 'src')
        logging.debug('SCRIPT: adding pictures and src')
        all_data.append(elem_dict)
        logging.debug('SCRIPT: adding all dictionary records to list')
    browser.quit()
    logging.debug('SCRIPT: Closing browser')
    return all_data


if __name__ == '__main__':
    all_data = main()
    print(all_data)


'''
Sweet, it worked! I probably overly logged this code snippet as I'm logging that I've found each element.
'''

'''
Part 2:
Add an automated message to previous code that you have written. YOu can choose to do an email, text or call. Make sure
to include the failure/ success in your message. Include your code and output in your submitted assignment. An example
of this can be found on page 408 - 412 of your Data Wrangling with Python.

Once again, I'll start with the book's example, and then modify some of my code from previous exercises.
'''


def get_config(env):
    config = ConfigParser.ConfigParser()
    if env == "DEV":
        config.read(['config/development.cfg'])
    elif env == "PROD":
        config.read(['config/production.cfg'])
    return config


def mail(to, subject, text, attach=None, config=None):
    if not config:
        config = get_config("DEV")
    msg = MIMEMultipart()
    msg['From'] = config.get('email', 'user')
    msg['To'] = ", ".join(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'r').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(config.get('email', 'user'),
                     config.get('email', 'password'))
    mailServer.sendmail(config.get('email', 'user'), to, msg.as_string())
    mailServer.close()


def example():
    mail(['listof@mydomain.com', 'emails@mydomain.com'],
         "Automate your life: sending emails",
         "Why'd the elephant sit on the marshmallow?",
         attach="my_file.txt")


