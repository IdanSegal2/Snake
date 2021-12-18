from game_parameters import *

class Apple:

    def __init__(self):
        # (x,y,score) - Random location on the board and initial score
        self.new_apple = get_random_apple_data()


    def get_apple_coord(self):
        return self.add_apple[0], self.add_apple[1]