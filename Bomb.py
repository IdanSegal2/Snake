from game_parameters import *

class Bomb:

    def __init__(self):
        # returns from game_parameters random data for bomb
        # (x,y,radius,time) Random location, bomb radius and time to explode
        parameters = get_random_bomb_data()
        # x parameter of bomb location
        self.x = parameters[0]
        # y parameter of bomb location
        self.y = parameters[1]
        # radius parameter of bomb explosion
        self.radius = parameters[2]
        # time parameter of how long from bomb appearance on board until it explodes
        self.time = parameters[3]
        # counter that indicates if bomb has exploded or not
        self.time_counter = 0
        # radius of explosion that grows with every turn
        self.current_radius = -1
        # False until time_counter >= time
        self.exploded = False

    def get_time(self):
        """
        :return: time parameter of how long from bomb appearance on board until it explodes
        """
        return self.time

    def get_radius(self):
        """
        :return: radius parameter of bomb explosion
        """
        return self.radius

    def get_bomb_coords(self):
        """
        :return: tuple of coordinates of bomb location in the form of (x, y)
        """
        return self.x, self.y

    def update_bomb(self):
        """
        Calculates if bomb should explode, adds time to counter with every turn
        :return: bool if current_radius <= radius parameter.
        If True, new bomb is added, if False continues to grow current bomb
        """
        # checks if time_counter has surpassed the time indicator for the bomb to explode
        if self.time_counter >= self.time:
            # if bomb should explode, changes self.exploded status to True
            self.exploded = True
            # updates and grows current radius to portray on board by 1
            self.current_radius += 1
        # every turn the time_counter grows by 1
        self.time_counter += 1
        return self.current_radius <= self.radius