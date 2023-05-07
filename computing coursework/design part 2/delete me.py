
# the game class is used to keep track of a chess game between a user and the computer
class Game(object):
    # constructor for game object
    def __init__(self, time=10, user_color="W", echo=False) -> None:
        # based on user's color, determine color key
        self.player_color_key = {
            "W": 1 if user_color == "W" else -1,
            "B": -1 if user_color == "W" else 1
        }
        # set depth property from parameters
        self.time = time
        self.echo = echo

        # set attributes for game at start
        self.board_state = Board_State()
        self.move_counter = 0
        self.move_engine = Move_Engine_Timed()
        self.game_history_output = ()

    def create_row(moving_player, time_delta, move_count, new_utility, future_utility, move_description, white_pieces_taken, black_pieces_taken, number_legal_moves) -> str:
        pass
    def print_game_history(self):
        pass

    def make_move(self, move, time_delta, future_utility):
        pass
    def implement_user_move(self, from_square, to_square, time_delta=None, estimated_utility=None) -> None:
        pass

    def check_game_over(self) -> list[bool, str, str]:
        pass
    def implement_computer_move(self, best_move_function=None):
        pass
