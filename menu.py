"""
menu.py

A generic class to build command line menu interfaces. menus built with the 
Menu class work as follows:

1. A menu is displayed, listing the first line of the docstring for each 
	method whose name starts with 'menu_'. After the menu, the status 
	attribute of the class is displayed, if it is not empty.
2. The user may pick one of these options by typing the text before the first
	colon. Frex, if the first line of menu_foo's docstring is 'F: Foo', the 
	user may select that option by typing 'F', causing the menu_foo method to 
	be executed. The selection is case insensitive.
3. Typing in an empty line repeats the last selection by default. This can be
	changed by overriding the emptyline method.
4. If the selection is not recognized, it is passed to the unrecognized
	method.

The Menu class is not meant to be instantiated itself. It would just sit 
there doing nothing if you did. Instead, you can subclass the Menu class
to create your own menu processing systems.

There are stub methods in the Menu class that can be overridden to change 
the menu processing:

    preloop: Add processing before the entire menu loop starts.
    premenu: Add processing before any menu choice is processed.
    postmenu: Add processing after the menu choice is processed.
    postloop: Add processing before the application closes.

There are also three class attributes that are also meant to be overridden:

    intro: Text displayed at the beginning of the menu loop.
    prompt: The text displayed when getting user input.
    sort_key: The sort key for menu items, for non-alphabetical menu choices.

Classes:
Menu: A simple framework for writing command line menus. (object)
"""

import string
import sys

class Menu(object):
    """
    A simple framework for writing command line menus. (object)

    There is no reason to instantiate Menu itself. It should be used as a
    parent class for a menu system that you define yourself.

    Class Attributes:
    intro: Text displayed at the beginning of the menu loop. (str)
    prompt: Text displayed when getting user choices. (str)

    Attributes:
    choice_queue: Automatic commands yet to be proccessed. (list of str)
    lastchoice: The last choice made by the user. (str)
    methods: The mapping of menu choices to methods. (dict of str:bound method)
    status: The status of the menu system, if any. (str)
    stdin_save: Storage for when stdin is redirected. (file)
    stdout_save: Storage for when stdout is redirected. (file)
    text: The text of the menu. (str)

    Methods:
    emptyline: Handle blank choices. (bool)
    menuloop: Repeatedly display a menu, get a choice, and process tit. (None)
    onechoice: Act on a single menu choice. (bool)
    postchoice: Common processing after the choice is proccessed. (bool)
    postloop: Processing done after the menu loop ends. (None)
    prechoice: Process the choice before acting on it. (str)
    preloop: Processing done before starting the menu loop. (None)
    set_menu: Set up the menu text and dictionary. (None)
    sort_menu: Sort the lines of the menu text. (None)
    unrecognized: Handle choices not in the menu. (bool)

    Overridden Methods:
    __init__
    """

    # Text displayed at the beginning of the menu loop.
    intro = ''
    # Text displayed when getting user choices.
    prompt = 'Please enter your selection: '

    def __init__(self, stdin=None, stdout=None):
        """
        Initialize the file interface for the menu system. (None)

        Parameters:
        sort_key: The key parameter when sorting menu choices. (callable)
        stdin: The input file for the menu interface. (file)
        stdout: The output file for the menu interface. (file)
        """
        # Save the stdin before redirecting.
        self.stdin_save = sys.__stdin__
        if stdin is not None:
            sys.stdin = stdin
        # Save the stdout before redirecting.
        self.stdout_save = sys.__stdout__
        if stdout is not None:
            sys.stdout = stdout
        # Set up the menu.
        self.set_menu()
        # Set up the tracking attributes.
        self.lastchoice = ''
        self.status = ''
        self.choice_queue = []

    def emptyline(self):
        """Handle blank choices. (bool)"""
        # Do the last choice over again, if there is one.
        if self.lastchoice:
            return self.onechoice(self.lastchoice)
        else:
            return False

    def menuloop(self, intro=None):
        """
        Repeatedly display a menu, get a choice, and process that choice. (None)

        If the intro parameter is None, the intro attribute of the class is used
        instead.

        Parameters:
        intro: The text to display before the loop begins. (str or None)
        """
        # User defined processing before the loop starts.
        self.preloop()
        # Display any introductory text.
        if intro is not None:
            self.intro = intro
        if self.intro:
            print(self.intro)
        # Loop through the menu choices.
        while True:
            # Process any queued tasks first.
            if self.choice_queue:
                choice = self.choice_queue.pop(0)
            else:
                # Display the menu, with any status.
                print(self.text)
                print()
                if self.status:
                    print('Status:', self.status)
                    print()
                    self.status = ''
                # Get the user's choice.
                choice = input(self.prompt).strip()
            # Process the choice.
            choice = self.prechoice(choice)
            stop = self.onechoice(choice)
            stop = self.postchoice(stop, choice)
            # Check for loop termination.
            if stop:
                break
        # Clean up after the menu loop.
        self.postloop()
        sys.stdin = self.stdin_save
        sys.stdout = self.stdout_save

    def onechoice(self, choice):
        """
        Act on a single menu choice. (bool)

        Parameters:
        choice: The user's menu choice. (str)
        """
        if not choice:
            stop = self.emptyline()
        elif choice.lower() in self.methods:
            stop = self.methods[choice.lower()]()
            self.lastchoice = choice
        else:
            stop = self.unrecognized(choice)
        return stop

    def postchoice(self, stop, choice):
        """
        Common processing after the choice is proccessed. (bool)

        Parameters:
        stop: Flag for stopping the menu loop. (bool)
        choice: The user's choice. (str)
        """
        return stop

    def postloop(self):
        """Processing done after the menu loop ends. (None)"""
        pass

    def prechoice(self, choice):
        """
        Process the choice before acting on it. (str)

        Parameters:
        choice: The original user's choice. (str)
        """
        return choice

    def preloop(self):
        """Processing done before starting the menu loop. (None)"""
        pass

    def set_menu(self):
        """Set up the menu text and dictionary. (None)"""
        menu_lines = []
        self.methods = {}
        for attribute in dir(self):
            if attribute.startswith('menu_'):
                attr = getattr(self, attribute)
                if hasattr(attr, '__doc__'):
                    menu_lines.append(attr.__doc__.strip().split('\n')[0].strip())
                    self.methods[attr.__doc__.split(':')[0].strip().lower()] = attr
        self.sort_menu(menu_lines)
        self.text = '\n' + '\n'.join(menu_lines)

    def sort_menu(self, menu_lines):
        """
        Sort the lines of the menu text. (None)

        Parameters:
        menu_lines: the lines of the menu. (list of str)
        """
        menu_lines.sort(key = lambda line: line.split(':')[0])

    def unrecognized(self, choice):
        """
        Handle choices not in the menu. (bool)

        Parameters:
        choice: The user's menu choice. (str)
        """
        self.status = 'I do not recognize the choice {!r}. Please make another choice.'.format(choice)
        return False
