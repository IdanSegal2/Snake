import Snake, Apple, Bomb
from game_display import *
import copy


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
        self.add_snake_to_board(True)
        # bomb object of the class Bomb
        self.add_bomb_to_board()
        # # list of all the apples on the board
        self.apples_on_board = []
        # Apples: ensure valid list of apples
        self.maintain_apples()
        # Game score
        self.total_score = 0
        # explosion coordinates on the board
        self.explosion_coordinates = []
        # coordinate of where the snake landed on explosion
        self.snake_exploded = []
        # bool if snake hit border of board
        self.snake_hit_border = False

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
        growing = self.growing_turns_left > 0

        # check if new head is where tail was before move & tail's leaving
        if self.growing_turns_left == 0 and prev_tail[0] == head_x \
                and prev_tail[1] == head_y:
            return True

        # if head is out of board return False after adding it to board
        elif head_x < 0 or head_x >= len(self.board) or head_y < 0 \
                or head_y >= len(self.board[0]):
            self.add_snake_to_board(growing)
            return False

        # if there's an apple on the new cell, add growing turns
        # Also replaces apple, if no space left to put apple return False
        elif self.board[head_x][head_y] == 'apple':
            self.growing_turns_left += 3
            return self.replace_apple(head_x, head_y)

        # if there's part of the snake, paint snake and return False
        elif self.board[head_x][head_y] == 'snake':
            if not growing:
                self.add_snake_to_board(growing)
            self.snake_hit_border = True
            return False

        # If snake moved to a coordinate where there is an explosion, return False
        elif not self.is_explosion_on_snake():
            return False

        # if succeeded return true
        return True

    def replace_apple(self, x, y):
        """
        Replaces apple if ate by snake or burned by explosion
        :param x: x coordinate of head of snake or explosion
        :param y: y coordinate of head of snake or explosion
        :return: True if apple was replaced,
        False if there was no place on board to replace apple
        """
        # iterates over all the apples currently on the board
        for apple in self.apples_on_board:
            # gets apple on boards coordinates
            x_apple, y_apple = apple.get_apple_coord()
            # if apple and snake or explosion coordinates are the same
            if x == x_apple and y == y_apple:
                # gets apple's score
                score = apple.get_apple_score()
                # adds apple's score to total game score
                self.total_score += score
                # removes certain apple from the board
                self.apples_on_board.remove(apple)
        # generates new random apple and checks if space available
        return self.maintain_apples()

    def get_board(self):
        """Returns list of lists which represents the board"""
        return self.board

    def add_snake_to_board(self, growing=False):
        """This function adds all of the snakes coordinate to the board"""
        for coordinate in self.prev_snake.get_coordinates():
            x = coordinate[0]
            y = coordinate[1]
            # if coordinate within snake boundaries
            if (len(self.board) > x >= 0) and (len(self.board[0]) > y >= 0):
                self.board[x][y] = None
        for coordinate in self.snake.get_coordinates():
            x = coordinate[0]
            y = coordinate[1]
            # if coordinate within snake boundaries
            if (len(self.board) > x >= 0) and (len(self.board[0]) > y >= 0):
                self.board[x][y] = 'snake'

    def add_bomb_to_board(self):
        """
        adds bomb to board at the beginning of the game
        and after every explosion
        :return: True if bomb added, False if no space on board to add bomb
        """
        # checks if there is available space to add bomb to board
        if not self.check_for_space():
            return False
        # returns True when bomb is placed on board
        while True:
            self.bomb = Bomb.Bomb()
            x, y = self.bomb.get_bomb_coords()
            if self.board[x][y] is not None:
                continue
            else:
                self.board[x][y] = 'bomb'
                return True

    def maintain_apples(self):
        """
        places apple on board and makes sure there is always three on the board at a time
        :return: True if there are 3 apples on the board, False otherwise
        """
        while len(self.apples_on_board) < 3:
            # checks for available space on board
            if not self.check_for_space():
                return False
            # generates random apple
            apple = Apple.Apple()
            x, y = apple.get_apple_coord()
            score = apple.get_apple_score()
            # checks that apple was not generated on snake or bomb
            if self.board[x][y] is not None:
                continue
            else:
                # adds apple to board and places in apples_on_board list
                self.board[x][y] = 'apple'
                self.apples_on_board.append(apple)
        return True

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
        # update_bomb returns False if finished explosion, then creates a new bomb
        if not self.bomb.update_bomb():
            self.erase_explosion()
            self.add_bomb_to_board()
        # Checks what stage bomb explosion is at, True if bomb is exploding
        if self.bomb.exploded:
            # If explosion_expansion returns False, adds new bomb to board
            if not self.explosion_expansion(self.bomb):
                self.erase_explosion()
                self.add_bomb_to_board()
            # checks if apple was burned by explosion
            # if burned, removes burned apple and adds new apple
            for apple in self.apples_on_board:
                x, y = apple.get_apple_coord()
                if self.board[x][y] == 'explosion':
                    self.apples_on_board.remove(apple)
                    self.maintain_apples()
        # check if the updated snake kept the game's rules. (or if he
        # ate an apple)
        # otherwise player lost. return False
        if self.check_updated_snake():
            self.add_snake_to_board(growing)
        else:
            # checks if snake hit the border of the board
            if self.snake_hit_border:
                return False
            # checks if explosion landed on snake
            if not self.is_explosion_on_snake():
                self.add_snake_to_board(growing)
                self.board[self.snake_exploded[0][0]][self.snake_exploded[0][1]] = 'explosion'
                return False
            return False
        # action succeeded. return True and update prev snake.
        self.prev_snake = copy.deepcopy(self.snake)
        return True

    def explosion_expansion(self, exploding_bomb):
        """
        :param exploding_bomb: bomb's class with all the values
        :return: True if explosion didn't hit border, False otherwise
        """
        r = exploding_bomb.current_radius
        x, y = exploding_bomb.get_bomb_coords()
        return self.__explosion_helper(r - 1, x, y)

    def __explosion_helper(self, radius, x, y):
        """
        :param radius: int of current explosion radius
        :param x: int representing the bomb's original location for x coordinate
        :param y: int representing the bomb's original location for y coordinate
        :return: False if bomb can't make move, True otherwise
        """
        # erases previous explosion coordinates
        self.erase_explosion()
        for i in range(radius + 1):
            for j in range(radius + 1):
                # checks if coordinates are the size of the radius
                if i + j == radius:
                    if 0 <= (x + i) < game_parameters.WIDTH and 0 <= (y - j) < game_parameters.HEIGHT:
                        self.board[x + i][y - j] = 'explosion'
                        self.explosion_coordinates.append((x + i, y - j))
                    else:
                        return False
                    if 0 <= (x - i) < game_parameters.WIDTH and 0 <= (y - j) < game_parameters.HEIGHT:
                        self.board[x - i][y - j] = 'explosion'
                        self.explosion_coordinates.append((x - i, y - j))
                    else:
                        return False
                    if (x + i) < game_parameters.WIDTH and (y + j) < game_parameters.HEIGHT:
                        self.board[x + i][y + j] = 'explosion'
                        self.explosion_coordinates.append((x + i, y + j))
                    else:
                        return False
                    if (x - i) < game_parameters.WIDTH and (y + j) < game_parameters.HEIGHT:
                        self.board[x - i][y + j] = 'explosion'
                        self.explosion_coordinates.append((x - i, y + j))
                    else:
                        return False
        # returns True if all coordinates are legal to place
        return True

    def erase_explosion(self):
        """ erases places where explosion appeared in the last turn """
        for coord in self.explosion_coordinates:
            x, y = coord
            self.board[x][y] = None
        self.explosion_coordinates = []

    def is_explosion_on_snake(self):
        """
        Checks if snake moved to a coordinate where an explosion is happening
        :return: True if snake didn't land on explosion, False otherwise
        """
        for coord in self.snake.get_coordinates():
            x, y = coord
            if self.board[x][y] == 'explosion':
                self.snake_exploded.append((x, y))
                return False
        return True