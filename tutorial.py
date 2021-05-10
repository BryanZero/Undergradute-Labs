#Python Tutorial

# This is a comment

'''This is a multi-line
string which acts as a comment.'''

#We don't have to declare the type of variables, they are automatically assigned.
testInt = 5
testFloat = 5.3
testStr = 'String'
testTuple = ('Hello',2,5,'Test')
testDictionary = {'A': 'Apples', 'B': 'Bananas'}
testList = [1,2,3]
testList2 = [[1,2,3],[4,5,6]]
#You can make a list of lists and a dictionary of dictionaries
#This is how you make multi-dimensional arrays

x = range(1,10)
#x will be a range(1,10)

#While loop
while True:
    print('hi') #This is how you print
    break
#The for loop in python is extremely responsive

for k in range(50): #range is self explanatory
    print(k) #This will print 0-49, python starts at 0 like any good programming language.

for i in x: #x was defined earlier.
    print(i)

for k in testStr:
    print(k) #This will print out every character in testStr.

for k in testTuple:
    print(k) #This will print out each element in the tuple.

#Now the way that for loops work you might want to iterate through a specific number of element instead of interacting with the element itself,
for k in range(len(testTuple)): #len() gets the length of a tuple or a string
    print(k) #This will print 0,1,2,3
    print(testTuple[k]) #This will print out the elements of testTuple
    print(testTuple[k-1]) #This will print out the elements of testTuple starting from the last element (testTuple[-1] will give you the last element)

#Formmatting
print('Testing\n') #Print testing and make a new line
print('Testing' + testStr) #This concatenates the two strings.
#print('Testing' + testInt) #This will not work, it will return an error
print('Testing' + str(testInt)) #This will work
print(b'01010100') #This will convert a string to bytes
print(r'Testing\nTesting\nTestinng') #This will convert the string to a raw string which will result in \n not working.

print(f'{testStr} you smell this much: {testInt}') #This will allow you to call variables in your string.
print('%s'% testStr) #Another type of formatting.
print('{} Testing {}'.format(testStr,testInt)) #Yet another way to format


#This is how you define a function
def funcname():
    return
#This is how you define a function with arguments
def funcname(arg1,arg2):
    print(arg1)
    print(arg2)
#Notice that no return is needed
funcname('Testing 1','testing 2')
#This will return
#>>'Testing 1'
#>>'Testing 2'

#In order to define optional arguments you can do:
def funcname(option1=None,option2='Hello'):  #option1 is the option name and what you're defining is the default value.
        print(option1)
        print(option2)
funcname() #This will return
#>>None
#>>'Hello'

def funcname(*args):  #This lets you feed as many args as you want and it will store it in a tuple.
    print(args)
funcname('Hello',5,'Test')
#>>('Hello',5,'Test')

def funcname(**args): #This lets you push through keyword arguments and stores it in a dictionary by default.
    print(args)
funcname(a=123,b=456)
#>>{'a': 123, 'b': 456}

#So let's talk quickly about what * and ** actually does, * unpacks a tuple so for example, **will unpack a dictionary
exampleTuple = (1,2,3,4,5,6,7,8)
a,b,c,d,e,f,g,h = exampleTuple #This will define a to be 1 b to be 2 and etc...
print(exampleTuple) #This will print out the tuple
#>>(1, 2, 3, 4, 5, 6, 7, 8)
print(*exampleTuple) #This will unpack the tuple and then the print will print each element
print(1,2,3,4,5,6,7,8) #Same result as above
#>>1 2 3 4 5 6 7 8

#You can google everything else, numpy is a very popular module
try: #Try will attempt to run a command
    import numpy as np
except: #This will expect an error and if so will run the following commands.
    print('An error has occurred')

numpyArray = np.asarray([1,2,3,4,5,6,7,8])
#What it lets you do is seemlessly interact with arrays
testResult = numpyArray + 5
#testResult will be a numpy array of all the elements plus whatever you did to it so in this case, 6,7,8,9,10...
#>>array([ 6,  7,  8,  9, 10, 11, 12, 13])
#Numpy is extremely powerful for handling data.


#List Comprehension
print([x for x in range(6) if x >3])
#List comprehension goes a little something like this [{output} for {item} in {something} if {filter})
#It must be in brackets in order to be "packed" into a list otherwise it will be a generator class

# You also have ternary operators notice that these do not have to be in brackets and will be converted to a list if put in brackets
x,y = 50,25
small = x if x < y else y
print(x if x < y else y) # Same as print(small)
#>> 25

#Now try this challenge
'''Take a list, say for example this one:

  a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
and write a program that prints out all the elements of the list that are less than 5.

Extras:

Instead of printing the elements one by one, make a new list that has all the elements less than 5 from this list in it and print out this new list.
Write this in one line of Python.
Ask the user for a number and return a list that contains only elements from the original list a that are smaller than that number given by the user.'''


import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.ylabel('some numbers')
plt.show()