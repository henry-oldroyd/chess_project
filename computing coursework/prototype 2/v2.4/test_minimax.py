# this test is responsible for testing various mutations of the minimax function and how they play, it is not a data driven test

# imports
from random import choice as random_choice
import unittest
# from functools import wraps
import multiprocessing 
import os.path
import csv

from game import Game
from minimax import minimax
from assorted import ARBITRARILY_LARGE_VALUE
# from board_state import Board_State
# from vector import Vector

# # was not needed in the end, this decorator would have repeated a given function a given number of times 
# def repeat_decorator_factory(times):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for _ in range(times):
#                 func(*args, **kwargs)
#         return wrapper
#     return decorator

# this is a utility function that maps a function across an iterable but also converts the result to a list data structure 
def list_map(func, iter):
    return list(map(func, iter))

# this function is used to serialize a pieces matrix for output in a message
# it converts pieces to symbols
def map_pieces_matrix_to_symbols(pieces_matrix):
    return list_map(
        lambda row: list_map(
            lambda square: square.symbol() if square else None,
            row
        ),
        pieces_matrix
    )

# this functions updates a CSV file with the moves and scores of a chess game for graphical analysis in excel
def csv_write_move_score(file_path, move, score):
    # convert move to a pair of squares
    position_vector, movement_vector = move
    resultant_vector = position_vector + movement_vector

    from_square = position_vector.to_square()
    to_square = resultant_vector.to_square()

    # if file doesn't exist, create is and add the headers
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(("from_square", "to_square", "score"))
    
    # add data as a new row
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow((from_square, to_square, score))

# this contains the majority of the logic to do a bot vs bot test with the game class
# it is a component as it isn't the whole test
def minimax_test_component(description, good_bot, bad_bot, success_criteria, write_to_csv=False):
    # print(f"CALL minimax_test_component(description={description}, write_to_csv={write_to_csv})")
    # sourcery skip: extract-duplicate-method

    # good bot and bad bot make decisions about moves, 
    # the test is designed to assert that good bot wins (and or draws in some cases)

    # generate csv path
    if write_to_csv:
        # not sure why but the description sometimes contains an erroneous colon, this is caught and removed
        # was able to locate bug to here, as it is a test I added a quick fix
        # bug located, some description stings included them
        csv_path = f"test_reports/{description}.csv".replace(" ", "_").replace(":", "")

        # prevent adding to a previous trial
        if os.path.exists(csv_path):
            # overwrite so it is blank
            with open(csv_path, "w") as file:
                file.write("")

    # start a new blank game
    # depth irrelevant as computer move function passed as parameter
    game: Game = Game()

    # keep them making moves until return statement breaks loop
    while True:
        # get move choice from bad bot
        _, _, move_choice = bad_bot(game)
        
        # serialised to is can be passed as a user move (reusing game class)
        position_vector, movement_vector = move_choice
        resultant_vector = position_vector + movement_vector
        from_square, to_square = position_vector.to_square(), resultant_vector.to_square()

        # implement bad bot move and update csv
        move, score = game.implement_user_move(from_square=from_square, to_square=to_square)
        if write_to_csv:
            csv_write_move_score(
                file_path=csv_path,
                move=move,
                score=score
            )

        # see if this move causes the test to succeed or fail or keep going
        success, msg, board_state = success_criteria(game, description=description)
        if success is not None:
            return success, msg, board_state

        # providing good bot function, implement good bot move and update csv
        move, score = game.implement_computer_move(best_move_function=good_bot)
        if write_to_csv:
            csv_write_move_score(
                file_path=csv_path,
                move=move,
                score=game.board_state.static_evaluation()
            )

        # again check if this affects the test
        success, msg, board_state = success_criteria(game, description=description)
        if success is not None:
            return success, msg, board_state

        # # if needed provide console output to clarify that slow bot hasn't crashed
        # if game.move_counter % 10 == 0 or depth >= 3:
        # print(f"Moves {game.move_counter}:  static evaluation -> {game.board_state.static_evaluation()}, Minimax evaluation -> {score} by turn {description}")


# below are some function that have been programmed as classes with a __call__ method. 
# these are basically fancy functions that CAN BE HASHED. 
# I had to manually do this under the hood hashing as it is needed to allow communication between the threads
# a job must be hashable to be piped to a thread (separate python instance)


class Random_Bot():
    # picks a random move
    def __call__(self, game):
        # determine move at random
        legal_moves = list(game.board_state.generate_legal_moves())
        assert len(legal_moves) != 0
        # match minimax output structure
        # score, best_child, best_move
        return None, None, random_choice(legal_moves)
    def __hash__(self) -> int:
        return hash("I am random bot, I am a unique singleton so each instance can share a hash")




# picks a good move
# has constructor to allow for configuration 
class Good_Bot():
    # configure for depth and allow variable depth
    def __init__(self, depth, check_extra_depth):
        self.depth = depth
        self.check_extra_depth = check_extra_depth
    
    # make minimax function call given config
    def __call__(self, game):
        return minimax(
            board_state=game.board_state,
            is_maximizer=(game.board_state.next_to_go == "W"),
            depth=self.depth,
            alpha=(-1)*ARBITRARILY_LARGE_VALUE,
            beta=ARBITRARILY_LARGE_VALUE,
            check_extra_depth=self.check_extra_depth
        )
    def __hash__(self) -> int:
        return hash(f"Good_Bot(depth={self.depth}, check_extra_depth={self.check_extra_depth})")


# used to look at a game and decide if the test should finish
class Success_Criteria():
    # constructor allow config for stalemates to sill allow test to pass
    def __init__(self, allow_stalemate_3_states_repeated: bool):
        self.allow_stalemate_3_states_repeated = allow_stalemate_3_states_repeated
    def __call__(self, game: Game, description):
        # returns: success, message, serialised pieces matrix

        # call game over and use a switch case to decide what to do
        match game.check_game_over():

            # if 3 repeat stalemate, check with config wether is is allows
            case True, None, "Stalemate":
                # game.board_state.print_board()
                if game.is_3_board_repeats_in_game_history and self.allow_stalemate_3_states_repeated:
                    # game.board_state.print_board()
                    # print(f"Success: Stalemate at {game.moves} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes")
                    return True, f"Success: Stalemate at {game.move_counter} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
                else:
                    # game.board_state.print_board()
                    # print(f"FAILURE: ({description}) stalemate caused (3 repeats?  -> {game.is_3_board_repeats_in_game_history()})")
                    return False, f"FAILURE: ({description}) stalemate caused (3 repeats?  -> {game.is_3_board_repeats_in_game_history()})", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
            # good bot loss causes test to fail
            case True, 1, "Checkmate":
                # game.board_state.print_board()
                # print(f"Failure: ({description}) computer lost")
                return False, f"Failure: ({description}) computer lost", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
            # good bot win causes test to pass
            case True, -1, "Checkmate":
                # game.board_state.print_board()
                # print(f"SUCCESS: ({description}) Game has finished and been won in {game.move_counter} moves")
                return True, f"SUCCESS: ({description}) Game has finished and been won in {game.move_counter} moves", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
            # if the game isn't over, return success as none and test will continue
            case False, _, _:
                return None, None, None

    def hash(self):
        return hash(f"Success_Criteria(allow_stalemate_3_states_repeated={self.allow_stalemate_3_states_repeated})")




# given a test package (config for one test), carry it out
def execute_test_job(test_data_package):
    # deal with unexplained bug where argument is tuple / list length 1 containing relevant dict (quick fix as only a test)
    # I was able to identify that this is where it occurs and add a correction but I am not sure what the cause of the bug is
    if any(isinstance(test_data_package, some_type) for some_type in (tuple, list)):
        if len(test_data_package) == 1:
            test_data_package = test_data_package[0]

    # print(f"test_data_package   -->   {test_data_package}")

    # really simple, call minimax test component providing all keys in package as keyword arguments
    return minimax_test_component(**test_data_package)


# this function takes an iterable of hashable test_packages 
# it all 8 logical cores on my computer to multitask to finish the test sooner
def pool_jobs(test_data):
    # counts logical cores
    # my CPU is a 10th gen i7
    # it has 4 cores and 8 logical cores due to hyper threading 
    # with 4-8 workers I can use 100% of my CPU
    cores = multiprocessing.cpu_count()

    # create a pool
    with multiprocessing.Pool(cores) as pool:
        # map the execute_test_job function across the set of test packages using multitasking
        # return the result
        return pool.map(
            func = execute_test_job,
            iterable = test_data
        )

# test case contains unit tests
# multitasking only occurs within a test, tests are themselves executed sequentially 
# I could pool all tests into one test function but this way multiple failures can occur in different tests 
# (one single test would stop at first failure)

class Test_Case(unittest.TestCase):

    # this function takes the results of the tests from the test pool and checks the results with a unittest
    # a failure is correctly identified to correspond to the function that called this function
    # reduces repeated logic
    def check_test_results(self, test_results):
        for success, msg, final_pieces_matrix in test_results:
            # print()
            # for row in final_pieces_matrix:
            #     row = "  ".join(map(
            #         lambda square: str(square).replace("None", ". "),
            #         row
            #     ))
            #     print(row)
            # print(msg)
            
            # i choose to iterate rather than assert all as this allows me to have the appropriate message on failure 
            self.assertTrue(
                success,
                msg=msg
            )

    # tests basic minimax vs random moves
    def test_vanilla_depth_1_vs_randotron(self):
        # 10 trials as outcome is linked to a random behaviour
        trials = 10

        # test package generated to include relevant data and logic (bots and success criteria)
        test_data = {
            "description": "test: depth 1 vanilla vs randotron",
            "good_bot": Good_Bot(depth=1, check_extra_depth=False),
            "bad_bot": Random_Bot(),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] +  [test_data_but_to_csv]
            )
        )

    
    def test_advanced_depth_1_vs_randotron(self):
        trials = 10

        test_data = {
            "description": "test: depth 1 advanced vs randotron",
            "good_bot": Good_Bot(depth=1, check_extra_depth=True),
            "bad_bot": Random_Bot(),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )




    def test_depth_2_vs_randotron(self):
        trials = 10

        test_data = {
            "description": "test: depth 2 advanced vs randotron",
            "good_bot": Good_Bot(depth=2, check_extra_depth=True),
            "bad_bot": Random_Bot(),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )

    
    def test_depth_1_advanced_vs_depth_1_vanilla(self):
        # only one trial needed as outcome is deterministic
        trials = 1

        test_data = {
            "description": "test: depth 1 vanilla vs depth 1 variable check",
            "good_bot": Good_Bot(depth=1, check_extra_depth=True),
            "bad_bot": Good_Bot(depth=1, check_extra_depth=False),
            # they aren't different enough in efficacy to guarantee no draws
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )

    def test_depth_2_vs_depth_1(self):
        trials = 1 

        test_data = {
            "description": "test: depth 2 vs depth 1",
            "good_bot": Good_Bot(depth=2, check_extra_depth=True),
            "bad_bot": Good_Bot(depth=1, check_extra_depth=True),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )

    def test_depth_3_vs_depth_2(self):
        trials = 1

        test_data = {
            "description": "test: depth 3 vs depth 2",
            "good_bot": Good_Bot(depth=3, check_extra_depth=True),
            "bad_bot": Good_Bot(depth=2, check_extra_depth=True),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )


    def test_depth_3_vs_depth_1(self):
        trials = 1

        test_data = {
            "description": "test: depth 3 vs depth 1",
            "good_bot": Good_Bot(depth=3, check_extra_depth=True),
            "bad_bot": Good_Bot(depth=1, check_extra_depth=True),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )


    def test_depth_3_vs_randotron(self):
        trials = 4

        test_data = {
            "description": "test: depth 3 vs randotron",
            "good_bot": Good_Bot(depth=3, check_extra_depth=True),
            "bad_bot": Random_Bot(),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": False
        }

        # only trial will write to a csv
        test_data_but_to_csv = test_data.copy()
        test_data_but_to_csv["write_to_csv"] = True

        self.check_test_results(
            pool_jobs(
                (trials-1) * [test_data] + [test_data_but_to_csv]
            )
        )


    
if __name__ == '__main__':
    unittest.main()