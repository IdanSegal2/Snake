import Snake
import game_parameters
from game_display import *


class Board:
    def __init__(self):
        """This function initializes the board"""
        # board: list of lists representing the x,y cells of the
        # board. outer list is the x axis. inner lists are the y axis.
        # left and bottom-most cell is (0,0).
        self.board = [[None for _ in range(game_parameters.HEIGHT)]
                      for _ in range(game_parameters.WIDTH)]
        # time_left: turns until bomb explodes
        self.time_left = 0
        # max_radius: max radius of the last bomb added tot he board
        self.max_radius = 0
        # current_radius: the radius current explosion reached
        self.current_radius = 0
        # growing_turns_left: how many turns the snake has left to grow due
        # to eating apple(s)
        self.growing_turns_left = 0
        # snake: object of the class Snake that the player controls
        self.snake = Snake.Snake()
        # keep a deep copy of the old snake to compare moves later
        self.prev_snake = Snake.Snake()
        self.add_snake_to_board()

    def check_for_space(self):
        """This function returns True if there's space left at the board
        for adding new objects"""

        # iterate over the board
        for x in range(len(self.board)):
            for content in self.board[x]:
                if content is not None:
                    # return True only if found an empty cell
                    return True
        return False

    def check_updated_snake(self):
        """This function checks that new snake following this turn's move
        is within board, didn't hit himself/bomb and if it ate an apple
        Returns True if ok, False otherwise"""

        # calculate x and y of new head
        head_x = self.snake.get_coordinates()[0][0]
        head_y = self.snake.get_coordinates()[0][1]
        # keep the coordinates of the tail of the snake before the move
        prev_tail = self.prev_snake.get_coordinates()[-1]

        # check if new head is where tail was before move & tail's leaving
        if self.growing_turns_left == 0 and prev_tail[0] == head_x \
                and prev_tail[1] == head_y:
            return True

        # if head is out of board return False
        elif head_x < 0 or head_x >= len(self.board) or head_y < 0 \
                or head_y >= len(self.board[0]):
            return False

        # if there's an apple on the new cell, add growing turns
        elif self.board[head_x][head_y] == 'apple':
            self.growing_turns_left += 3
            return True

        # if there's a bomb or another part of the snake, return False
        elif self.board[head_x][head_y] is not None:
            return False

        # if succeeded, set prev snake to current one and return true
        self.prev_snake = self.snake
        return True

    def get_board(self):
        """Returns list of lists which represents the board"""
        return self.board

    def add_snake_to_board(self, growing=False):
        """This function adds all of the snakes coordinate to the board"""
        for coordinate in self.snake.get_coordinates():
            x = coordinate[0]
            y = coordinate[1]
            self.board[x][y] = 'snake'
        if not growing:
            old_tail = self.prev_snake.get_coordinates()[-1]
            self.board[old_tail[0]][old_tail[1]] = None

    def update_board(self, key_clicked=None):
        """This function updates the board with new objects.
        :return True if succeeded and False otherwise."""
        # on first use, add snake to board
        # check if snake should grow from eating apples recently
        growing = self.growing_turns_left > 0
        self.snake.move(key_clicked, growing)
        if growing:
            # decrease by 1 the turns it has left to grow
            self.growing_turns_left -= 1
        # check if the updated snake kept the game's rules. (or if he
        # ate an apple)
        if self.check_updated_snake():
            self.add_snake_to_board(growing)
        # otherwise player lost. return False
        else:
            return False
        # action succeeded. return True.
        return True
