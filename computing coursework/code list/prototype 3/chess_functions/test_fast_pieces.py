import unittest
import ddt

from . import pieces
# as vector is already tested we can use it here and assume it won't cause any logic errors
from .vector import Vector

def test_dir(file_name): return f"test_data/pieces/{file_name}.yaml"

EMPTY_PIECES_MATRIX = ((None,)*8,)*8

@ddt.ddt
class Test_Case(unittest.TestCase):

    # this test is based on testing the the movement vectors of a piece places at some position in an empty board are as expected
    @ddt.file_data(test_dir('test_empty_board'))
    def test_empty_board(self, piece_type, square, expected_move_squares):
        # deserialize
        position_vector = Vector.construct_from_square(square)
        piece: pieces.Piece = pieces.PIECE_TYPES[piece_type]('W')
        movement_vectors = piece.generate_movement_vectors(pieces_matrix=EMPTY_PIECES_MATRIX, position_vector=position_vector)
        resultant_squares = list(
            map(
                lambda movement_vector: (movement_vector+position_vector).to_square(),
                movement_vectors
            )
        ) 
        # assert as expected
        # can use sets to prevent order being an issue as vectors are hashable
        self.assertEqual(
            set(resultant_squares),
            set(expected_move_squares),
            msg=f"\n\nactual movement squares {sorted(resultant_squares)}  !=  expected movement squares {sorted(expected_move_squares)}\n{repr(piece)} at {square}"
        )


    # this test assert that that a pieces movement vectors are as expected when the piece is surrounded by other pieces
    @ddt.file_data(test_dir('test_board_populated'))
    def test_board_populated(self, pieces_matrix, square, expected_piece_symbol, expected_move_squares):
        # deserialize
        def list_map(function, iterable): return list(map(function, iterable))
        def tuple_map(function, iterable): return tuple(map(function, iterable))
        
        def descriptor_to_piece(descriptor) -> pieces.Piece:
            # converts WN to knight object with a color attribute of white
            if descriptor is None: 
                return None

            color, symbol  = descriptor
            piece_type: pieces.Piece = pieces.PIECE_TYPES[symbol]
            return piece_type(color=color)
        
        def row_of_symbols_to_pieces(row): return tuple_map(descriptor_to_piece, row)
        
        # update pieces_matrix replacing piece descriptors to piece objects
        pieces_matrix = tuple_map(row_of_symbols_to_pieces, pieces_matrix)

        position_vector = Vector.construct_from_square(square)
        row, column = 7-position_vector.j, position_vector.i
        
        # assert piece as expected
        piece: pieces.Piece = pieces_matrix[row][column]
        self.assertEqual(
            piece.symbol(),
            expected_piece_symbol,
            msg=f"\nPiece at square {square} was not the expected piece"
        )
    
        # assert movement vectors as expected
        movement_vectors = piece.generate_movement_vectors(pieces_matrix=pieces_matrix, position_vector=position_vector)
        resultant_squares = list(
            map(
                lambda movement_vector: (movement_vector+position_vector).to_square(),
                movement_vectors
            )
        )
        self.assertEqual(
            set(resultant_squares),
            set(expected_move_squares),
                msg=f"\n\nactual movement squares {sorted(resultant_squares)}  !=  expected movement squares {sorted(expected_move_squares)}\n{repr(piece)} at {square}"
        )

if __name__ == '__main__':
    unittest.main()
