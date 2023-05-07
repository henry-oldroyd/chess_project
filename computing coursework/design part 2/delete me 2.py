# this class is a variant of the game class that is to be used in a web game of chess
# it originally inherited from the game class but then it became to different so I no longer made it inherit from the game class

# from .game import Game

from assorted import safe_hash
from chess_functions import Board_State, Vector
from move_engine import Move_Engine_Timed
from schemas import serialize_piece, serialize_move


# import other modules
from chess_functions import Board_State, Vector
from move_engine import Move_Engine_Timed
from assorted import NotUserTurn, NotComputerTurn, InvalidMove, safe_hash

from time import perf_counter
import os


# # this function clears the console
# def clear_console():
#     #  https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
#     os.system('cls')


# # this function allows for a functions performance to be measured
# def time_function(function):
#     start = perf_counter()
#     result = function()
#     end = perf_counter()
#     time_delta = end - start
#     return result, time_delta


# the game class is used to keep track of a chess game between a user and the computer
class Game_Website(object):

    # constructor for game object
    # def __init__(self, time, user_color="W", echo=True) -> None:
    def __init__(self, difficulty="medium", user_color="W") -> None:
        self.difficulty = difficulty.strip().lower()

        # based on user's color, determine color key
        self.player_color_key = {
            "W": 1 if user_color == "W" else -1,
            "B": -1 if user_color == "W" else 1
        }
        # set depth property from parameters

        # set attributes for game at start
        # start with a blank board
        self.board_state = Board_State()
        self.move_counter = 0
        # use the timed move engine to find moves
        self.move_engine = Move_Engine_Timed()
        self.move_history_output = []

    # the time function is treated as a property to emulate how it was before when it was a property (before difficulty)
    def get_time(self) -> int:
        pass
    

    # this functions adds a move to the move history,
    # it doesn't make the move

    def add_move_to_history(self, move: list[Vector, Vector]):
        pass 
    # this function makes a move on the board state and logs this in the game history
    def make_move(self, move: list[Vector, Vector]):
        pass

    def implement_user_move(self, move: list[Vector]) -> None:
        pass
    # this function determines if the game is over and if so, what is the nature of the outcome
    def check_game_over(self) -> list[bool, str, str]:
        pass
    # this function is used to determine the AI's move
    # the time delta can be explicitly given or it can use the time provided manually as a parameter
    def best_move_function(self, time: int) -> list[int, list[Vector, Vector]]:
        pass
    # this function is used to generate a description of the move that the computer has completed for the client side GUI
    # it is needed to provide highlighting ect.
    # it doesn't make the computer move
    def generate_computer_move_description(self, move, previous_board_state) -> dict[str: Vector, str: Piece]:
        pass
    # this function completed the computer's move in a given time delta and returns a description
    def implement_computer_move_and_report(self, time=None) -> dict[str: Vector, str: Piece]:
        pass