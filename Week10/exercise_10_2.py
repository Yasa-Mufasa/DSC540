'''
DSC 540
Exercise 10.2: Logging and Automation
Joshua Gardner
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


def start_logger():
    logging.basicConfig(filename='C:\Users\yasam\OneDrive\Documents\Workspaces\DSC540\Week10\Logs\Logs_report_%s.log' %
                        datetime.strftime(datetime.now(), '%m%d%Y_%H%S'),
                        level = logging.DEBUG,
                        format = '$(asctime)s %(message)s',
                        datefmt = '%m-%d %H:%M:%S')


def main():
    start_logger()
    logging.debug("SCRIPT: I'm starting to do things!")

    try:
        20 / 0
    except Exception:
        logging.exception('SCRIPT: We had a problem!')
        logging.error('SCRIPT: Issue with division in the main() function')

    logging.debug('SCRIPT: About to wrap things up')


if __name__ == '__main__':
    main()

'''
Alright, seems to be working. The above example creates the log where I want it to. Now to grab some previous code and
add logging to it. I'm assuming I can use a snippet of code to add logging to.
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


