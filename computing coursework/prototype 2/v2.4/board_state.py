from copy import deepcopy
from dataclasses import dataclass
from itertools import product as iter_product

import pieces as pieces_mod
from assorted import ARBITRARILY_LARGE_VALUE
from vector import Vector

# this is a pieces matrix for the starting position is chess
# white is at the bottom as it is from the user's perspective and I am currently assuming the user is white.
# I can change this in the frontend later
STARTING_POSITIONS: tuple[tuple[pieces_mod.Piece]] = (
    (
        pieces_mod.Rook(color="B"),
        pieces_mod.Knight(color="B"),
        pieces_mod.Bishop(color="B"),
        pieces_mod.Queen(color="B"),
        pieces_mod.King(color="B"),
        pieces_mod.Bishop(color="B"),
        pieces_mod.Knight(color="B"),
        pieces_mod.Rook(color="B")
    ),
    (pieces_mod.Pawn(color="B"),)*8,
    (None,)*8,
    (None,)*8,
    (None,)*8,
    (None,)*8,
    (pieces_mod.Pawn(color="W"),)*8,
    (
        pieces_mod.Rook(color="W"),
        pieces_mod.Knight(color="W"),
        pieces_mod.Bishop(color="W"),
        pieces_mod.Queen(color="W"),
        pieces_mod.King(color="W"),
        pieces_mod.Bishop(color="W"),
        pieces_mod.Knight(color="W"),
        pieces_mod.Rook(color="W")
    )
)

# frozen makes each instance of the board_state class is immutable
@dataclass(frozen=True)
class Board_State():
    next_to_go: str = "W"
    # the pieces matrix keeps track of the board positions and the pieces
    pieces_matrix: tuple[tuple[pieces_mod.Piece]] = STARTING_POSITIONS
    
    # this function outputs the board in a user friendly way
    # 8| BR  BN  BB  BQ  BK  BB  BN  BR
    # 7| ·   ·   BP  BP  BP  BP  BP  BP
    # 6| ·   ·   ·   ·   ·   ·   ·   ·
    # 5| BP  BP  ·   ·   ·   ·   ·   ·
    # 4| ·   ·   ·   WP  ·   WP  ·   ·
    # 3| ·   ·   ·   ·   ·   ·   ·   ·
    # 2| WP  WP  WP  ·   WP  ·   WP  WP
    # 1| WR  WN  WB  WQ  WK  WB  WN  WR
    #   (A   B   C   D   E   F   G   H )
    def print_board(self):
        # convert each piece to a symbol BP and replace none with dots
        # add numbers to left and add letters at the bottom
        numbers = range(8, 0, -1)
        letters = [chr(i) for i in range(ord("A"), ord("H")+1)]
        for row, number in zip(self.pieces_matrix, numbers):
            # clean up row of pieces
            symbols_row = map(lambda piece: piece.symbol() if piece else "· ", row)
            pretty_row = f"{number}| {'  '.join(symbols_row)}"
            print(pretty_row)
        print(f"  ({'   '.join(letters)} )")

    def get_piece_at_vector(self, vector: Vector):
        # this function exists as it is a really common operation. 
        # due to vector 0, 0 pointing the the bottom left not top left of the 2d array, 
        # some correction is needed 
        column, row = vector.i, 7-vector.j
        return self.pieces_matrix[row][column]

    # this function should yield all the pieces on the board
    def generate_all_pieces(self):
        # nested loop for i and j to iterate through all possible vectors
        for i, j in iter_product(range(8), range(8)):
            position_vector = Vector(i,j)
            # get the contents of the corresponding square
            piece = self.get_piece_at_vector(position_vector)
            
            # skip if none: skip if square empty
            if piece:
                yield piece, position_vector

    # this yields all pieces of a given color: 
    # used when examining legal moves of a given player
    def generate_pieces_of_color(self, color=None):
        # be default give pieces of player next to go
        if color is None:
            color = self.next_to_go

        # return all piece and position vector pairs
        # filtered by piece must match in color
        yield from filter(
            # lambda piece, _: piece.color == color,
            lambda piece_and_vector: piece_and_vector[0].color == color,
            self.generate_all_pieces()
        )

    # determines if a given player is in check based on the player's color
    def color_in_check(self, color=None):
        # default is to check if the player next to go is in check
        if color is None:
            color = self.next_to_go
            
        # let is now be A's turn
        # I use this player a and b model to keep track of the logic here
        color_a = color
        color_b = "W" if color == "B" else "B"
        
        # we will examine all the movement vectors of B's pieces 
        # if any of them could take the A's King then currently A is in check as their king is threatened by 1 or more pieces (which could take it next turn)
        # for each of b's pieces
        for piece, position_v in self.generate_pieces_of_color(color=color_b):
            movement_vs = piece.generate_movement_vectors(
                pieces_matrix=self.pieces_matrix,
                position_vector=position_v
            )
            # for each movement vector that the piece could make
            for movement_v in movement_vs:
                resultant = position_v + movement_v
                # check the contents of the square
                to_square = self.get_piece_at_vector(resultant)
                # As_move_threatens_king_A = isinstance(to_square, pieces_mod.King) and to_square.color == color_a
                # if the contents is A's king then the a is in check. 
                As_move_threatens_king_A = (to_square == pieces_mod.King(color=color_a))
                # if As_move_threatens_king_A then return true
                if As_move_threatens_king_A:
                    return True
        # if none of B's pieces were threatening to take A's king then A isn't in check
        return False

    # this function is a generator to be iterated through. 
    # it is responsible for yielding every possible move that a given player can make
    # yields this as a position and a movement vector 
    def generate_legal_moves(self):
        # iterate through all pieces belonging to player next to go
        for piece, piece_position_vector in self.generate_pieces_of_color(color=self.next_to_go):
            movement_vectors = piece.generate_movement_vectors(
                pieces_matrix=self.pieces_matrix,
                position_vector=piece_position_vector
            )
            # iterate through movement vectors of this piece
            for movement_vector in movement_vectors:
                # examine resulting child game state
                child_game_state = self.make_move(from_position_vector=piece_position_vector, movement_vector=movement_vector)
                # determine if current player next to go (different to next to go of child game state) is in check
                is_check_after_move = child_game_state.color_in_check(color=self.next_to_go)
                # only yield the move if it doesn't result in check
                if not is_check_after_move:
                    yield piece_position_vector, movement_vector
    
    # determines if the game is over
    # returns over, winner
    def is_game_over_for_next_to_go(self):
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        
        # in all cases, the game if over if a player has no legal moves left
        if not list(self.generate_legal_moves()):
            # if b in check
            if self.color_in_check():
                # checkmate for b, a wins
                winner = "W" if self.next_to_go == "B" else "B"
                return True, winner
            else:
                # stalemate
                return True, None
        # game not over
        return False, None

    # this function if responsible for generating a static evaluation for a given board-stat
    # it should be used by a maximiser or minimiser
    # starting position should have and evaluation of 0
    def static_evaluation(self):
        # if over give an appropriate score for win loss or draw
        over, winner = self.is_game_over_for_next_to_go()
        if over:
            match winner:
                case None: multiplier = 0
                case "W": multiplier = 1
                case "B": multiplier = -1
            # return winner * ARBITRARILY_LARGE_VALUE
            return multiplier * ARBITRARILY_LARGE_VALUE

        # this function takes a piece as an argument and uses its color to decide if its value should be positive or negative
        def get_piece_value(piece: pieces_mod.Piece, position_vector: Vector):
            # this function assumes white it maximizer and so white pieces have a positive score and black negative
            match piece.color:
                case "W": multiplier = 1
                case "B": multiplier = (-1)
            value = multiplier * piece.get_value(position_vector)
            # print(f"{piece.symbol()} at {position_vector.to_square} has value {value}")
            return value
        
        # for each piece, get the value (+/-)
        values = map(
            lambda x: get_piece_value(*x),
            self.generate_all_pieces()
        )
        # sum values for static eval
        return sum(values)


    def make_move(self, from_position_vector: Vector, movement_vector: Vector):
        resultant_vector = from_position_vector + movement_vector

        # make a coppy of the position vector, deep coppy is used to ensure no parts are shared be reference 
        new_pieces_matrix = deepcopy(self.pieces_matrix)

        # convert to list
        new_pieces_matrix = list(map(list, new_pieces_matrix))

        # look at square with position vector
        row, col = 7-from_position_vector.j, from_position_vector.i
        # get piece thats moving
        piece: pieces_mod.Piece = new_pieces_matrix[row][col]
        # set from square to blank
        new_pieces_matrix[row][col] = None

        # update piece to keep track of its last move
        piece.last_move = movement_vector


        # set to square to this piece
        row, col = 7-resultant_vector.j, resultant_vector.i
        new_pieces_matrix[row][col] = piece

        # convert back to tuple
        new_pieces_matrix = tuple(map(tuple, new_pieces_matrix))
        
        # update next to go
        new_next_to_go = "W" if self.next_to_go == "B" else "B"

        # return new board state instance 
        return Board_State(
            next_to_go=new_next_to_go,
            pieces_matrix=new_pieces_matrix
        )

