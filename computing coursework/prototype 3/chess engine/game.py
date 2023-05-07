# import other modules
from board_state import Board_State
from minimax import Move_Engine
from vector import Vector
from assorted import NotUserTurn, InvalidMove

from time import perf_counter
import os

def clear_console():
    #  https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
    os.system('cls')


def time_function(function):
    start = perf_counter()
    result = function()
    end = perf_counter()
    time_delta = end - start
    return result, time_delta



# the game class is used to keep track of a chess game between a user and the computer
class Game(object):
    # it keeps track of:
    # the player's color's
    player_color_key: dict
    # the difficulty or depth of the game
    depth: int
    # the current board state
    board_state: Board_State
    # the number of moves so far
    move_counter: int

    move_engine: Move_Engine

    game_history_output: tuple[str]

    # constructor for game object
    def __init__(self, depth=2, user_color="W", echo=True) -> None:
        # based on user's color, determine color key
        self.player_color_key = {
            "W": 1 if user_color=="W" else -1,
            "B": -1 if user_color=="W" else 1
        }
        # set depth property from parameters
        self.depth = depth
        self.echo = True

        # set attributes for game at start
        self.board_state = Board_State()
        self.move_counter = 0
        self.move_engine = Move_Engine()
        self.game_history_output = ()

    @staticmethod
    def create_row(moving_player, time_delta, move_count, new_utility, future_utility, move_description, white_pieces_taken, black_pieces_taken, number_legal_moves):
        # print("(moving_player, time_delta, move_count, new_utility, future_utility, move_description, white_pieces_taken, black_pieces_taken, number_legal_moves)")
        # print((moving_player, time_delta, move_count, new_utility, future_utility, move_description, white_pieces_taken, black_pieces_taken, number_legal_moves))
        if time_delta is None: 
            time_delta = ""
        if future_utility is None:
            future_utility = ""
        return f"| {move_count:^14} | {moving_player:^15} | {new_utility:^15}  | {future_utility:^15}  | {time_delta:^15} | {number_legal_moves:^15} | {move_description:<40} | {white_pieces_taken:<35} | {black_pieces_taken:<35} |"

    def print_game_history(self):
        clear_console()
        # https://www.geeksforgeeks.org/string-alignment-in-python-f-string/
        print("Moves History:")
        print()
        # print(self.create_row('Moving Color', 'Move Count', 'Time Taken (sec)', 'New Utility', 'Move', 'White Pieces Taken', 'Black Pieces Taken'))
        print(
            self.create_row(
                moving_player="Moving Color",
                time_delta="Time Taken",
                new_utility="New Utility",
                future_utility="Future Utility",
                move_description="Move Description",
                white_pieces_taken="White Pieces Taken",
                black_pieces_taken="Black Pieces Taken",
                move_count="Move Number",
                number_legal_moves="NO legal moves"
            )
        )
        for item in self.game_history_output:
            print(item)
        print()
        self.board_state.print_board()


    def make_move(self, move, time_delta, future_utility):
        if self.echo:
            color_moving = "White (+)" if self.board_state.next_to_go == "W" else "Black (-)"
            position_vector: Vector = move[0]
            resultant_vector: Vector = move[0] + move[1]
            moving_piece, taken_piece = self.board_state.get_piece_at_vector(position_vector), self.board_state.get_piece_at_vector(resultant_vector)
            from_square, to_square = position_vector.to_square(), resultant_vector.to_square()
            no_legal_moves = self.board_state.number_legal_moves

        # adjust properties that keep track of the game state
        self.board_state = self.board_state.make_move(*move)
        print(f"self.board_state.next_to_go   -->   {self.board_state.next_to_go}")
        self.move_counter += 1
            
        if self.echo:
            utility_score = self.board_state.static_evaluation()
            move_number = self.move_counter

            if taken_piece is None:
                move_description = f"{moving_piece} moved from {from_square} to {to_square}"
            else:
                move_description = f"{moving_piece} moved from {from_square} to {to_square}, taking piece {taken_piece}"

            white_pieces_taken = " ".join(self.board_state.pieces_taken_by_color("W"))
            # white_pieces_taken = "(No pieces taken)" if white_pieces_taken == "" else white_pieces_taken
            black_pieces_taken = " ".join(self.board_state.pieces_taken_by_color("B"))
            # black_pieces_taken = "(No pieces taken)" if black_pieces_taken == "" else black_pieces_taken

            if time_delta is not None:
                time_delta = f"{round(time_delta, 2)} sec"
            # else:
            #     time_delta = ""

            new_row = self.create_row(
                moving_player=color_moving,
                time_delta=time_delta,
                move_count=move_number,
                new_utility=utility_score,
                move_description=move_description,
                white_pieces_taken=white_pieces_taken,
                black_pieces_taken=black_pieces_taken,
                number_legal_moves=no_legal_moves,
                future_utility=future_utility,
            )

            self.game_history_output = tuple(list(self.game_history_output) + [new_row])

            if self.board_state.color_in_check():
                check_msg = f"CHECK:  {self.board_state.next_to_go} in check"
                new_row = self.create_row(
                    moving_player="-",
                    time_delta="-",
                    move_count="-",
                    new_utility="-",
                    move_description=check_msg,
                    white_pieces_taken="-",
                    black_pieces_taken="-",
                    number_legal_moves="-",
                    future_utility="-",
                )
                self.game_history_output = tuple(list(self.game_history_output) + [new_row])


            over, winner = self.board_state.is_game_over_for_next_to_go()
            if over:
                how = "Stalemate" if winner is None else "Checkmate"
                winning_color = "White" if winner == "W" else "B"

                if how == "Stalemate":
                    if self.board_state.is_3_board_repeats_in_game_history():
                        game_over_msg = "Stalemate: both players draw (3 repeats of the board state)"
                    else:
                        game_over_msg = "Stalemate: both players draw (no legal moves and not in check)"
                else:
                    game_over_msg = f"Checkmate: {winning_color} wins"

                new_row = self.create_row(
                    moving_player="-",
                    time_delta="-",
                    move_count="-",
                    new_utility="-",
                    move_description=game_over_msg,
                    white_pieces_taken="-",
                    black_pieces_taken="-",
                    number_legal_moves="-",
                    future_utility="-",
                )
                self.game_history_output = tuple(list(self.game_history_output) + [new_row])


            self.print_game_history()

    # this function validates if the user's move is allowed and if so, makes it
    def implement_user_move(self, from_square, to_square, time_delta=None, estimated_utility=None) -> None:
        # check that the user is allowed to move
        which_player_next_to_go = self.player_color_key.get(
            self.board_state.next_to_go
        )
        if which_player_next_to_go != 1:
            raise NotUserTurn(game=self)
        
        # unpack move into vector form
        # invalid square syntaxes will cause a value error here
        try:
            position_vector = Vector.construct_from_square(from_square)
            movement_vector = Vector.construct_from_square(to_square) - position_vector
        except Exception:
            raise ValueError("Square's not in valid format")

        move = (position_vector, movement_vector)

        # if the move is not in the set of legal moves, raise and appropriate exception
        if move not in self.board_state.generate_legal_moves():
            raise InvalidMove(game=self)
        
        self.make_move(move, time_delta, estimated_utility)

        return move, self.board_state.static_evaluation()

    # this function determines if the game is over and if so, what is the nature of the outcome
    def check_game_over(self):
        # returns: over: bool, winning_player: (1/-1), classification: str
        
        # determine if board state is over for next player
        over, winner = self.board_state.is_game_over_for_next_to_go()
        # switch case statement to determine the appropriate values to be returned in each case
        match (over, winner):
            case False, _:
                victory_classification = None
                winning_player = None
            case True, None:
                victory_classification = "Stalemate"
                winning_player = None
            case True, winner:
                victory_classification = "Checkmate"
                winning_player = self.player_color_key[winner]
        # return appropriate values
        return over, winning_player, victory_classification
    
    # this function determines and implements the computer move
    def implement_computer_move(self, best_move_function=None):
        # for use with testing bots, a best move function can be provided for use, but minimax if the default

        # get next to go player (1/-1)
        which_player_next_to_go = self.player_color_key.get(
            self.board_state.next_to_go
        )
        # check that is it the computer's turn
        if which_player_next_to_go != -1:
            raise ValueError(f"Next to go is user: {self.board_state.next_to_go} not computer")

        # if no function provided, default to minimax
        if best_move_function is None:
            def best_move_function(self):
                return self.move_engine(
                    board_state = self.board_state,
                    # depth is based of difficulty of game based on depth parameter
                    depth = self.depth,
                )

        # otherwise use provided function,
        # the provided function should take game as an argument and then return data in the same format as the minimax function
        result, time_delta = time_function(
            lambda: best_move_function(self)
        )
        score, best_move = result
    
        assert best_move is not None

        self.make_move(best_move, time_delta, score)

        # incase is it wanted for a print out ect, return move and score
        return best_move, score
