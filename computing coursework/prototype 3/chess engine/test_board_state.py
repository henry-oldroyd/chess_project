import unittest
import ddt

from board_state import Board_State
# tested so assumed correct
import pieces
from vector import Vector

def test_dir(file_name): return f"test_data/board_state/{file_name}.yaml"

# code used to deserialize 
# code repeated from test pieces, opportunity to reduce redundancy
def list_map(function, iterable): return list(map(function, iterable))
def tuple_map(function, iterable): return tuple(map(function, iterable))

def descriptor_to_piece(descriptor) -> pieces.Piece:
    # converts WN to knight object with a color attribute of white
    if descriptor is None:
        return None

    color, symbol = descriptor
    piece_type: pieces.Piece = pieces.PIECE_TYPES[symbol]
    return piece_type(color=color)

def deserialize_pieces_matrix(pieces_matrix, next_to_go="W") -> Board_State:
    def row_of_symbols_to_pieces(row):
        return tuple_map(descriptor_to_piece, row)

    # update pieces_matrix replacing piece descriptors to piece objects
    pieces_matrix = tuple_map(row_of_symbols_to_pieces, pieces_matrix)
    board_state: Board_State = Board_State(pieces_matrix=pieces_matrix, next_to_go=next_to_go)

    return board_state



@ddt.ddt
class Test_Case(unittest.TestCase):
    
    # this test isn't data driven, 
    # it tests that the static evaluation is 0 for starting positions
    def test_static_eval_starting_positions(self):
        self.assertEqual(
            Board_State().static_evaluation(),
            0
        )
    
    # this test is testing that a list of all pieces and there position vectors can be generated
    @ddt.file_data(test_dir('generate_all_pieces'))
    def test_generate_all_pieces(self, pieces_matrix, pieces_and_squares):
        pieces_and_squares = tuple_map(tuple, pieces_and_squares)
        
        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix)
        # use set as order irrelevant
        all_pieces: set[pieces.Piece, Vector] = set(board_state.generate_all_pieces())


        # convert square to vector, allowed as this is tested
        def deserialize(data_unit):
            # unpack test data unit
            descriptor, square = data_unit
            # return [descriptor_to_piece(descriptor), Vector.construct_from_square(square)]
            return (descriptor_to_piece(descriptor), Vector.construct_from_square(square))
        
        def serialize(data_unit):
            piece, vector = data_unit
            # return [piece.symbol(), vector.to_square()]
            return (piece.symbol(), vector.to_square())
        
        
        all_pieces_expected: set[pieces.Piece, Vector] = set(map(deserialize, pieces_and_squares))
        # legal_moves_expected: list[pieces.Piece, Vector] = sorted(
        #     map(deserialize, pieces_and_squares),
        #     key=repr
        # )
        
        self.assertEqual(
            all_pieces,
            all_pieces_expected,
            msg=f"\nactual {list_map(serialize, all_pieces)}  !=  expected {list_map(serialize, all_pieces_expected)}"
        )
    
    # this test is to test the function responsible for getting the piece at a given position vector
    @ddt.file_data(test_dir('piece_at_vector'))
    def test_piece_at_vector(self, pieces_matrix, vectors_and_expected_piece):
        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix)
        
        # could use all method and one assert but this would have been less readable, also hard to make useful message,
        # wanting different messages implies multiple asserts should be completed
        for vector, expected_piece in vectors_and_expected_piece:
            # deserialize vector / cast to Vector
            vector: Vector = Vector(*vector)
            # repeat for piece
            expected_piece: pieces.Piece = descriptor_to_piece(expected_piece)
            
            # actual
            piece: piece.Piece = board_state.get_piece_at_vector(vector)
            msg = f"Piece at vector {repr(vector)} is {repr(piece)} not expected piece {repr(expected_piece)}"

    # this test ensures that all the pieces belonging to a specific color and there position vectors can be identified
    @ddt.file_data(test_dir('generate_pieces_of_color'))
    def test_generate_pieces_of_color(self, pieces_matrix, color, pieces_and_squares):
        pieces_and_squares = tuple_map(tuple, pieces_and_squares)

        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix)
        # use set as order irrelevant
        legal_moves_actual: set[pieces.Piece, Vector] = set(board_state.generate_pieces_of_color(color))

        # convert square to vector, allowed as this is tested
        def deserialize(data_unit):
            # unpack test data unit
            descriptor, square = data_unit
            # return [descriptor_to_piece(descriptor), Vector.construct_from_square(square)]
            return (descriptor_to_piece(descriptor), Vector.construct_from_square(square))
        
        def serialize(data_unit):
            piece, vector = data_unit
            # return [piece.symbol(), vector.to_square()]
            return (piece.symbol(), vector.to_square())
        
        
        legal_moves_expected: set[pieces.Piece, Vector] = set(map(deserialize, pieces_and_squares))

        self.assertEqual(
            legal_moves_actual,
            legal_moves_expected,
            msg=f"\nactual {list_map(serialize, legal_moves_actual)}  !=  expected {list_map(serialize, legal_moves_expected)}"
        )
    
    # this test ensures that the chess engine can determine if a specified player is currently in check
    @ddt.file_data(test_dir('color_in_check'))
    def test_color_in_check(self, pieces_matrix, white_in_check, black_in_check):
        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix)
        
        self.assertEqual(
            board_state.color_in_check("W"), 
            white_in_check,
            msg=f"white {'should' if white_in_check else 'should not'} be in check but {'is' if board_state.color_in_check('W') else 'is not'}"
        )
        self.assertEqual(
            board_state.color_in_check("B"), 
            black_in_check,
            msg=f"black {'should' if black_in_check else 'should not'} be in check but {'is' if board_state.color_in_check('B') else 'is not'}"
        )

    # this test ensures that a game over situation can be identified and its nature discerned 
    @ddt.file_data(test_dir("game_over"))
    def test_game_over(self, pieces_matrix, expected_over, expected_outcome, next_to_go):
        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix, next_to_go=next_to_go)

        self.assertEqual(
            board_state.is_game_over_for_next_to_go(),
            (expected_over, expected_outcome),
            msg=f"\nactual {board_state.is_game_over_for_next_to_go()} != expected {(expected_over, expected_outcome)}"
        )

    # this is one of the most important functions to test
    # this function determines all the possible legal moves a player can make with their pieces, accounting for check
    # this test checks this for many inputs
    @ddt.file_data(test_dir("generate_legal_moves"))
    def test_generate_legal_moves(self, pieces_matrix, next_to_go, expected_legal_moves):
        board_state: Board_State = deserialize_pieces_matrix(pieces_matrix=pieces_matrix, next_to_go=next_to_go)
        actual_legal_moves = set(board_state.generate_legal_moves())
        
        # convert square to vector, allowed as this is tested
        def deserialize_expected_legal_moves():
            # unpack test data unit
            for test_datum in expected_legal_moves:
                from_square, all_to_squares = test_datum
                for to_square in all_to_squares:
                    position_vector: Vector = Vector.construct_from_square(from_square)
                    movement_vector: Vector = Vector.construct_from_square(to_square) - position_vector
                    
                    yield (position_vector, movement_vector)
        
        expected_legal_moves = set(deserialize_expected_legal_moves())
        self.assertEqual(
            actual_legal_moves,
            expected_legal_moves,
        )

if __name__ == '__main__':
    unittest.main()
    
