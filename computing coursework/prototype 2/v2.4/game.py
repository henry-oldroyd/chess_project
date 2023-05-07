# import other modules
from board_state import Board_State
from minimax import minimax
from vector import Vector
from assorted import ARBITRARILY_LARGE_VALUE, dev_print, NotUserTurn, InvalidMove

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
    # a table of game state hashes and there frequency
    piece_matrix_occurrence_hash_table: list

    # this adds a new game state to the frequency table 
    def add_new_piece_matrix_to_hash_table(self, piece_matrix):
        # the pieces matrix is hashed
        matrix_hash = hash(piece_matrix)

        # if this pieces matrix has been encountered before, add 1 to the frequency
        if matrix_hash in self.piece_matrix_occurrence_hash_table.keys():
            self.piece_matrix_occurrence_hash_table[matrix_hash] += 1
        # else set frequency to 1
        else:
            self.piece_matrix_occurrence_hash_table[matrix_hash] = 1

    # determines if there is a 3 repeat stalemate  
    def is_3_board_repeats_in_game_history(self):
        # if any of the board states have been repeated 3 or more times: stalemate
        return any(value >= 3 for value in self.piece_matrix_occurrence_hash_table.values())

    # constructor for game object
    def __init__(self, depth=2, user_color="W") -> None:
        # based on user's color, determine color key
        self.player_color_key = {
            "W": 1 if user_color=="W" else -1,
            "B": -1 if user_color=="W" else 1
        }
        # set depth property from parameters
        self.depth = depth

        # set attributes for game at start
        self.board_state = Board_State()
        self.move_counter = 0
        self.piece_matrix_occurrence_hash_table = {}

    # this function validates if the user's move is allowed and if so, makes it
    def implement_user_move(self, from_square, to_square) -> None:
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

        # if the move is not in the set of legal moves, raise and appropriate exception
        if (position_vector, movement_vector) not in self.board_state.generate_legal_moves():
            raise InvalidMove(game=self)
        
        # implement move 
        self.board_state = self.board_state.make_move(from_position_vector=position_vector, movement_vector=movement_vector)
        # adjust other properties that keep track of the game
        self.move_counter += 1
        self.add_new_piece_matrix_to_hash_table(self.board_state.pieces_matrix)

        return (position_vector, movement_vector), self.board_state.static_evaluation()

    # this function determines if the game is over and if so, what is the nature of the outcome
    def check_game_over(self):
        # returns: over: bool, winning_player: (1/-1), classification: str
        # check for 3 repeat stalemate
        if self.is_3_board_repeats_in_game_history():
            return True, None, "Stalemate"
        
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
            score, best_child, best_move = minimax(
                board_state = self.board_state,
                # assume white / user always maximizer
                # is_maximizer = (self.board_state.next_to_go == "W"),
                is_maximizer = False,
                # depth is based of difficulty of game based on depth parameter
                depth = self.depth,
                # default values for alpha and beta
                alpha = (-1)*ARBITRARILY_LARGE_VALUE,
                beta = ARBITRARILY_LARGE_VALUE
            )
        else:
            # otherwise use provided function,
            # the provided function should take game as an argument and then return data in the same format as the minimax function
            score, best_child, best_move = best_move_function(self)

        # adjust properties that keep track of the game state
        self.board_state = best_child
        self.move_counter += 1
        self.add_new_piece_matrix_to_hash_table(self.board_state.pieces_matrix)

        # incase is it wanted for a print out ect, return move and score
        return best_move, score
