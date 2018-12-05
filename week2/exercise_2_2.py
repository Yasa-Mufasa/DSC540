'''
DSC 540 - T301 Data Preparation
Exercise 2.2: Python Basics
'''

'''
What tools will you be using for the class and which version of Python? Jupyter Notebook, PyCharm, Anaconda, etc?
    I will be using Python 3.7. I enjoy exploring the newer material that is available in the newest version of Python.
    Being newer to Python, this may not be the best of options, but but I figure learning on the newest version would be
    easier than trying to learn both 2.X and 3.X at the same time. I know that not everything is backwards compatible
    between 3.X and 2.X. I'm hoping that as I learn more about 3.X, writing code for 2.X won't be as challenging as I
    will still be learning Python.
    
    I will be using PyCharm as my IDE. It's the IDE that I have the most experience in at the moment. I will also be
    exploring Sublime and Atom to see which is the best fit for me. If either works better for me, I will switch over to
    the IDE that works best for me.    



Complete the following using Python - make sure to show your work and show the values returned. You can submit via your
notebook or code editor, no need to export your work.
'''

# Change case in a string

# This can be done by either capitalizing something, or changing a capital letter to a lower case letter

change_case = "HeLlO"
print(change_case)
change_case = change_case.lower()
print(change_case)
change_case = change_case.upper()
print(change_case)

'''
Here we can see that all of the letters have been changed by making everything lowercase and then capitalizing every
letter. I went ahead and reassigned each variable to show that the string was changing. If you just want to see the
changing case of the letters, rather than changing the original string, the following code would display the changing
cases:

change_case = "hElLo"
print(change_case.lower())
print(change_case.upper())
'''

# Strip space off the end of a string

strip_string = 'Hello, World! '
print(strip_string.strip(' '))

'''
This code snippet prints 'Hello, World!' without the trailing space. Technically, you don't need to tell the strip
method that it needs to strip the space. strip_string.strip() would strip the trailing space without any issues.
If the stripped version of the variable is needed, the variable could be redefined as above.
'''

# Split a string

# I'm going to make a string of random characters and split it by 'a'.

random_string = 'kjodiajndowiand'
print(random_string.split('a'))

'''
Here we have that the string was split any time the character 'a' appeared. The split results in a list of the string
fragments.
'''

# Add and subtract integers and decimals

# This is easy enough.
print(1 + 2)
print(4 - 7)
print(1.4 + 5.2)
print(6.6 - 2.3)

# Create a list

my_list = ['Mountain Dew', 'Pepsi', 'Coke', 'Dr. Pepper']
print(my_list)

'''
This creates a list of 4 different sodas. These are the 4 most recent sodas I've had.
'''

# Add to the list

my_list.append('Crush')
print(my_list)

'''
This adds Crush to the list. It was the next soda I could think of.
'''

# Subtract from the list

my_list.remove("Pepsi")
print(my_list)

'''
This removes Pepsi from the list. I'm sorry Pepsi fans
'''

# Remove the last item from the list

# There are a couple of ways to do this. You could use the remove command again, or you could slice the list

my_list = my_list[0:3]
print(my_list)

'''
Slicing using the list indexes to work. Indexing in Python starts with 0. The first number in the slice is inclusive, so
the 0th index will be included. The ending index number of the slice is not inclusive, it's exclusive. This means the
slice will start from the 0th index and go up to the 3rd index, but not include the 3rd index. If you don't know how
long the list is but want to cut off the last list entry, you can do

my_list[0:(len(my_list)-1)])

Just remember that lists are mutable, and don't forget the print() statement.
'''

# Reorder the list

# I'm going to reorder the list by reversing the list

my_list.reverse()
print(my_list)

'''
This command reverses the list and then prints it.
'''

# Sort the list

my_list.sort()
print(my_list)
my_list.sort(reverse = True)
print(my_list)

'''
This snippet of code first sorts the list alphabetically from A to Z, and then sorts the list alphabetically from Z to A.
'''

# Create a dictionary

my_dict = {'ps4': 14, 'xbox_one': 4, 'switch': 9}
print(my_dict)

'''
This creates a dictionary record of the number of games for given gaming consoles.
'''

# Add a key-value to the dictionary

my_dict['desktop'] = 24
print(my_dict['desktop'])
print(my_dict)

'''
Here we can see that the dictionary record key of 'desktop' was added to the dictionary with the value of 24. I printed
the full dictionary to prove that the record was added to the dictionary.
'''

# Set a new value to corresponding key in dictionary

my_dict['switch'] = 15
print(my_dict['switch'])
print(my_dict)

'''
Here we can see that the value for the key 'switch' changed to 15.
'''

# Look a new value by the key in dictionary

# I'm not entirely sure what's being asked here. I'm assuming this is asking me to look at the value by calling the key

print(my_dict['ps4'])

'''
Here we see the value for the key of 'ps4'
'''
