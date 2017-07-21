"""
menu_test.py

A test of the Menu class.

Classes:
MontyMenu: A menu of Monty Python skits. (Menu)
NumberMenu: A menu of integer graphs. (Menu)
TopMenu: A top level menu. (Menu)
"""

import random
import time

from menu import Menu
from cmd_example2 import Maze

class MontyMenu(Menu):
    """
    A menu of Monty Python skits. (Menu)

    Methods:
    menu_argument: A: Have an intellectual discussion. (bool)
    menu_knight: B: Get some vigorous exercise. (bool)
    menu_quit: D: Stop it, that's just silly. (bool)
    menu_spam: C: Enjoy some fine dining.
    """

    def menu_argument(self):
        """A: Have an intellectual discussion."""
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

    def menu_knight(self):
        """B: Get some vigorous exercise."""
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

    def menu_quit(self):
        """D: Stop it, that's just silly."""
        return True

    def menu_spam(self):
        """C: Enjoy some fine dining."""
        # Get the user's order.
        food = input('What would you like to eat? ')
        # Prepare the meal.
        pre_spam = ['spam'] * random.randint(2, 4)
        post_spam = ['spam'] * random.randint(0, 2) + ['and spam.']
        meal = pre_spam + [food] + post_spam
        # Deliver the food and say goodbye.
        print('Here is your ' + ', '.join(meal))
        input('Press Enter to eat a wafer thin wafer and explode: ')

class NumberMenu(Menu):
    """
    A menu of integer graphs. (Menu)

    Class Attributes:
    primes: All of the prime numbers up to just over 100. (list of int)

    Attributes:
    numbers: The number sequence generated so far. (list of int)

    Methods:
    menu_collatz: 3: Collatz the last number. (bool)
    menu_fibonacci: 1: Add the last two numbers. (bool)
    menu_prime: 2: Go up to the next prime. (bool)
    menu_quit: 4: Quit. (bool)

    Overridden Methods:
    preloop
    postchoice
    postloop
    """
    
    # All of the prime numbers up to just over 100.
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
    primes += [97, 101]

    def menu_collatz(self):
        """3: Collatz the last number."""
        if self.numbers[-1] % 2:
            self.numbers.append(self.numbers[-1] * 3 + 1)
        else:
            self.numbers.append(self.numbers[-1] // 2)

    def menu_fibonacci(self):
        """1: Add the last two numbers."""
        self.numbers.append(self.numbers[-1] + self.numbers[-2])

    def menu_prime(self):
        """2: Go up to the next prime."""
        self.numbers.append([p for p in self.primes if p > self.numbers[-1]][0])

    def menu_quit(self):
        """4: Quit."""
        return True

    def preloop(self):
        """Processing done before starting the choice/action loop. (None)"""
        # Set up number lists.
        self.numbers = [0, 1]
        # Show the starting number.
        self.status = 'The number is now {}.'.format(self.numbers[-1])

    def postchoice(self, stop, choice):
        """
        Common processing after the choice is proccessed. (bool)

        Parameters:
        stop: Flag for stopping the menu loop. (bool)
        choice: The user's choice. (str)
        """
        # Show the current number.
        if not self.status:
            self.status = 'The number is now {}.'.format(self.numbers[-1])
        # Check the current number.
        if self.numbers[-1] > 99:
            return True
        else:
            return stop

    def postloop(self):
        """Processing done after the choice/action loop ends. (None)"""
        print('The final number is {}.'.format(self.numbers[-1]))
        print('Have a nice day.')

    def sort_menu(self, menu_lines):
        """
        Sort the lines of the menu text. (None)

        Parameters:
        menu_lines: the lines of the menu. (list of str)
        """
        menu_lines.sort(key = lambda line: int(line.split(':')[0]))

class TopMenu(Menu):
    """
    A top level menu. (Menu)

    Class Attributes:
    rps_wins: What beats what in rock-paper-scissors. (dict of str: str)

    Methods:
    menu_maze: A: Play in a maze. (bool)
    menu_numbers: B. Play with numbers. (bool)
    menu_rps: C: Play with your hands. (bool)
    menu_quit: E: Quit. (bool)
    menu_words: D: Play with words. (bool)
    """

    # What beats what in rock-paper-scissors. 
    rps_wins = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

    def menu_maze(self):
        """A: Play in a maze."""
        maze = Maze()
        maze.cmdloop()

    def menu_numbers(self):
        """B: Play with numbers."""
        numbers = NumberMenu()
        numbers.menuloop()

    def menu_rps(self):
        """
        C: Play with your hands.

        This is just a game of rock-paper-scissors.
        """
        while True:
            play = input('Rock, paper, or scissors? ').lower()
            bot = random.choice(list(self.rps_wins.keys()))
            if play not in self.rps_wins:
                print("Invalid play. Come on, this is kid's stuff.")
            elif play == bot:
                print('Draw, play again.')
            elif self.rps_wins[play] == bot:
                print('I chose {}. You won!'.format(bot))
                break
            else:
                print('I chose {}. You lose.'.format(bot))
                break

    def menu_quit(self):
        """E: Quit."""
        return True

    def menu_words(self):
        """D: Play with words."""
        words = MontyMenu()
        words.menuloop()


if __name__ == '__main__':
    top = TopMenu()
    top.menuloop()