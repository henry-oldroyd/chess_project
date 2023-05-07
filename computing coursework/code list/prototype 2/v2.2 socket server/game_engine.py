from copy import deepcopy
from dataclasses import dataclass
from hashlib import new
from itertools import product

from function_lib import Vector


@dataclass
class Board_State():
    # due to the unicode characters for pieces not being on my keyboard I will use None, BP and WP to represent squares
    pieces_matrix: tuple[tuple[str]]
    # next_to_go: str
    # next to go is -1 for computer of 1 for user
    next_to_go: int


    def execute_move(self, from_sq: Vector, to_sq: Vector):
        new_pieces_matrix = deepcopy(self.pieces_matrix)
        # convert to list
        new_pieces_matrix = list(map(list, new_pieces_matrix))
        
        # set from to blank
        row, col = 7-from_sq.j, from_sq.i
        current_piece = new_pieces_matrix[row][col]
        
        owner = current_piece[0]
        assert owner == {-1: 'C', 1: 'U'}[self.next_to_go]
        
        new_pieces_matrix[row][col] = None
        
        # set to square to this piece
        row, col = 7-to_sq.j, to_sq.i
        new_pieces_matrix[row][col] = current_piece
        
        # convert back to tuple
        new_pieces_matrix = tuple(map(tuple, new_pieces_matrix))
        # new_next_to_go = "U" if self.next_to_go == "C" else "C"
        new_next_to_go = -1 * self.next_to_go
        return Board_State(
            pieces_matrix=new_pieces_matrix,
            next_to_go=new_next_to_go
        )

    def piece_at_vector(self, vector: Vector):
        column, row = vector.i, 7-vector.j
        # column, row = vector.i, vector.j
        return self.pieces_matrix[row][column]
    
    def pawn_position_vector_generator(self):
        for i, j in product(range(8), range(8)):
            position_vector = Vector(i, j)
            # if self.piece_at_vector(position_vector) == "AP":
            if self.piece_at_vector(position_vector) == self.next_to_go:
                yield position_vector
    
    def legal_moves_generator(self):
        for pawn_position_vector in self.pawn_position_vector_generator():
            movement_vectors = tuple(get_pawn_movement_vectors(pawn_position_vector, self))
            # print(f"get_pawn_movement_vectors({pawn_position_vector}, self)   ->   {movement_vectors}")
            # if not None or empty
            if movement_vectors:
                yield from movement_vectors

    def static_eval(self) -> float:
        pass
    
    def minimax_best_move(self):
        pass
    
    def outcome_if_over(self):
        pass


def get_pawn_movement_vectors(position_vector, board_state: Board_State):
    # computer pawns at the top of the board move down not up
    # multiplier = 1 if board_state.next_to_go == 'U' else -1
    multiplier = -1 * board_state.next_to_go
    # enemy_piece = 'CP' if board.next_to_go == 'U'
    enemy_piece = {-1: 'CP', 1: 'UP'}[-1*board_state.next_to_go]

    foreword_v = position_vector + (Vector(0, 1)*multiplier)
    if foreword_v.position_vector_in_board():
        # square = board_state.pieces_matrix[foreword_v.i][foreword_v.j]
        square = board_state.piece_at_vector(foreword_v)
        if square is None:
            yield (position_vector, foreword_v)
    
    diagonal_takes = (
        position_vector + (Vector(-1, 1)*multiplier),
        position_vector + (Vector(1, 1)*multiplier),
    )
    
    for diagonal_take in diagonal_takes:
        if diagonal_take.position_vector_in_board():
            square = board_state.piece_at_vector(diagonal_take)
            # if square == "PP":
            if square == enemy_piece:
                yield (position_vector, diagonal_take)

def main(board_state: list[list[str]]) -> list:
    """This function will take the current board state as a parameter
    Its output mirror the API diagram
    move, new board state matrix, array of legal moves and outcome, is game over
    I am yet to decide if I will return all of this in one object"""
    
    board_state: Board_State = Board_State(board_state)
    
    best_move = board_state.minimax_best_move()
    new_board_state: Board_State = board_state.execute_move(best_move)
    
    over, outcome = new_board_state.outcome_if_over()
    legal_moves = new_board_state.legal_moves_enumerator()
    legal_moves_and_outcome = legal_moves.map(
        lambda move: (move, new_board_state.execute_move(move).outcome_if_over())
    )
    
    return (
        best_move, new_board_state, (over, outcome), tuple(legal_moves_and_outcome)
    )