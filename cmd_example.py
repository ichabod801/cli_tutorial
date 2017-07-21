"""
cmd_example.py

An example of using the cmd module.

This will be a simple maze game, using the below maze stolen from Wikipedia.

+   +-------+-----------+---------------+
|           |           |               |
|   +---+   |   +---+   +   +---+---+   |
|   |       |       |       |   |       |
|   +---+---+---+   +---+   +   |   +---+
|       |       |       |       |   |   |
+---+   |   +---+   +   +---+---+   +   |
|           |       |       |           |
|   +-------+   +   +---+---+   +-------+
|               |       |               |
+---------------+-------+-----------+   +

Constants:
MAP: What directions you can move from each cell in the maze. (list of list)
MAZE: The details of the maze to solve. (dict)

Classes:
Maze: A maze game. (cmd.Cmd)
"""

import cmd
import random

# What directions you can move from each cell in the maze.
MAP = [['se', 'ew', 'ws', 'es', 'we', 'ws', 'es', 'we', 'we', 'ws'],
    ['sn', 'e', 'wn', 'ne', 'sw', 'ne', 'wns', 's', 'se', 'nw'],
    ['ne', 'sw', 'se', 'w', 'nse', 'ws', 'en', 'wn', 'ns', 's'],
    ['se', 'wen', 'wn', 'se', 'nsw', 'ne', 'w', 'se', 'ewn', 'wn'],
    ['ne', 'ew', 'ew', 'nw', 'ne', 'w', 'e', 'wen', 'ew', 'w']]
# The details of the maze to solve.
MAZE = {'map': MAP, 'start': (0, 0), 'end': (9, 4)}

class Maze(cmd.Cmd):
    """
    A maze game. (cmd.Cmd)

    Class Attributes:
    directions: Abbreviations for movement directions. (dict of str: str)

    Attributes:
    current: The possible moves from the current location. (str)
    map: What directions you can move from each cell in the maze. (list of list)
    start: The starting coordinates of the player. (tuple of int)
    x: The x coordinate of the current location. (int)
    y: The y location of the current coordinate. (int)

    Methods:
    do_east: Move to the east. (bool)
    do_north: Move to the north. (bool)
    do_south: Move to the couth. (bool)
    do_west: Move to the west. (bool)
    move: Move in the maze. (bool)
    ow: Bump into a wall. (None)
    show_directions: Show the ways the player can move. (None)

    Overridden Methods:
    preloop
    """

    directions = {'e': 'east', 'n': 'north', 's': 'south', 'w': 'west'}

    def do_east(self, arg):
        """Move to the east. Add an integer argument to move multiple times."""
        return self.move('e', 1, 0, arg)

    def do_north(self, arg):
        """Move to the north. Add an integer argument to move multiple times."""
        return self.move('n', 0, -1, arg)

    def do_south(self, arg):
        """Move to the south. Add an integer argument to move multiple times."""
        return self.move('s', 0, 1, arg)

    def do_west(self, arg):
        """Move to the west. Add an integer argument to move multiple times."""
        return self.move('w', -1, 0, arg)

    def move(self, check, delta_x, delta_y, arg):
        """
        Move in the maze. (bool)

        Parameters:
        check: The character for checking for valid directions. (str)
        delta_x: How much to move on the x axis. (int)
        delta_y: How much to move on the y axis. (int)
        arg: The arguments passed with the movement command. (str)
        """
        # Check for moving multiple times.
        if arg.isdigit():
            times = int(arg)
        else:
            times = 1
        for movement in range(times):
            # Check for a valid move
            if check not in self.current:
                self.ow()
                break
            # Update the player's postion.
            self.x += delta_x
            self.y += delta_y
            self.current = self.map[self.y][self.x]
            print('moving...')
            # Check for solving the maze.
            if (self.x, self.y) == self.end:
                print('You made it out of the maze!')
                return True
        # Show the next location if not solved.
        self.show_directions()

    def ow(self):
        """Bump into a wall. (None)"""
        print('Ow! You bump into a wall.')

    def preloop(self):
        """Prep for the command loop. (None)"""
        # Extract the maze data.
        self.map = MAZE['map']
        self.x = MAZE['start'][0]
        self.y = MAZE['start'][1]
        self.end = MAZE['end']
        # Set the starting location for validity checks.
        self.current = self.map[self.y][self.x]
        # Print an introduction.
        print('You are in a maze.')
        print('You have a torch, but it barely lights past the end of your hand.')
        # Show the current location.
        self.show_directions()

    def show_directions(self):
        """Show the ways the player can move. (None)"""
        # Get the valid moves.
        direction_words = [self.directions[direction] for direction in self.current]
        # Select message based on number of valid moves.
        if len(self.current) == 1:
            message = 'You are in a dead end. You can only move to the {}.'
        elif len(self.current) == 2:
            message = 'You are in a hallway. You can move {} or {}.'
        elif len(self.current) == 3:
            message = 'You are at an intersection. You can move {}, {}, or {}.'
        elif len(self.current) == 4:
            message = 'You are in an open space. You can move {}, {}, {}, or {}'
        # Display the message.
        print(message.format(*direction_words))

if __name__ == '__main__':
    maze = Maze()
    maze.cmdloop()