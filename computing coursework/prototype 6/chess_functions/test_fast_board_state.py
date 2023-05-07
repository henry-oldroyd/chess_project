import unittest
import ddt
from random import randint
import json

from .board_state import Board_State, random_board_state
from .pieces import Pawn
# tested so assumed correct
from . import pieces
from .vector import Vector

from schemas import deserialize_pieces_matrix as deserialize_client_pieces_matrix

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

    def test_for_specific_issue(self):
        # print("\nRunning test test_for_specific_issue")
        board_state = Board_State()

        piece: Pawn = board_state.get_piece_at_vector(Vector(1, 1))
        self.assertTrue(
            piece.last_move is None,
            f"Piece hasn't been moved yet so last_move property should be None\nInstead it is {piece.last_move}"    
        )

        board_state = board_state.make_move(Vector(0, 1), Vector(0, 2))
        board_state = board_state.make_move(Vector(0, 6), Vector(0, -2))

        piece: Pawn = board_state.get_piece_at_vector(Vector(1, 1))
        self.assertTrue(
            piece.last_move is None,
            f"Piece hasn't been moved yet so last_move property should be None\nInstead it is {piece.last_move}"    
        )


        movement_vectors = list(piece.generate_movement_vectors(
            position_vector=Vector(1, 1),
            pieces_matrix=board_state.pieces_matrix,    
        ))
        # movement_vectors = sorted(movement_vectors, key=repr)

        # print("\n")
        # board_state.print_board()
        # print("\n")


        # print({"movement_vectors": movement_vectors})
        self.assertTrue(
            Vector(0, 1) in movement_vectors and Vector(0, 2) in movement_vectors,
            "Piece should be able to move foreword by either 1 or 2 squares"
        )

        actual_legal_moves = list(board_state.generate_legal_moves())
        actual_legal_moves = list(map(list, actual_legal_moves))

        self.assertTrue(
            [Vector(1, 1), Vector(0, 2)] in actual_legal_moves
        )

        # expected_legal_moves = [
        #     [Vector(1, 1), Vector(0, 2)],    
        #     [Vector(2, 1), Vector(0, 2)],    
        #     [Vector(3, 1), Vector(0, 2)],    
        #     [Vector(4, 1), Vector(0, 2)],    
        #     [Vector(5, 1), Vector(0, 2)],    
        #     [Vector(6, 1), Vector(0, 2)],    
        #     [Vector(7, 1), Vector(0, 2)],    
        #     [Vector(1, 6), Vector(0, -2)],    
        #     [Vector(2, 6), Vector(0, -2)],    
        #     [Vector(3, 6), Vector(0, -2)],    
        #     [Vector(4, 6), Vector(0, -2)],    
        #     [Vector(5, 6), Vector(0, -2)],    
        #     [Vector(6, 6), Vector(0, -2)],    
        #     [Vector(7, 6), Vector(0, -2)],
        #     [Vector(1, 1), Vector(0, 1)],
        #     [Vector(2, 1), Vector(0, 1)],
        #     [Vector(3, 1), Vector(0, 1)],
        #     [Vector(4, 1), Vector(0, 1)],
        #     [Vector(5, 1), Vector(0, 1)],
        #     [Vector(6, 1), Vector(0, 1)],
        #     [Vector(7, 1), Vector(0, 1)],
        #     [Vector(1, 6), Vector(0, -1)],
        #     [Vector(2, 6), Vector(0, -1)],
        #     [Vector(3, 6), Vector(0, -1)],
        #     [Vector(4, 6), Vector(0, -1)],
        #     [Vector(5, 6), Vector(0, -1)],
        #     [Vector(6, 6), Vector(0, -1)],
        #     [Vector(7, 6), Vector(0, -1)],
        #     [Vector(0, 3), Vector(0, 1)],
        #     [Vector(0, 4), Vector(0, -1)],
        #     [Vector(1, 0), Vector(1, 2)],
        #     [Vector(1, 0), Vector(-1, 2)],
        #     [Vector(6, 0), Vector(1, 2)],
        #     [Vector(6, 0), Vector(-1, 2)],
        #     [Vector(1, 7), Vector(1, -2)],
        #     [Vector(1, 7), Vector(-1, -2)],
        #     [Vector(6, 7), Vector(1, -2)],
        #     [Vector(6, 7), Vector(-1, -2)],
        #     [Vector(0, 0), Vector(0, 1)],
        #     [Vector(0, 0), Vector(0, 2)],
        #     [Vector(7, 0), Vector(0, 1)],
        #     [Vector(7, 0), Vector(0, 2)],
        #     [Vector(0, 7), Vector(0, -1)],
        #     [Vector(0, 7), Vector(0, -2)],
        #     [Vector(7, 7), Vector(0, -1)],
        #     [Vector(7, 7), Vector(0, -2)],
        # ] 
        
        # expected_legal_moves = list(map(list, expected_legal_moves))

        # actual_legal_moves = sorted(actual_legal_moves, key=lambda x: repr(x))
        # expected_legal_moves = sorted(expected_legal_moves, key=lambda x: repr(x))

        # print("\n")
        # print({"expected_legal_moves": expected_legal_moves})
        # print({"actual_legal_moves": actual_legal_moves})
        # self.assertEqual(
        #     actual_legal_moves,
        #     expected_legal_moves,
        #     "The actual legal moves are not the same as the expected legal moves"    
        # )


    # this test was written as I was confused about the source of a bug
    # I thought some move resultant vectors were some how outside the board
    # instead I was using a negative movement vector
    def test_legal_moves_in_board(self):
        # print("\nRunning test_legal_moves_in_board")
        def gen_random_board_states():
            # multiplier = 10
            multiplier = 3
            for _ in range(4*multiplier):
                yield random_board_state(moves=randint(0, 10))
            for _ in range(2*multiplier):
                yield random_board_state(moves=randint(0, 20))
            for _ in range(multiplier):
                yield random_board_state(moves=randint(0, 40))
            
        for board_state in gen_random_board_states():
            for to_v, movement_v in board_state.generate_legal_moves():
                resultant_v: Vector = to_v + movement_v
                self.assertTrue(
                    resultant_v.in_board(),
                    "All resultant vectors from legal moves should be in board"
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

        # print("board_state.get_piece_at_vector(Vector(6, 2))")
        # print(board_state.get_piece_at_vector(Vector(6, 2)))

        # print(Vector(6, 2).to_square())

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
        
        # print({"actual_legal_moves": actual_legal_moves})
        # print({"expected_legal_moves": expected_legal_moves})

        self.assertEqual(
            actual_legal_moves,
            expected_legal_moves,
            "\nActual (first) != Expected (second)"
        )

    # this tests for a bug I encountered where a knight couldn't take a piece, 
    # I created this test to identify the bug
    # I then modified the knight pieces class and used this test to show that the bug was fixed
    def test_troubleshoot_bug_legal_moves(self):
        # replicate the previous situation
        board_state = Board_State()
        board_state = board_state.make_move(
            Vector(1, 0), Vector(1, 2)
        )
        board_state = board_state.make_move(
            Vector(1, 7), Vector(1, -2)
        )
        board_state = board_state.make_move(
            Vector(6, 0), Vector(-1, 2)
        )
        board_state = board_state.make_move(
            Vector(6, 7), Vector(-1, -2)
        )
        board_state = board_state.make_move(
            Vector(4, 1), Vector(0, 1)
        )
        board_state = board_state.make_move(
            Vector(3, 6), Vector(0, -2)
        )

        # board_state.print_board()

        legal_moves = board_state.generate_legal_moves()

        # check that the knight can make the move
        self.assertTrue(
            (Vector(2, 2), Vector(1, 2)) in legal_moves
        ) 

    # this test is to ensure that the game over function can correctly identify a game over situation
    # The program crashed in a way that hasn't happened since (I must have been tinkering with the minimax code)
    # One of my assertion statements triggered and identified that the legal move variable was none.
    # this ensured that the program could successfully identify that the game wasn't over and that the king has one move
    # to correct the believed source of the bug, I ensured timed calls always perform at least a depth 1 search to ensure that a move is always produced.
    def test_troubleshoot_bug_game_over(self):
        pieces_matrix = deserialize_client_pieces_matrix(
            json.loads(
                """
                    [[[null,null],["B","♚"],[null,null],[null,null],[null,null],[null,null],[null,null],["B","♜"]],[["W","♜"],[null,null],[null,null],[null,null],["W","♛"],["B","♟︎"],["B","♟︎"],["B","♟︎"]],[[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null]],[[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null]],[[null,null],[null,null],[null,null],[null,null],["B","♟︎"],["W","♝"],[null,null],[null,null]],[[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null],[null,null]],[[null,null],["W","♟︎"],[null,null],[null,null],["W","♚"],[null,null],["W","♟︎"],["W","♟︎"]],[[null,null],[null,null],[null,null],[null,null],[null,null],["W","♝"],["W","♜"],[null,null]]]
                """
            )    
        )

        board_state = Board_State(
            next_to_go="B",
            pieces_matrix=pieces_matrix,
            check_encountered=True
        )

        # board_state.print_board()

        legal_moves = list(board_state.generate_legal_moves())

        # print({"legal_moves": legal_moves})

        self.assertEqual(
            legal_moves, 
            [(Vector(i=1, j=7), Vector(i=1, j=0))]
        )

        over, _ = board_state.is_game_over_for_next_to_go()
        # print(over)

        self.assertTrue(not over)


if __name__ == '__main__':
    unittest.main()
    
