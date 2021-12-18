from game_parameters import *

class Bomb:

    def __init__(self):
        parameters = get_random_bomb_data()
        self.x = parameters[0]
        self.y = parameters[1]
        self.radius = parameters[2]
        self.time = parameters[3]
        self.time_counter = 0
        self.current_radius = -1
        self.exploded = False

    def get_time(self):
        return self.time

    def get_radius(self):
        return self.radius

    def get_bomb_coords(self):
        return self.x, self.y

    def update_bomb(self):
        if self.time_counter >= self.time:
            self.exploded = True
            self.current_radius += 1
        self.time_counter += 1
        return self.current_radius <= self.radius