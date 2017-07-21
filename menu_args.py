"""
menu.py

A simple menu example.

Constants:
PRIMES: The prime numbers up to the first one over 100. (list of int)

Functions:
menu: A generic menu function. (None)
collatz: Collatz the last number in the sequence and append it. (list of int)
fibonacci: Add the last two numbers in the sequence and append. (list of int)
prime: Append the next highest prime to the sequence. (list of int)
"""

from collections import OrderedDict
import string
import time

# The prime numbers up to the first one over 100.
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
PRIMES.append(101)

def menu(menu_data, prompt = 'Please enter your choice: '):
    """
    A generic menu function.

    The menu_data dictionary keys are strings that are shown in the menu. The 
    values of the dictionary should be functions that are called when the menu
    item is chosen. If the order of the menu items is important, this should
    be an OrderedDict from collections.

    Parameters:
    menu_data: The menu items and actions for the menu. (dict of str: callable)
    prompt: The text for getting a menu choice from the user. (str)
    """
    # Set up the menu.
    menu_choices = OrderedDict(zip(string.ascii_uppercase, menu_data.keys()))
    quit_char = string.ascii_uppercase[len(menu_data)]
    # Set up the state.
    args = [[0, 1]]
    kwargs = {}
    # Loop until the user quits.
    while args[0][-1] < 100:
        # Display the menu.
        for char, menu_text in menu_choices.items():
            print('{}: {}'.format(char, menu_text))
        print('{}: Quit\n'.format(quit_char))
        # Get the response.
        choice = input(prompt).upper()
        # Handle the response.
        if choice == quit_char:
            break
        elif choice in menu_choices:
            args, kwargs = menu_data[menu_choices[choice]](*args, **kwargs)
            print('The current number is {}'.format(args[0][-1]))
        else:
            print('That is not a valid choice.')
    # Say goodbye.
    print('Have a nice day.')

def collatz(*args, **kwargs):
    """
    Collatz the last number in the sequence and append it. (list of int)

    The first item of args should be a list of integers.
    """
    # Get the sequence.
    numbers = args[0]
    # If the last number is odd, triple it and add one.
    if numbers[-1] % 2:
        numbers.append(numbers[-1] * 3 + 1)
    # If the last number is even, halve it.
    else:
        numbers.append(numbers[-1] // 2)
    return args, kwargs

def fibonacci(*args, **kwargs):
    """
    Add the last two numbers in the sequence and append. (list of int)

    The first item of args should be a list of integers.
    """
    # Get the sequence.
    numbers = args[0]
    # Add the last two numbers and append the sum.
    numbers.append(numbers[-1] + numbers[-2])
    return args, kwargs

def prime(*args, **kwargs):
    """
    Append the next highest prime to the sequence. (list of int)

    The first item of args should be a list of integers.
    """
    # Get the sequence.
    numbers = args[0]
    # Append the next highest prime.
    numbers.append([p for p in PRIMES if p > numbers[-1]][0])
    return args, kwargs

if __name__ == '__main__':
    math_menu = [('Add the last two numbers.', fibonacci), ('Get the next prime number.', prime), 
        ('Collatz the last number.', collatz)]
    menu(OrderedDict(math_menu))
