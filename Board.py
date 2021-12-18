import Snake, Apple, Bomb
import game_parameters
from game_display import *
import math

class Board:
    def __init__(self):
        """This function initializes the board"""
        # board: list of lists representing the x,y cells of the
        # board. outer list is the x axis. inner lists are the y axis.
        # left and bottom-most cell is (0,0).
        self.board = [[None for _ in range(game_parameters.HEIGHT)]
                      for _ in range(game_parameters.WIDTH)]
        # growing_turns_left: how many turns the snake has left to grow due
        # to eating apple(s)
        self.growing_turns_left = 0
        # snake: object of the class Snake that the player controls
        self.snake = Snake.Snake()
        # keep a deep copy of the old snake to compare moves later
        self.prev_snake = Snake.Snake()
        self.add_snake_to_board()
        # bomb object of the class Bomb
        self.bomb = Bomb.Bomb()
        # Adds new bomb to game
        self.add_bomb = Bomb.new_bomb
        # max_time: time that current bomb explodes
        self.max_time = self.bomb.get_time()
        # time_left: the time of current bomb explosion reached
        self.current_time = 0
        # max_radius: max radius of the last bomb added to he board
        self.max_radius = self.bomb.get_radius()
        # current_radius: the radius current explosion reached
        self.current_radius = 1
        # apple object of the class Apple
        self.apple = Apple.Apple()
        # Adds a new apple to the game
        self.add_apple = self.apple.new_apple
        # Apples: list of apples on board, each apple appears as dictionary
        # in the form {(x, y) : score}
        self.apples_on_board = []
        # Game score
        self.total_score = 0

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
            self.total_score += self.apples_on_board.get((head_x, head_y))
            self.apples_on_board.remove((head_x, head_y))
            self.add_apple_to_board()
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

    def add_bomb_to_board(self):
        x, y = self.bomb.get_bomb_coords()
        #TODO- this should end the game
        if not self.check_for_space():
            return
        if not self.board[x][y]:
            #TODO- remove current bomb and add random new bomb
        else:
            self.board[x][y] = 'bomb'


    def add_apple_to_board(self):
        while self.board.count('apple') < 3:
            # TODO- this should end the game
            if not self.check_for_space():
                return
            x, y, score = self.add_apple
            if not self.board[x][y]:
                continue
            else:
                self.board[x][y] = 'apple'
                self.apples_on_board.append({(x, y) : score})


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


    def check_2_activate_bomb(self):
        if self.current_time >= self.max_time:
            self.explosion_expansion()
        else:
            self.current_time += 1


    def explosion_expansion(self):
        if self.time_left <= 0:
            if self.current_radius > self.max_radius:
                #TODO- remove current bomb and add random new bomb
                self.current_radius = 1
            else:
                radius = self.current_radius
                x, y = self.bomb.get_bomb_coords
                self.__explosion_helper(self, radius, x, y)
                self.board[x][y] = None
                self.current_radius += 1


    def __explosion_helper(self, radius, x, y):
        explosion_coords = []
        for i in range(radius + 1):
            for j in range(radius + 1):
                if x + i + y + j == radius:
                    if 0 < (x - i) < game_parameters.WIDTH and 0 < (y - j) < game_parameters.HEIGHT:
                        explosion_coords.append((x - i, y - j))
                    if 0 < (x - j) < game_parameters.WIDTH and 0 < (y - i) < game_parameters.HEIGHT:
                        explosion_coords.append((x - j, y - i))
                if (x + i) < game_parameters.WIDTH and (y + j) < game_parameters.HEIGHT:
                    if math.fabs(x - i) + math.fabs(y - j) == radius:
                        explosion_coords.append((x + i, y + j))
                if (x + j) < game_parameters.WIDTH and (y + i) < game_parameters.HEIGHT:
                    if math.fabs(x - j) + math.fabs(y - i) == radius:
                        explosion_coords.append((x + j, y + i))
        if len(explosion_coords) < math.pow(2, radius + 1):
            if radius != self.max_radius:
                #TODO- remove this bomb and generate a new one
        for coords in explosion_coords:
            x, y = coords
            if self.board[x][y] == 'snake':
                #TODO- end game
            elif self.board[x][y] == 'apple':
                #TODO- remove apple and make new apple
                self.board[x][y] == 'explosion'
            else:
                self.board[x][y] == 'explosion'