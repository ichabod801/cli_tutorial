"""
menu_class.py

A simple menu example with a class.

Classes:
Menu: A basic menu interface. (object)
"""

from collections import OrderedDict
from string import ascii_uppercase

class Menu(object):
    """
    A basic menu interface for an integer graph. (object)

    Class Attributes:
    menu_data: The menu descriptions and function names. (dict of str: str)
    primes: The prime numbers up to the first one over 100. (list of int)

    Attributes:
    choices: The letter choices and their descriptions. (OderedDict of str: str)
    numbers: The current sequence of numbers. (list of int)
    prompt: The text displayed when requesting a user's choice. (str)
    quit_char: The letter choice for exiting the menu loop. (str)

    Methods:
    collatz: Collatz the last number in the sequence and append it. (None)
    fibonacci: Add the last two numbers in the sequence and append the sum. (None)
    menu_loop: Loop through menu choices, performing the relevant actions. (None)
    prime: Append the next highest prime to the sequence. (None)

    Overridden Methods:
    __init__
    """

    # The menu descriptions and function names.
    menu_data = OrderedDict([('Add the last two numbers.', 'fibonacci'), 
        ('Get the next prime number.', 'prime'), ('Collatz the last number.', 'collatz')])
    # All of the prime numbers up to just over 100.
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
    primes += [97, 101]

    def __init__(self, prompt='Please enter your choice: '):
        """
        Set up the class attributes. (None)

        Parameters:
        prompt: The text displayed when requesting a user's choice. (str)
        """
        # Store the parameters.
        self.prompt = prompt
        # Set up the menu.
        self.choices = OrderedDict(zip(ascii_uppercase, self.menu_data.keys()))
        self.quit_char = ascii_uppercase[len(self.menu_data)]
        # Set up the sequence information.
        self.numbers = [0, 1]

    def collatz(self):
        """Collatz the last number in the sequence and append it. (None)"""
        # Triple and add one to odd numbers.
        if self.numbers[-1] % 2:
            self.numbers.append(self.numbers[-1] * 3 + 1)
        # Halve even numbers.
        else:
            self.numbers.append(self.numbers[-1] // 2)

    def fibonacci(self):
        """Add the last two numbers in the sequence and append the sum. (None)"""
        self.numbers.append(self.numbers[-1] + self.numbers[-2])

    def menu_loop(self):
        """Loop through menu choices, performing the relevant actions. (None)"""
        # Loop until the user quits or the sequence goes over 100.
        while self.numbers[-1] < 100:
            # Display the menu.
            for char, menu_text in self.choices.items():
                print('{}: {}'.format(char, menu_text))
            print('{}: Quit\n'.format(self.quit_char))
            # Get the response.
            choice = input(self.prompt).upper()
            # Handle the response.
            if choice == self.quit_char:
                break
            elif choice in self.choices:
                method = self.menu_data[self.choices[choice]]
                getattr(self, method)()
                print('The current number is {}.'.format(self.numbers[-1]))
            else:
                print('That is not a valid choice.')
        # Clean up.
        print('Have a nice day.')

    def prime(self):
        """Append the next highest prime to the sequence. (None)"""
        self.numbers.append([p for p in self.primes if p > self.numbers[-1]][0])

if __name__ == '__main__':
    menu = Menu()
    menu.menu_loop()