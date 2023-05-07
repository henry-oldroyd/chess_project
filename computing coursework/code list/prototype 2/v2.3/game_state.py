from copy import deepcopy
from dataclasses import dataclass
from itertools import product as iter_product
from pprint import pprint
from turtle import position

import pieces as pieces_mod
from assorted_functions import Vector, ARBITRARILY_LARGE_VALUE

STARTING_POSITIONS: tuple[tuple[pieces_mod.Piece]] = (
    (
        pieces_mod.Castle(color="B", owner=-1),
        pieces_mod.Knight(color="B", owner=-1),
        pieces_mod.Bishop(color="B", owner=-1),
        pieces_mod.Queen(color="B", owner=-1),
        pieces_mod.King(color="B", owner=-1),
        pieces_mod.Bishop(color="B", owner=-1),
        pieces_mod.Knight(color="B", owner=-1),
        pieces_mod.Castle(color="B", owner=-1)
    ),
    (pieces_mod.Pawn(color="B", owner=-1),)*8,
    (None,)*8,
    (None,)*8,
    (None,)*8,
    (None,)*8,
    (pieces_mod.Pawn(color="W", owner=1),)*8,
    (
        pieces_mod.Castle(color="W", owner=1),
        pieces_mod.Knight(color="W", owner=1),
        pieces_mod.Bishop(color="W", owner=1),
        pieces_mod.Queen(color="W", owner=1),
        pieces_mod.King(color="W", owner=1),
        pieces_mod.Bishop(color="W", owner=1),
        pieces_mod.Knight(color="W", owner=1),
        pieces_mod.Castle(color="W", owner=1)
    )
)

@dataclass(frozen=True)
class Board_State():
    # 1 or -1
    next_to_go: int = 1
    pieces_matrix: tuple[tuple[pieces_mod.Piece]] = STARTING_POSITIONS

    def print_board(self):
        pprint(
            list(map(
                lambda row: list(map(
                    lambda piece: None if piece is None else piece.symbol,
                    row
                )),
                self.pieces_matrix
            ))
        )

    def get_piece_at_vector(self, vector: Vector):
        column, row = vector.i, 7-vector.j
        # column, row = vector.i, vector.j
        return self.pieces_matrix[row][column]

    def generate_pieces_of_owner(self, owner=None):
        if owner is None:
            owner = self.next_to_go

        for i, j in iter_product(range(8), range(8)):
            piece_position_vector = Vector(i, j)
            piece: pieces_mod.Piece = self.get_piece_at_vector(piece_position_vector)
            if not piece:
                continue
            if piece.owner != owner:
                continue
            yield piece, piece_position_vector

    def player_in_check(self, player=None):
        if player is None:
            player = self.next_to_go
            
        # it is now A's turn
        player_a = player
        player_b = (-1) * player
        
        # we will examine all the movement vectors of B's pieces 
        # if any of them could take the A's King then currently A is in check as their king is threatened by 1 or more pieces (which could take it next turn)
        for piece, position_v in self.generate_pieces_of_owner(player_b):
            movement_vs = piece.generate_movement_vectors(
                pieces_matrix=self.pieces_matrix,
                position_vector=position_v
            )
            for movement_v in movement_vs:
                resultant = position_v + movement_v
                to_square = self.get_piece_at_vector(resultant)
                As_move_threatens_king_A = isinstance(to_square, pieces_mod.King) and to_square.owner == player_a
                # if As_move_threatens_king_A break out of all 3 loops
                if As_move_threatens_king_A: return True
        return False

    def generate_legal_moves(self):
        for piece, piece_position_vector in self.generate_pieces_of_owner(owner=self.next_to_go):
            movement_vectors = piece.generate_movement_vectors(
                pieces_matrix=self.pieces_matrix,
                position_vector=piece_position_vector
            )
            for movement_vector in movement_vectors:
                child_game_state = self.make_move(from_position_vector=piece_position_vector, movement_vector=movement_vector)
                is_check_for_a = child_game_state.player_in_check(self.next_to_go)
                if not is_check_for_a:
                    yield piece_position_vector, movement_vector

    def is_game_over_for_next_to_go(self):
        # check if in checkmate
        # for player a
        # if b has no moves
        if not list(self.generate_legal_moves()):
            # if b in check
            if self.player_in_check():
                # checkmate for b, a wins
                return True, self.next_to_go
            else:
                # stalemate
                return True, 0

        return False, None

    def static_evaluation(self):
        def generate_all_pieces():
            for i, j in iter_product(range(8), range(8)):
                piece_position_vector = Vector(i, j)
                piece: pieces_mod.Piece = self.get_piece_at_vector(piece_position_vector)
                if not piece:
                    continue

                yield piece, piece_position_vector
    
        over, winner = self.is_game_over_for_next_to_go()
        if over:
            return winner * ARBITRARILY_LARGE_VALUE
        else:
            return sum(piece.get_value(position_vector) * piece.owner for piece, position_vector in generate_all_pieces())

    def make_move(self, from_position_vector: Vector, movement_vector: Vector):
        to_position_vector = from_position_vector + movement_vector
        # poor code, this below line can cause infinite recursion when legal moves generator called post check changes
        # assert (from_position_vector, movement_vector) in self.generate_legal_moves()

        new_pieces_matrix = deepcopy(self.pieces_matrix)
        # convert to list
        new_pieces_matrix = list(map(list, new_pieces_matrix))

        # set from to blank
        row, col = 7-from_position_vector.j, from_position_vector.i
        piece: pieces_mod.Piece = new_pieces_matrix[row][col]

        piece.last_move = movement_vector

        new_pieces_matrix[row][col] = None

        # set to square to this piece
        row, col = 7-to_position_vector.j, to_position_vector.i
        new_pieces_matrix[row][col] = piece

        # convert back to tuple
        new_pieces_matrix = tuple(map(tuple, new_pieces_matrix))

        return Board_State(
            next_to_go=self.next_to_go * (-1),
            pieces_matrix=new_pieces_matrix
        )

