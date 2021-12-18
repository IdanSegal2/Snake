class Snake:

    def __init__(self):
        """This function initializes the snake"""
        # body: list of tuples with the coordinate of the
        # snake's head at cell 0, up to its 'tail' at cell len-1.
        self.__body = [(10, 10), (10, 9), (10, 8)]
        # direction: the last move order the snake was given
        # can be either "up", "down", "right or "left.".
        self.__direction = "Up"

    def get_direction(self):
        """This function returns a string with the snake's direction"""
        return self.__direction

    def get_coordinates(self):
        """This function returns a list of tuples with the snake's head
        at cell 0, up to its 'tail' at cell len-1."""
        return self.__body

    def __change_direction(self, direction, growing):
        """This function sets the snake to a new moving direction"""

        # keep the coordinates of the snake's current head
        head_x = self.__body[0][0]
        head_y = self.__body[0][1]

        # add a new head (index 0) coordinate to the snake that corresponds
        # to the move direction
        if direction == "Up":
            self.__insert_new_head(head_x, head_y+1)
        if direction == "Down":
            self.__insert_new_head(head_x, head_y-1)
        if direction == "Right":
            self.__insert_new_head(head_x+1, head_y)
        if direction == "Left":
            self.__insert_new_head(head_x-1, head_y)

        # if the snake is not in a growing phase from eating:
        if not growing:
            # remove last coordinate of the snake (because size did no change)
            self.__body.pop()
        # update the snake's direction property
        self.__direction = direction

    def __insert_new_head(self, head_x, head_y):
        """add a new cell at index 0 with an updated
        head coordinate corresponding to the new direction."""
        # create a new coordinate
        new = (head_x, head_y)
        # add it to the head (index 0) of the snake's body
        self.__body.insert(0, new)

    def move(self, direction, growing):
        """This function changes snakes direction when it is necessary
        and possible"""

        # check if direction was given
        given = direction is not None

        # check direction is not the opposite of current direction (legal)
        legal = True
        if direction == 'Up':
            legal = self.__direction != 'Down'
        elif direction == 'Down':
            legal = self.__direction != 'Up'
        elif direction == 'Right':
            legal = self.__direction != 'Left'
        elif direction == 'Left':
            legal = self.__direction != 'Right'

        # if direction was given and is legal change the snake's direction.
        if given and legal:
            self.__change_direction(direction, growing)
        # otherwise, move in current direction
        else:
            direction = self.__direction
            self.__change_direction(direction, growing)

