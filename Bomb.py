from game_parameters import *

class Bomb:

    def __init__(self):
        self.new_bomb = get_random_bomb_data()
        self.current_bomb = []


    def current_bomb(self):
        return self.current_bomb.append(self.new_bomb)

    def __check_bomb(self):
        if self.current_bomb() == []:
            return current_bomb(self)

    def get_time(self):
        return self.current_bomb([0][3])

    def get_radius(self):
        return self.current_bomb([0][2])

    def __get_bomb_coords(self):
        return self.current_bomb([0][0]), self.current_bomb([0][1])