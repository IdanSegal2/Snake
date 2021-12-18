from game_parameters import *

class Apple:

    def __init__(self):
        # (x,y,score) - Random location on the board and initial score
        apple_parameters = get_random_apple_data()
        self.x, self.y, self.score = apple_parameters


    def get_apple_coord(self):
        return self.x, self.y

    def get_apple_score(self):
        return self.score