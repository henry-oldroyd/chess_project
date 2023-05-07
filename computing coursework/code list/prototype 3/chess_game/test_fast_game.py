import unittest
import pickle

from .game import Game

from assorted import NotComputerTurn, NotUserTurn
from chess_functions import King, Queen, Rook, Bishop, Pawn, Board_State, Vector
from move_engine import Move_Engine_Prime

class Test_Case(unittest.TestCase):
    # this test checks that a game object can be preserved when it is encoded to binary and then loaded back  
    def test_save_and_restore(self):
        game = Game(
            echo=False,
            time=10,
        )

        # make a load of changes to the game object
        game.implement_user_move(from_square="A2", to_square="A4")
        game.implement_computer_move(best_move_function=lambda *arg, **kwargs: [0, [Vector(0, 6), Vector(0, -2)]])
        game.implement_user_move(from_square="B2", to_square="B4")
        game.implement_computer_move(best_move_function=lambda *arg, **kwargs: [0, [Vector(1, 6), Vector(0, -2)]])
        game.implement_user_move(from_square="C2", to_square="C4")
        game.implement_computer_move(best_move_function=lambda *arg, **kwargs: [0, [Vector(2, 6), Vector(0, -2)]])

        original_game = game

        pickle_file_path = "chess_game/test_data/test_save_and_restore/saved_game.game"

        # dump it to binary and save to a file 
        with open(pickle_file_path, "wb") as file:
            file.write(
                pickle.dumps(
                    game
                )
            )

        # read the binary and load it back into an object
        with open(pickle_file_path, "rb") as file:
            reloaded_game = pickle.loads(
                file.read()
            )
        
        # check that the games are the same
        self.assertTrue(
            original_game == reloaded_game,
            "The original game was not the same as the saved and reloaded game"    
        )

    def test_whose_go(self):
        # this function tests that the validation present can stop a player going twice in a row
        game = Game(time=2)

        game.implement_user_move(from_square="A2", to_square="A4")

        def try_to_make_user_move(*args, **kwargs):
            game.implement_user_move(from_square="B2", to_square="B4")

        def try_to_make_computer(*args, **kwargs):
            game.implement_computer_move()

        self.assertRaises(
            NotUserTurn,
            try_to_make_user_move,
            "The user shouldn't be able to make 2 consecutive turns"    
        )

        game.implement_computer_move()

        self.assertRaises(
            NotComputerTurn,
            try_to_make_computer,
            "The computer shouldn't be able to make 2 consecutive turns"
        ) 
    
    # @unittest.skip("Test takes too long, depth ")
    # def test_specific_bug_null_move(self):
    #     pieces_matrix = [
    #         [Rook("B"), King("B"), None, None, None, None, Queen("W"), None],
    #         [None, Pawn("B"), Pawn("B"), None, None, None, None, None],
    #         [Pawn("B"), None, None, None, None, None, None, None],
    #         [None, None, None, Pawn("W"), None, None, None, None],
    #         [None, None, None, None, None, Bishop("W"), None, None],
    #         [None, None, Pawn("W"), None, None, None, None, None],
    #         [Pawn("W"), None, None, None, None, Pawn("W"), None, Pawn("W")],
    #         [None, Rook("W"), None, None, None, King("W"), None, None]
    #     ]
    #     next_to_go = "B"

    #     board_state = Board_State(next_to_go, pieces_matrix)
    #     print()
    #     board_state.print_board()
        
    #     move_engine = Move_Engine_Prime()
    #     move_engine.cache_allowed = False
    #     move_engine.cache_manager = None
    #     move_engine.parallel = False

    #     # self.assertRaises(
    #     #     AssertionError,
    #     #     lambda: move_engine(board_state, depth=4)
    #     # )

    #     def absolute(x): return x if x >= 0 else 0-x


    #     # _, move = move_engine(board_state, depth=1)
    #     # self.assertTrue(move is not None)
    #     # board_state = board_state.make_move(*move)
    #     # print()
    #     # board_state.print_board()


    #     # _, move = move_engine(board_state, depth=1)
    #     # self.assertTrue(move is not None)
    #     # board_state = board_state.make_move(*move)
    #     # print()
    #     # board_state.print_board()


    #     # _, move = move_engine(board_state, depth=1)
    #     # self.assertTrue(move is not None)
    #     # board_state = board_state.make_move(*move)
    #     # print()
    #     # board_state.print_board()



  
    #     print(board_state.is_game_over_for_next_to_go())
    #     print(list(board_state.generate_legal_moves()))

    #     score, move = move_engine(board_state, depth=4)


    #     self.assertTrue(
    #         absolute(score) < 1_000_001 and move is not None,
    #         msg=repr({"score": score, "move": move})
    #     )


if __name__ == '__main__':
    unittest.main()
