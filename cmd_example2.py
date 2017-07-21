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
HELP_TEXT: The text to display for general help. (str)
MAP: What directions you can move from each cell in the maze. (list of list)
MAZE: The details of the maze to solve. (dict)

Classes:
Maze: A maze game. (cmd.Cmd)
"""

import cmd
import random

# The text to display for general help.
HELP_TEXT = """This is a maze game. The only info you get is what directions you can move from
where you are. You may move by typing in any of the four cardinal compass
points: north, south, east, or west. You may abbreviate any of these
commands by just using the first letter: n, s, e, or w."""

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
    map: What directions you can move from each cell in the maze. (list of list)
    start: The starting coordinates of the player. (tuple)

    Methods:
    do_east: Move to the east. (bool)
    do_north: Move to the north. (bool)
    do_quit: Give up and quit. (bool)
    do_south: Move to the couth. (bool)
    do_west: Move to the west. (bool)
    move: Move in the maze. (bool)
    ow: Bump into a wall. (None)
    show_directions: Show the ways the player can move. (None)

    Overridden Methods:
    do_help
    precmd
    preloop
    """

    directions = {'e': 'east', 'n': 'north', 's': 'south', 'w': 'west'}
    intro = 'You are in a maze.\nYou have a torch, but it barely lights past the end of your hand.'
    prompt = 'In the maze: '

    def do_east(self, arg):
        """Move to the east. Add an integer argument to move multiple times."""
        return self.move('e', 1, 0, arg)

    def do_help(self, arg):
        """Get help on a command, or just help for general help."""
        if arg:
            super().do_help(arg)
        else:
            print(HELP_TEXT)

    def do_north(self, arg):
        """Move to the north. Add an integer argument to move multiple times."""
        return self.move('n', 0, -1, arg)

    def do_quit(self, arg):
        """Give up and quit."""
        return True

    def do_south(self, arg):
        """Move to the south. Add an integer argument to move multiple times."""
        return self.move('s', 0, 1, arg)

    def do_west(self, arg):
        """Move to the west. Add an integer argument to move multiple times."""
        return self.move('w', -1, 0, arg)

    def do_xyzzy(self, arg):
        if random.random() < 0.23:
            self.x = random.randrange(len(self.map[0]))
            self.y = random.randrange(len(self.map))
            print('Poof! You have been teleported!')
        else:
            print('Nothing happens.')

    def move(self, check, delta_x, delta_y):
        """
        Move in the maze. (bool)

        The return value is the stop flag for the do_direction method that called this
        method.

        Parameters:
        check: The character for checking for valid directions. (str)
        delta_x: How much to move on the x axis. (int)
        delta_y: How much to move on the y axis. (int)
        """
        # Check for a valid move.
        if check not in self.current:
            return self.ow()
        # Update the current location.
        self.x += delta_x
        self.y += delta_y
        self.current = self.map[self.y][self.x]

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

    def ow(self):
        """ Bump into a wall. (None) """
        print('Ow! You bump into a wall.')

    def precmd(self, line):
        """
        Pre-command handling. (str)

        Parameters:
        line: The orignal user command input. (str)
        """
        # Replace alases with commands.
        cmd, space, arg = line.partition(' ')
        cmd = self.directions.get(cmd, cmd)
        return '{} {}'.format(cmd, arg)

    def preloop(self):
        """ Prep for the command loop. (None)"""
        # Extract the information from the MAZE global.
        self.map = MAZE['map']
        self.x = MAZE['start'][0]
        self.y = MAZE['start'][1]
        self.end = MAZE['end']
        # Get the moves for the start position
        self.current = self.map[self.y][self.x]
        self.intro = '{}\n{}'.format(self.intro, self.show_directions())

    def postcmd(self, stop, line):
        """
        Post-command handling. (bool)

        Parameters:
        stop: A flag for stopping command processing. (bool)
        line: The user command input. (str)
        """
        # Check for a solution.
        if (self.x, self.y) == self.end:
            print('You made it out of the maze!')
            stop = True
        elif not stop:
            print(self.show_directions())
        return stop

    def show_directions(self):
        """Show the ways the player can move. (str)"""
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
        # Return the message.
        return message.format(*direction_words)

if __name__ == '__main__':
    maze = Maze()
    maze.cmdloop()