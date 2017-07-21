"""
menu.py

A simple menu example.

Functions:
simple_menu: The most basic of menu functions. (None)
menu: A generic menu function. (None)
argument: An intellectual discussion. (None)
knight: Some vigorous physical activity. (None)
spam: Fine dining. (None)
"""

from collections import OrderedDict
import random
import string
import time

def simple_menu():
    """
    The most basic of menu functions. (None)
    """
    # Loop until the user quits.
    while True:
        # Show the menu.
        print('A: Have an intellectual discussion.')
        print('B: Get some vigorous exercise.')
        print('C: Enjoy some fine dining.')
        print('D: Quit.')
        # Get the user's choice.
        choice = input('Please enter your choice: ').lower()
        # Process the user's choice.
        if choice == 'a':
            argument()
        elif choice == 'b':
            knight()
        elif choice == 'c':
            spam()
        elif choice == 'd':
            break
        else:
            # Handle invalid choices.
            print('That is not a valid choice.')
    # Be polite.
    print('Have a nice day.')


def menu(menu_data, prompt = 'Please enter your choice: '):
    """
    A generic menu function. (None)

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
    # Loop until the user quits.
    while True:
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
            menu_data[menu_choices[choice]]()
        else:
            print('That is not a valid choice.')
    # Say goodbye.
    print('Have a nice day.')

def argument():
    """
    An intellectual discussion. (None)

    No it isn't.
    """
    # Prep the argument.
    start = time.perf_counter()
    user_text = input('Please state an assertion to argue about: ')
    # Argue for two minutes
    while time.perf_counter() - start < 120:
        # Automatically gainsay whatever the user says. 
        user_words = user_text.lower().split()
        for negative in ('no', 'not', "isn't", "ain't", "doesn't", "wasn't"):
            if negative in user_words:
                user_text = input('Yes it is. ')
        else:
            user_text = input("No it isn't. ")
    # Say goodbye.
    print("I'm sorry, your five minutes is up.")
    input('Press Enter to continue: ')

def knight():
    """Some vigorous exercise. (None)"""
    # Set up the combat.
    limbs = ['other leg', 'leg', 'other arm', 'arm']
    combat = False
    # Loop while the knight has limbs.
    while limbs:
        # None shall pass.
        if not combat:
            print('None shall pass.')
        # Get the user's action.
        user_action = input('What do you do? ')
        # Attacking chops off a limb.
        if user_action.lower() == 'attack':
            print("Excellent attack. You chop off the black knight's {}".format(limbs.pop()))
            combat = True
        # Anything else after attacking provokes an attack.
        elif combat:
            print('The black knight attacks, but you easily block his blow.')
    # Say goodbye.
    input('Press Enter to call it a draw: ')

def spam():
    """Fine dining. (None)"""
    # Get the user's order.
    food = input('What would you like to eat? ')
    # Prepare the meal.
    pre_spam = ['spam'] * random.randint(2, 4)
    post_spam = ['spam'] * random.randint(0, 2) + ['and spam.']
    meal = pre_spam + [food] + post_spam
    # Deliver the food and say goodbye.
    print('Here is your ' + ', '.join(meal))
    input('Press Enter to eat a wafer thin wafer and explode: ')

if __name__ == '__main__':
    monty_menu = [('Have an intellectual discussion.', argument), ('Get some vigorous exercise.', knight),
        ('Enjoy some fine dining.', spam)]
    menu(OrderedDict(monty_menu))
