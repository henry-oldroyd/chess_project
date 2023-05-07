# this test is responsible for testing various mutations of the minimax function and how they play, it is not a data driven test

# imports of external modules. 
from random import choice as random_choice, randint
# from itertools import product as iter_product
import pickle
import unittest
# from functools import wraps
import multiprocessing
import os
import csv
from time import perf_counter


# imports of local modules
from chess_game import Game
# from chess_functions import Board_State
# from minimax import Move_Engine
from move_engine import Move_Engine_Timed, Move_Engine_Prime
from chess_functions import random_board_state

# from assorted import ARBITRARILY_LARGE_VALUE
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
# it converts pieces to symbols it they are not none
def map_pieces_matrix_to_symbols(pieces_matrix):
    return list_map(
        lambda row: list_map(
            lambda square: square.symbol() if square else None,
            row
        ),
        pieces_matrix
    )

# this functions updates a CSV file with the moves and scores of a chess game for graphical analysis in excel
# each move in the game causes a new row to be added
def csv_write_move_score(file_path,  move_counter, move, score):
    # convert move to a pair of squares
    position_vector, movement_vector = move
    resultant_vector = position_vector + movement_vector

    from_square = position_vector.to_square()
    to_square = resultant_vector.to_square()

    # # if file doesn't exist, create is and add the headers
    # if not os.path.exists(file_path):
    #     with open(file_path, "w", newline="") as file:
    #         writer = csv.writer(file, delimiter=",")
    #         writer.writerow(("from_square", "to_square", "score"))

    # add data as a new row
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        # writer.writerow(("Move_counter", "B_score", "from_square", "to_square", "W_score"))
        writer.writerow((move_counter, -score, from_square, to_square, score))


# this function is used to time another function to allow for performance testing
def time_function(function):
    start = perf_counter()
    result = function()
    end = perf_counter()
    time_delta = end - start
    return result, time_delta


# this function aims to save games to a file as part of an unfinished feature 
def save_games(games: tuple, file_path):
    with open(file_path, "wb") as file:
        file.write(
            pickle.dumps(
                games
            )
        )

# this method aims to load a game from a file as part of another unfinished feature
def load_games(file_path):
    if not os.path.exists(file_path):
        return dict()
    with open(file_path, "rb") as file:
        return pickle.loads(
            file.read()
        )

# the below function contains the logic to perform a test between 2 minimax bots to assert that the good bot is better

# this contains the majority of the logic to do a bot vs bot test with the game class
# it is a component as it isn't the whole test
def minimax_test_component(description, good_bot, bad_bot, success_criteria, write_to_csv, csv_folder, csv_file_name, load_game=False, save_game=False):
    # print(f"CALL minimax_test_component(description={description}, write_to_csv={write_to_csv})")
    # sourcery skip: extract-duplicate-method

    # good bot and bad bot make decisions about moves,
    # the test is designed to assert that good bot wins (and or draws in some cases)


    # if the write to csv file it enabled
    # generate csv path
    if write_to_csv:
        # not sure why but the description sometimes contains an erroneous colon, this is caught and removed
        # was able to locate bug to here, as it is a test I added a quick fix
        # bug located, some description stings included them

        # create folders
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        # create file with headers if is doesn't exist
        csv_path = f"{csv_folder}/{csv_file_name}.csv"

        # overwrite so it is blank
        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(("Move_counter", "B_score", "from_square", "to_square", "W_score"))

    # pickle_file_path = f"{csv_folder}/{csv_file_name}.games"
    # if load_game and os.path.exists(pickle_file_path):
    #     print("Attempting to load game")
    #     indexes = (-1, -2)
    #     games = load_games(pickle_file_path)
    #     for game in games:
    #         print(hash(game))
    #         print(game.board_state.next_to_go)
    #     for index in indexes:
    #         try:
    #             game = games[index]
    #             assert game.board_state.next_to_go == "W", "next to go wasn't user so use other game"
    #         except Exception as e:
    #             print(e)
    #             continue
    #         else:
    #             print(f"Using game {hash(game)} at index {index}")
    #             games = games[:index]
    # else:

    # create a new game 
    print("Creating new game")
    game: Game = Game(echo=True)
        # games = tuple()

    # start a new blank game
    # depth irrelevant as computer move function passed as parameter
    print()
    print(f"Beginning test game:   {description}")

    # def record_new_game(games, new_game):
    #     games = tuple(list(games) + [new_game])
    #     save_games(games, pickle_file_path)
    #     return games

    # if save_game:
    #     games = record_new_game(games, game)

    # keep them making moves until return statement breaks loop
    while True:
        # print()
        # game.board_state.print_board()
        # print()
        # get move choice from bad bot

        # the bad bots move is implemented as the user as the user plays as white (advantage)
        result, time_delta = time_function(
            lambda: bad_bot(game)
        )
        score, move_choice = result
        # print({"move_choice": move_choice})

        # serialised to is can be passed as a user move (reusing game class)
        position_vector, movement_vector = move_choice
        resultant_vector = position_vector + movement_vector
        from_square, to_square = position_vector.to_square(), resultant_vector.to_square()

        # implement bad bot move and update csv
        # move, score = game.implement_user_move(from_square=from_square, to_square=to_square, time_delta=time_delta)
        move, _ = game.implement_user_move(from_square=from_square, to_square=to_square, time_delta=time_delta, estimated_utility=score)

        # games = record_new_game(games, game)

        if write_to_csv:
            csv_write_move_score(
                file_path=csv_path,
                move=move,
                score=game.board_state.static_evaluation(),
                move_counter=game.move_counter
            )

        # piece_moved = game.board_state.get_piece_at_vector(resultant_vector)
        # print(f"Move {game.move_counter}: bad bot moved {piece_moved} from {from_square} to {to_square} with a score perceived of {score}")

        # if game.board_state.color_in_check():
        #    print(f"CHECK:  {game.board_state.next_to_go} in check")

        # see if this move causes the test to succeed or fail or keep going

        # use the provided success criteria to determine if the game should be over. 
        success, msg, board_state = success_criteria(game, description=description)
        # result = success_criteria(game, description=description)
        # print({"result": result})
        # success, msg, board_state = result

        if success is not None:
            # game.board_state.print_board()
            return success, msg, board_state


        # repeat for the good bot
        # providing good bot function, implement good bot move and update csv
        move, score = game.implement_computer_move(best_move_function=good_bot)

        # games = record_new_game(games, game)

        # update CSV
        if write_to_csv:
            csv_write_move_score(
                file_path=csv_path,
                move=move,
                score=game.board_state.static_evaluation(),
                move_counter=game.move_counter
            )
        # unpack move in terms of to and from squares 
        position_vector, movement_vector = move
        resultant_vector = position_vector + movement_vector
        # piece_moved = game.board_state.get_piece_at_vector(resultant_vector)
        from_square, to_square = position_vector.to_square(), resultant_vector.to_square()
        # print(f"Move {game.move_counter}: good bot moved {piece_moved} from {from_square} to {to_square} with a score perceived of {score}")

        # if game.board_state.color_in_check():
        #    print(f"CHECK:  {game.board_state.next_to_go} in check")

        # again check if this affects the test
        success, msg, board_state = success_criteria(game, description=description)
        if success is not None:
            # game.board_state.print_board()
            return success, msg, board_state

        # # if needed provide console output to clarify that slow bot hasn't crashed
        # if game.move_counter % 10 == 0 or depth >= 3:
        # print(f"Moves {game.move_counter}:  static evaluation -> {game.board_state.static_evaluation()}, Minimax evaluation -> {score} by turn {description}")


# below are some function that have been programmed as classes with a __call__ method.
# these are basically fancy functions that CAN BE HASHED.
# I had to manually do this under the hood hashing as it is needed to allow communication between the threads
# a job must be hashable to be piped to a thread (separate python instance)


# this is a pipe-able object that makes a random move
class Random_Bot():
    # picks a random move
    def __call__(self, game):
        # determine move at random
        legal_moves = list(game.board_state.generate_legal_moves())
        assert len(legal_moves) != 0
        # match minimax output structure
        # score, best_move
        return None, random_choice(legal_moves)

    def __hash__(self) -> int:
        return hash("I am random bot, I am a unique singleton so each instance can share a hash")


# this bot picks a good move
# it exploration is limited by time
# has constructor to allow for configuration
class Bot_By_Time():
    # configure for depth and allow variable depth
    def __init__(self, time, cache_allowed=False):
        self.time = time
        self.move_engine = Move_Engine_Timed()
        self.move_engine.cache_allowed = cache_allowed

    # make minimax function call given config
    def __call__(self, game):
        return self.move_engine(
            board_state=game.board_state,
            time=self.time
        )
        # result = self.move_engine(
        #     board_state=game.board_state,
        #     time=self.time
        # )
        # print(f"Bot_By_Time:   result={result}")
        # return result

    def __hash__(self) -> int:
        return hash(f"Bot_By_Time(time={self.time})")
    

# this is a bot that has its exploration limited by depth
class Bot_By_Depth():
    # configure for depth and allow variable depth
    def __init__(self, depth, cache_allowed=False):
        self.depth = depth
        self.move_engine = Move_Engine_Prime()
        self.move_engine.cache_allowed = cache_allowed

    # make minimax function call given config
    def __call__(self, game):
        return self.move_engine(
            board_state=game.board_state,
            depth=self.depth
        )
        # result = self.move_engine(
        #     board_state=game.board_state,
        #     depth=self.depth
        # )
        # print(f"Bot_By_Depth:   result={result}")
        # return result

    def __hash__(self) -> int:
        return hash(f"Bot_By_Depth(depth={self.depth})")


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
            # case True, None, "Stalemate":
            case True, None, _:
                # game.board_state.print_board()
                if game.board_state.is_3_board_repeats_in_game_history() and self.allow_stalemate_3_states_repeated:
                    # game.board_state.print_board()
                    # print(f"Success: Stalemate at {game.move_counter} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes")
                    # return True, f"Success: Stalemate at {game.move_counter} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
                    return (
                        True, 
                        f"Success: Stalemate at in test {description}: 3 repeat board states, outcome specify included in allowed outcomes", 
                        map_pieces_matrix_to_symbols(game.board_state.pieces_matrix),
                    )
                else:
                    # game.board_state.print_board()
                    # print(f"FAILURE: ({description}) stalemate caused (3 repeats?  -> {game.board_state.is_3_board_repeats_in_game_history()})")
                    return (
                        False, 
                        f"FAILURE: ({description}) stalemate caused (3 repeats?  -> {game.board_state.is_3_board_repeats_in_game_history()})", 
                        map_pieces_matrix_to_symbols(game.board_state.pieces_matrix),
                    )
            # good bot loss causes test to fail
            # case True, 1, "Checkmate":
            case True, 1, _:
                # game.board_state.print_board()
                # print(f"Failure: ({description}) computer lost")
                return (
                    False, 
                    f"Failure: ({description}) computer lost", 
                    map_pieces_matrix_to_symbols(game.board_state.pieces_matrix),
                )
            # good bot win causes test to pass
            # case True, -1, "Checkmate":
            case True, -1, _:
                # game.board_state.print_board()
                # print(f"SUCCESS: ({description}) Game has finished and been won in {game.move_counter} moves")
                return (
                    True, 
                    f"SUCCESS: ({description}) Game has finished and been won in {game.move_counter} moves", 
                    map_pieces_matrix_to_symbols(game.board_state.pieces_matrix),
                )
            # if the game isn't over, return success as none and test will continue
            case False, _, _:
                return (
                    None, 
                    None, 
                    None,
                )

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


# this pool jobs function for completing tests in parallel is not needed when the move engine is parallelized

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
        # return pool.map(
        #     func = execute_test_job,
        #     iterable = test_data
        # )
        yield from pool.map(
            func=execute_test_job,
            iterable=test_data
        )


# test case contains unit tests
# multitasking only occurs within a test, tests are themselves executed sequentially
# I could pool all tests into one test function but this way multiple failures can occur in different tests
# (one single test would stop at first failure)

overnight = False
RANDOM_TRIAL_NUM = 3

# this function asserts that are elements in a list are the same
def test_same(some_list):
    assert len(some_list) > 0
    return all(some_list[0] == element for element in some_list)


# @unittest.skip("Takes too long")
class Test_Case(unittest.TestCase):

    # this function takes the results of the tests from the test pool and checks the results with a unittest
    # a failure is correctly identified to correspond to the function that called this function
    # reduces repeated logic
    def check_test_results(self, test_results):
        # for success, msg, final_pieces_matrix in test_results:
        for success, msg, _ in test_results:
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

    # this function tests that a cached call always produces the same result as one without caching
    # it also ensures that the second cache call for the same search is much faster
    # this test is completed on many random board states
    def test_cache_is_faster(self):
        trials = 40
        # trials = 5

        # create and configure move engines
        move_engine_with_cache = Move_Engine_Prime()
        move_engine_without_cache = Move_Engine_Prime()

        move_engine_without_cache.cache_allowed = False

        for move_engine in (move_engine_with_cache, move_engine_without_cache):
            move_engine.depth = 2
            move_engine.cache_manager.allow_greater_depth = False


        # repeat test for many trials
        for _ in range(trials):
            # note random_board_state as a function is inefficient as it is used for testing only, takes a while
            # generate a random board state
            board_state = random_board_state(60)
            # turn of 3 repeat stalemates so cache and without behave the same
            board_state.three_repeat_stalemates_enabled = False

            # board_state.print_board()

            # check result with out cache 
            true_result = move_engine_without_cache(board_state)
            true_result = list(true_result)
            true_result[1] = list(true_result[1])

            # attempt 1 with cache
            first_cache_result, first_cache_time_delta = time_function(
                lambda: move_engine_with_cache(board_state)
            )
            first_cache_result = list(first_cache_result)
            first_cache_result[1] = list(first_cache_result[1])

            # check that the results were the same
            self.assertEqual(
                first_cache_result,
                true_result,
                "The first cache call should give the same result as without cache"
            )

            # attempt 2 with cache
            second_cache_result, second_cache_time_delta = time_function(
                lambda: move_engine_with_cache(board_state)
            )

            second_cache_result = list(second_cache_result)
            second_cache_result[1] = list(second_cache_result[1])

            # check that the results were again the same
            self.assertEqual(
                first_cache_result,
                true_result,
                "The second cache call should give the same result as without cache"
            )

            # check that with cache was much faster
            self.assertLessEqual(
                second_cache_time_delta,
                0.2 * first_cache_time_delta,
                "When using database cache, the lookup should be at least 5 times quicker than calculation"    
            )

    # tests basic minimax vs random moves
    def test_timed_vs_randotron(self):
        trials = RANDOM_TRIAL_NUM

        # test package generated to include relevant data and logic (bots and success criteria)
        def generate_jobs():
            for num in range(1, trials+1):
                for time in [2, 5, 10, 20]:
                    yield {
                        "description": f"test: {time}s timed move engine vs randotron",
                        "good_bot": Bot_By_Time(time=time),
                        "bad_bot": Random_Bot(),
                        "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
                        "write_to_csv": True,
                        "csv_folder": "./test_reports/test_timed_vs_randotron",
                        "csv_file_name": f"test_timed_{time}s_num_{num}"
                    }

        def generate_test_results():
            for test_specs in generate_jobs():
                yield minimax_test_component(**test_specs)

        self.check_test_results(
            generate_test_results()    
        )

    # tests basic minimax vs random moves
    @unittest.skip("takes too long")
    def test_depth_vs_randotron(self):
            trials = RANDOM_TRIAL_NUM

            # test package generated to include relevant data and logic (bots and success criteria)
            def generate_jobs():
                for num in range(1, trials+1):
                    # for depth in range(4):
                    for depth in [1, 2]:
                        yield {
                            "description": f"test: depth {depth} move engine vs randotron",
                            "good_bot": Bot_By_Depth(depth=depth),
                            "bad_bot": Random_Bot(),
                            "success_criteria": Success_Criteria(
                                allow_stalemate_3_states_repeated=(depth<=1)
                            ),
                            "write_to_csv": True,
                            "csv_folder": "./test_reports/test_depth_vs_randotron",
                            "csv_file_name": f"test_depth_{depth}_num_{num}"
                        }

            def generate_test_results():
                for test_specs in generate_jobs():
                    yield minimax_test_component(**test_specs)

            self.check_test_results(
                generate_test_results()    
            )

    # test that bots that can explore more are better 
    # @unittest.skip("takes too long")
    def test_bots_by_depth(self):
        # test package generated to include relevant data and logic (bots and success criteria)
        def generate_jobs():
            # don't do depth 0s as they cannot decide a move
            for depth_greater in (3,):
            # for depth_greater in (2, 3):
                # ensure depth_a >= depth_b
                # for depth_lesser in range(1, depth_greater):
                # for depth_lesser in range(1, depth_greater+1):
                # allow_draw = (depth_lesser == depth_greater)
                depth_lesser = depth_greater - 1
                yield {
                    "description": f"test: depth {depth_greater} bot vs depth {depth_lesser} bot",
                    "good_bot": Bot_By_Depth(depth=depth_greater),
                    "bad_bot": Bot_By_Depth(depth=depth_lesser),
                    "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
                    # "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=allow_draw),
                    "write_to_csv": True,
                    "csv_folder": "./test_reports/test_bots_by_depth",
                    "csv_file_name": f"test_depth_{depth_greater}_vs_depth_{depth_lesser}"
                }

        def generate_test_results():
            for test_specs in generate_jobs():
                yield minimax_test_component(**test_specs)

        self.check_test_results(
            generate_test_results()    
        )

    # test that bots that can explore more are better 
    def test_bots_by_time(self):
        # test package generated to include relevant data and logic (bots and success criteria)
        def generate_jobs():
            time_deltas = [2, 5, 10, 15, 20]
            for time_delta_lesser in time_deltas:
                time_delta_greater = max(1.4*time_delta_lesser, 4+time_delta_lesser)
                # time_delta_greater = max(2*time_delta_lesser, 10+time_delta_lesser)
                # time_delta_greater = max(4*time_delta_lesser, 15+time_delta_lesser)
                yield {
                    "description": f"test: {time_delta_greater}s timed bot vs {time_delta_lesser}s timed bot",
                    "good_bot": Bot_By_Time(time=time_delta_greater),
                    "bad_bot": Bot_By_Time(time=time_delta_lesser),
                    # "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
                    "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
                    "write_to_csv": True,
                    "csv_folder": "./test_reports/test_bots_by_time",
                    "csv_file_name": f"test_{time_delta_greater}s_timed_bot_vs_{time_delta_lesser}s_timed_bot"
                }

        def generate_test_results():
            for test_specs in generate_jobs():
                yield minimax_test_component(**test_specs)

        self.check_test_results(
            generate_test_results()
        )

    # test what the parallel move engine doesn't produce a different output
    def test_deterministic_outcomes_parallel(self):
        # create move engines and configures them
        with_parallel_engine = Move_Engine_Prime()

        without_parallel_engine = Move_Engine_Prime()

        for engine in (with_parallel_engine, without_parallel_engine):
            engine.cache_allowed = False
            engine.additional_depth = 0


        with_parallel_engine.parallel = True
        without_parallel_engine.parallel = False

        def always(*args, **kwargs): return True
        def never(*args, **kwargs): return False

        with_parallel_engine.should_use_parallel = always
        without_parallel_engine.should_use_parallel = never


        # generate a large number of random board states
        def gen_random_board_states():
            for _ in range(40):
                yield random_board_state(moves=randint(0, 10))
            for _ in range(20):
                yield random_board_state(moves=randint(0, 20))
            for _ in range(10):
                yield random_board_state(moves=randint(0, 40))

        # test that for each board state, the move engines produce the same deterministic outcome 
        for board_state in gen_random_board_states():
            score_parallel, move_parallel = with_parallel_engine(board_state)
            score_non_parallel, move_non_parallel = without_parallel_engine(board_state)

            fail_msg = f"Test hash={hash(board_state)}: score parallel != without -->  {score_parallel} != {score_non_parallel}"
            # assert score_parallel == score_non_parallel, fail_msg
            self.assertEqual(
                score_parallel, score_non_parallel, fail_msg    
            )

            fail_msg = f"Test hash={hash(board_state)}: move parallel != without -->  {move_parallel} != {move_non_parallel}"
            # assert move_parallel == move_non_parallel, fail_msg
            self.assertEqual(
                move_parallel, move_non_parallel, fail_msg
            )

        # for trial in range(1, 101):
        #     try:
        #         moves = random_choice(range(10, 50))
        #         board_state = random_board_state(moves)

        #         score_parallel, _ = with_parallel_engine(board_state)
        #         score_non_parallel, _ = without_parallel_engine(board_state)

        #         fail_msg = f"Test moves={moves} hash={hash(board_state)}: score parallel != without -->  {score_parallel} != {score_non_parallel}"
        #         assert score_parallel == score_non_parallel, fail_msg
        #     except AssertionError as e:
        #         print(f"TEST FAILURE: (trial={trial})")
        #         board_state.print_board()
        #         print(repr(board_state))
        #         self.fail(str(e))
        #     except Exception as e:
        #         self.fail(f"UNEXPECTED ERROR (trial = {trial}):   {str(e)}")


if __name__ == '__main__':
    unittest.main()
