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
        self.add_snake_to_board()
        # bomb object of the class Bomb
        self.add_bomb_to_board()
        # # list of all the apples on the board
        self.apples_on_board = []
        # Apples: ensure valid list of apples
        self.maintain_apples()
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
            return self.replace_apple(head_x, head_y)

        # if there's a bomb or another part of the snake, return False
        elif self.board[head_x][head_y] is not None:
            return False
        # if succeeded return true
        return True

    def replace_apple(self, x, y):
        for apple in self.apples_on_board:
            x_apple, y_apple = apple.get_apple_coord()
            if x == x_apple and y == y_apple:
                score = apple.get_apple_score()
                self.total_score += score
                self.apples_on_board.remove(apple)
        return self.maintain_apples()

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
        if not self.check_for_space():
            return False
        while True:
            self.bomb = Bomb.Bomb()
            x, y = self.bomb.get_bomb_coords()
            if self.board[x][y] is not None:
                continue
            else:
                self.board[x][y] = 'bomb'
                return True

    def maintain_apples(self):
        while len(self.apples_on_board) < 3:
            if not self.check_for_space():
                return False
            apple = Apple.Apple()
            x, y = apple.get_apple_coord()
            score = apple.get_apple_score()
            if self.board[x][y] is not None:
                continue
            else:
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
        if self.bomb.exploded:
            if not self.explosion_expansion(self.bomb):
                self.erase_explosion()
                self.add_bomb_to_board()
            for apple in self.apples_on_board:
                x, y = apple.get_apple_coord()
                if self.board[x][y] == 'explosion':
                    self.apples_on_board.remove(apple)
                    self.maintain_apples()
        # check if the updated snake kept the game's rules. (or if he
        # ate an apple)
        if self.check_updated_snake():
            self.add_snake_to_board(growing)
        # otherwise player lost. return False
        else:
            return False
        # action succeeded. return True and update prev snake.
        self.prev_snake = copy.deepcopy(self.snake)
        return True

    def explosion_expansion(self, exploding_bomb):
        r = exploding_bomb.current_radius
        x, y = exploding_bomb.get_bomb_coords()
        return self.__explosion_helper(r, x, y)

    def __explosion_helper(self, radius, x, y):
        self.erase_explosion()
        for i in range(radius + 1):
            for j in range(radius + 1):
                if i + j == radius:
                    if 0 <= (x + i) < game_parameters.WIDTH and 0 <= (y - j) < game_parameters.HEIGHT:
                        self.board[x + i][y - j] = 'explosion'
                    else:
                        return False
                    if 0 <= (x - i) < game_parameters.WIDTH and 0 <= (y - j) < game_parameters.HEIGHT:
                        self.board[x - i][y - j] = 'explosion'
                    else:
                        return False
                    if (x + i) < game_parameters.WIDTH and (y + j) < game_parameters.HEIGHT:
                        self.board[x + i][y + j] = 'explosion'
                    else:
                        return False
                    if (x - i) < game_parameters.WIDTH and (y + j) < game_parameters.HEIGHT:
                        self.board[x - i][y + j] = 'explosion'
                    else:
                        return False
        return True

    def erase_explosion(self):
        for i in range(game_parameters.WIDTH):
            for j in range(game_parameters.HEIGHT):
                if self.board[i][j] == 'explosion':
                    self.board[i][j] = None