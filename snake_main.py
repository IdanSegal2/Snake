import game_parameters
from Board import *
from game_display import GameDisplay


def main_loop(gd: GameDisplay) -> None:
    """This is the main loop running the game"""
    gd.show_score(0)
    # create the game board
    board = Board()
    # "action_ok" will be True if user actions are in agreement with the
    # game rules (borders, away from bomb etc.) and False otherwise
    action_ok = True
    # end round after setup
    draw_graphics(board.get_board(), gd, board.total_score)
    gd.end_round()
    # loop while user actions ok and there's enough space to add objects
    while board.check_for_space() and action_ok:
        # get user click or None if there wasn't
        key_clicked = gd.get_key_clicked()
        # update board according to click if action was ok (or change
        # action ok to False and exit loop at the end of the round)
        action_ok = board.update_board(key_clicked)
        # draw the graphics according to board state this turn
        draw_graphics(board.get_board(), gd, board.total_score)
        gd.end_round()


def draw_graphics(board, gd, score):
    """This function draws thee game display's board according to internal
    board's properties"""
    # iterate over all cells in internal board
    for x in range(game_parameters.WIDTH):
        for y in range(game_parameters.HEIGHT):
            # whenever encountering a known object, draw its color.
            if board[x][y] == 'snake':
                gd.draw_cell(x, y, 'black')
            elif board[x][y] == 'apple':
                gd.draw_cell(x, y, 'green')
            elif board[x][y] == 'bomb':
                gd.draw_cell(x, y, 'red')
            elif board[x][y] == 'explosion':
                gd.draw_cell(x, y, 'orange')
    gd.show_score(score)
