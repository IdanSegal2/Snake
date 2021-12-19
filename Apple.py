from game_parameters import *

class Apple:

    def __init__(self):
        # (x,y,score) - Random location on the board and initial score
        apple_parameters = get_random_apple_data()
        # Unpacking apple_parameters tuple into coordinates and score
        self.x, self.y, self.score = apple_parameters

    def get_apple_coord(self):
        """
        :return: tuple of apple coordinates (x, y)
        """
        return self.x, self.y

    def get_apple_score(self):
        """
        :return: int of random score given to certain apple
        """
        return self.score