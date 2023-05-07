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
    # # it keeps track of:
    # # the player's color's
    # player_color_key: dict
    # # the difficulty or depth of the game
    # depth: int
    # # the current board state
    # board_state: Board_State
    # # the number of moves so far
    # move_counter: int

    # move_engine: Move_Engine

    # game_history_output: tuple[str]

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
    @property
    def time(self):
        match self.difficulty:
            case "really_easy": return 1
            case "easy": return 2
            case "medium": return 5
            case "hard": return 10
            case "really_hard": return 15
            case "extreme": return 30
            case "legendary": return 60
        raise ValueError(f"Difficulty {self.difficulty} not recognised")


    # this functions adds a move to the move history, 
    # it doesn't make the move 
    def add_move_to_history(self, move):
        # should be called pre move
        # color_moving = "White" if self.board_state.next_to_go == "W" else "Black"
        # print({"move": move})

        # unpack move and determine squares and relevant pieces
        position_vector: Vector = move[0]
        resultant_vector: Vector = move[0] + move[1]
        moving_piece, taken_piece = self.board_state.get_piece_at_vector(position_vector), self.board_state.get_piece_at_vector(resultant_vector)
        from_square, to_square = position_vector.to_square(), resultant_vector.to_square()

        # increment move count
        self.move_counter += 1

        # generate string move description using this data
        if taken_piece is None:
            # move_description = f"Move {self.move_counter}: {color_moving} moved {moving_piece} from {from_square} to {to_square}"
            # move_description = f"{self.move_counter}: {color_moving} moved {moving_piece} from {from_square} to {to_square}"
            move_description = f"{self.move_counter}: {moving_piece} from {from_square} to {to_square}"
        else:
            # move_description = f"Move {self.move_counter}: {color_moving} moved {moving_piece} from {from_square} to {to_square}, taking piece {taken_piece}"
            # move_description = f"{self.move_counter}: {color_moving} moved {moving_piece} from {from_square} to {to_square}, taking piece {taken_piece}"
            move_description = f"{self.move_counter}: {moving_piece} from {from_square} to {to_square}, taking piece {taken_piece}"

        # append this string to the move history list
        self.move_history_output.append(move_description)

    
    # this function makes a move on the board state and logs this in the game history
    def make_move(self, move):
        assert not self.board_state.is_game_over_for_next_to_go()[0], "Cannot make move if game is over"
        assert move is not None, "Cannot move as move parameter not valid"

        self.add_move_to_history(move)

        # adjust properties that keep track of the game state
        self.board_state = self.board_state.make_move(*move)
        



    # this function validates if the user's move is allowed and if so, makes it
    # input form javascript is a move in terms of vectors
    def implement_user_move(self, move: list[Vector]) -> None:
        assert not self.board_state.is_game_over_for_next_to_go()[0], "Cannot make move if game is over"
        
        # check that the user is allowed to move
        which_player_next_to_go = self.player_color_key.get(
            self.board_state.next_to_go
        )
        # check it is the user's go
        if which_player_next_to_go != 1:
            raise NotUserTurn(game=self)

        # if the move is not in the set of legal moves, raise and appropriate exception
        if move not in self.board_state.generate_legal_moves():
            self.board_state.print_board()
            print(f"Move  {move} not in legal moves")
            raise InvalidMove(game=self)

        # make the move
        self.make_move(move)

        # no return data needed
        # return move, self.board_state.static_evaluation()


    # this function determines if the game is over and if so, what is the nature of the outcome
    def check_game_over(self):
        # returns: over: bool, winning_player: (W / B), classification: str

        # determine if board state is over for next player
        over, winner = self.board_state.is_game_over_for_next_to_go()
        # switch case statement to determine the appropriate values to be returned in each case
        match (over, winner):
            case False, _:
                victory_classification = None
                winning_player = None
            case True, None:
                if self.board_state.is_3_board_repeats_in_game_history():
                    victory_classification = "stalemate board repeat"
                else:
                    victory_classification = "stalemate no legal moves"
                winning_player = None
            case True, winner:
                victory_classification = "checkmate"
                winning_player = self.player_color_key[winner]

        # return appropriate values
        return over, winning_player, victory_classification

    # this function is used to determine the AI's move
    # the time delta can be explicitly given or it can use the time provided manually as a parameter
    def best_move_function(self, time):
        if time is None:
            time = self.time

        # returns just the move 
        return self.move_engine(
            board_state=self.board_state,
            # depth is based of difficulty of game based on depth parameter
            time=time,
        )[1]

    # this function is used to generate a description of the move that the computer has completed for the client side GUI
    # it is needed to provide highlighting ect.
    # it doesn't make the computer move
    def generate_computer_move_description(self, move, previous_board_state):
        
        # determine various qualities about the move
        position_vector, movement_vector = move
        resultant_vector = position_vector + movement_vector

        moved_piece = previous_board_state.get_piece_at_vector(position_vector)
        taken_piece = previous_board_state.get_piece_at_vector(resultant_vector)

        from_square = position_vector.to_square()
        to_square = resultant_vector.to_square()

        # return dictionary of this data ready for json serialization 
        # to do this, ensure all objects such as pieces and vectors are serialized. 
        move_description = {
            "moved_piece": serialize_piece(moved_piece),
            "taken_piece": serialize_piece(taken_piece),
            "from_square": from_square,
            "to_square": to_square,
            "move": serialize_move(move)
        }

        return move_description


    # this function completed the computer's move in a given time delta and returns a description
    def implement_computer_move_and_report(self, time=None):
        previous_board_state = self.board_state

        # get next to go player (1/-1)
        which_player_next_to_go = self.player_color_key.get(
            self.board_state.next_to_go
        )
        # check that is it the computer's turn
        if which_player_next_to_go != -1:
            raise NotComputerTurn()
            # raise ValueError(f"Next to go is user: {self.board_state.next_to_go} not computer")

        # get the computer's move
        best_move = self.best_move_function(time=time)


        # defensive design to detect issues, ensure a move has been calculated
        assert best_move is not None

        # implement the move and return a description
        self.make_move(best_move)

        return self.generate_computer_move_description(best_move, previous_board_state)



    def __eq__(self, other: object) -> bool:
        # this method used the hash function to determine if 2 of these objects are the same
        if not isinstance(other, Game_Website):
            return False

        return hash(self) == hash(other)

    def __hash__(self):
        # this function encodes all the data that makes a game unique in a hash to be stored in a database
        return hash(safe_hash((
            "Game_Website",
            self.player_color_key,
            self.time,
            self.board_state,
            self.move_counter,
            # self.move_engine,
            self.move_history_output,
            self.difficulty
        )))






# class Game_With_Difficulty(Game):
#     def __init__(self, difficulty="medium", user_color="W") -> None:
#         self.difficulty = difficulty.strip().lower()

#         # based on user's color, determine color key
#         self.player_color_key = {
#             "W": 1 if user_color == "W" else -1,
#             "B": -1 if user_color == "W" else 1
#         }
#         # set depth property from parameters
#         self.echo = False

#         # set attributes for game at start
#         self.board_state = Board_State()
#         self.move_counter = 0
#         self.move_engine = Move_Engine_Timed()
#         self.game_history_output = ()



    
#     @property
#     def time(self):
#         # return 0.5
#         match self.difficulty:
#             case "really easy": return 1
#             case "easy": return 2
#             case "medium": return 6
#             case "hard": return 10
#             case "really hard": return 15

#     def implement_user_move(self, position_vector: Vector, movement_vector: Vector) -> None:
#         resultant_vector: Vector = position_vector + movement_vector
#         from_square, to_square = position_vector.to_square(), resultant_vector.to_square()
        
#         return super().implement_user_move(from_square, to_square, time_delta=None, estimated_utility=None)
    
#     def implement_computer_move(self):
#         previous_board_state: Board_State = self.board_state
#         move, _ = super().implement_computer_move(best_move_function=None)
#         position_vector, movement_vector = move
#         resultant_vector = position_vector + movement_vector

#         moved_piece = previous_board_state.get_piece_at_vector(position_vector)
#         taken_piece = previous_board_state.get_piece_at_vector(resultant_vector)

#         from_square = position_vector.to_square()
#         to_square = resultant_vector.to_square()

#         move_description = {
#             "moved_piece": serialize_piece(moved_piece),
#             "taken_piece": serialize_piece(taken_piece),
#             "from_square": from_square,
#             "to_square": to_square,
#             "move": serialize_move(move)   
#         }

#         return move_description

#     def __hash__(self):
#         return safe_hash((
#             self.player_color_key,
#             self.time,
#             self.echo,
#             self.board_state,
#             self.move_counter,
#             self.move_engine,
#             self.game_history_output,
#             self.difficulty
#         ))
