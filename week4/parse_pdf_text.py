pdf_txt = 'en-final-table9.txt'
openfile = open(pdf_txt, "r")

double_lined_countries = [
    'Bolivia (Plurinational \n',
    'Democratic People\xe2\x80\x99s \n',
    'Deomcratic Republic \n',
    'Lao People\xe2\x80\x99s Democratic \n',
    'Micronesia (Federated \n',
    'Saint Vincent and \n',
    'The former Yugoslav \n',
    'United Republic \n',
    'Venezuela (Bolivarian \n'
]

def turn_on_off(line, status, prev_line, start, end='\n', count=0):
    '''
    This function checks to see if a line starts/ends with a certain value. If the line starts/ends with that value,
    the status is set to on/off (True/False) as long as the previous line isn't special.
    :param line: the line we are evaluating
    :param status: a Boolean (True of False) representing whether it is on or off
    :param start: what we are looking for as the start of the section -- this will trigger the on or True status
    :param end: is what we are looking for as the end of the section -- this will trigger the off or False status
    :return:
    '''
    if line.startswith(start):
        status = True
    elif status:
        if line == end and prev_line != 'and areas':
            status = False
    return status


def clean(line):
    '''
    Cleans line breaks, spaces, and special characters from our line
    :param line: the line we want to clean
    :return:
    '''
    line = line.strip('\n').strip()
    line = line.replace('\xe2\x80\x93', '-')
    line = line.replace('\xe2\x80\x99', '\'')
    return line


countries = []
totals = []
country_line = total_line = False
previous_line = ''

for line in openfile:
    if country_line:
        if previous_line in double_lined_countries:
            line = ' '.join([clean(previous_line), clean(line)])
            countries.append(line)
        elif line not in double_lined_countries:
            countries.append(clean(line))

    elif total_line:
        if len(line.replace('\n', '').strip()) > 0:
            totals.append(clean(line))

    country_line = turn_on_off(line, country_line, previous_line, 'and areas')
    total_line = turn_on_off(line, total_line, previous_line, 'total')
    previous_line = line

import pprint
data = dict(zip(countries, totals))
pprint.pprint(data)
