########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Karina Abad
# Student ID: 918533530
# Student Github Username: karinaaltheaabad
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given.
#               No unit test are provided for lab #0
########################################################################################################################

########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Karina Althea F. Abad"
SID = 918533530
git_username = "karinaaltheaabad" 
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, 
then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************")  # problem header (don't modify)


# TODO: your code here

# convert user input from string to integer
def convert_to_int(number):
    return int(input(number))


def evaluate_input(first, second):
    if (first * second) > 500:
        return first + second
    return first * second


for i in range(2):
    x = convert_to_int("Enter the first integer: ")
    y = convert_to_int("Enter the second integer: ")
    print("Result is", evaluate_input(x, y))

########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting" 
the sample output would be: 'Alice' found 2 times. 
"""
print("Problem 2 ********************")  # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here

word = myString.split()


def word_count(count=0):
    for w in word:
        if w == "Alice":
            count += 1
    return count


print("\'Alice\' found", word_count(), "times.")

########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************")  # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here

total = 0

for i in range(len(numbers) - 1):
    total = numbers[i] + numbers[i + 1]
    print(total)

########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending order. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************")  # problem header (don't modify)


# function skeleton
def merge_odds(l1, l2):
    odds = []
    temp = l1 + l2
    for i in range(len(temp)):
        if temp[i] % 2 == 1:
            odds.append(temp[i])
    return sorted(odds)


l1 = [2, 1, 5, 7, 9]
l2 = [32, 33, 13]
odds = merge_odds(l1, l2)
print(odds)

########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************")  # problem header


# function skeleton
def merge_odds(l1, l2):
    odds = {}
    for i in range(len(l1)):
        if l1[i] % 2 == 1:
            odds[i] = []
            odds[i].append(l1[i])
            if i < len(l2):
                odds[i].append(l2[i])
    return odds


l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)
