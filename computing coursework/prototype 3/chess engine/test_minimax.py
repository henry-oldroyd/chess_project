# this test is responsible for testing various mutations of the minimax function and how they play, it is not a data driven test

# imports
from random import choice as random_choice
import pickle
import unittest
# from functools import wraps
import multiprocessing 
import os
import csv
from time import perf_counter

from game import Game
from board_state import Board_State
# from minimax import Move_Engine
from minimax_parallel import Move_Engine_Prime

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


def random_board_state(moves: int):
    board_state = Board_State()
    while True:
        try:
            for _ in range(moves):
                legal_moves = list(board_state.generate_legal_moves())
                # print(legal_moves)
                assert len(legal_moves) > 0
                random_move = random_choice(legal_moves)
                # print(f"Making move:   {board_state.get_piece_at_vector(random_move[0])}  {random_move[0].to_square()} to {(random_move[0] + random_move[1]).to_square()}")
                board_state = board_state.make_move(*random_move)

                # assert not board_state.is_game_over_for_next_to_go()

        except AssertionError:
            # print("Game over, trying again")
            continue
        else:
            return board_state


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


def time_function(function):
    start = perf_counter()
    result = function()
    end = perf_counter()
    time_delta = end - start
    return result, time_delta





def save_games(games: tuple, file_path):
    with open(file_path, "wb") as file:
        file.write(
            pickle.dumps(
                games
            )
        )


def load_games(file_path):
    if not os.path.exists(file_path):
        return dict()
    with open(file_path, "rb") as file:
        return pickle.loads(
            file.read()
        )


# this contains the majority of the logic to do a bot vs bot test with the game class
# it is a component as it isn't the whole test
def minimax_test_component(description, good_bot, bad_bot, success_criteria, write_to_csv, csv_folder, csv_file_name, load_game = False):
    # print(f"CALL minimax_test_component(description={description}, write_to_csv={write_to_csv})")
    # sourcery skip: extract-duplicate-method

    # good bot and bad bot make decisions about moves, 
    # the test is designed to assert that good bot wins (and or draws in some cases)

    # generate csv path
    if write_to_csv:
        # not sure why but the description sometimes contains an erroneous colon, this is caught and removed
        # was able to locate bug to here, as it is a test I added a quick fix
        # bug located, some description stings included them


        # prevent adding to a previous trial
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        csv_path = f"{csv_folder}/{csv_file_name}.csv"

        # overwrite so it is blank
        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(("Move_counter", "B_score", "from_square", "to_square", "W_score"))

    pickle_file_path = f"{csv_folder}/{csv_file_name}.games"
    if load_game and os.path.exists(pickle_file_path):
        print("Attempting to load game")
        indexes = (-1, -2)
        games = load_games(pickle_file_path)
        for game in games:
            print(hash(game))
            print(game.board_state.next_to_go)
        for index in indexes:
            try:
                game = games[index]
                assert game.board_state.next_to_go == "W", "next to go wasn't user so use other game"
            except Exception as e:
                print(e)
                continue
            else:
                print(f"Using game {hash(game)} at index {index}")
                games = games[:index]
    else:
        print("Creating new game")
        game: Game = Game()
        games = tuple()

    # start a new blank game
    # depth irrelevant as computer move function passed as parameter
    print()
    print(f"Beginning test game:   {description}")

    def record_new_game(games, new_game):
        games = tuple(list(games) + [new_game])
        save_games(games, pickle_file_path)
        return games

    games = record_new_game(games, game)

    # keep them making moves until return statement breaks loop
    while True:
        # print()
        # game.board_state.print_board()
        # print()
        # get move choice from bad bot

        result, time_delta = time_function(
            lambda: bad_bot(game)
        )
        score, move_choice = result

        # serialised to is can be passed as a user move (reusing game class)
        position_vector, movement_vector = move_choice
        resultant_vector = position_vector + movement_vector
        from_square, to_square = position_vector.to_square(), resultant_vector.to_square()

    
        # implement bad bot move and update csv
        # move, score = game.implement_user_move(from_square=from_square, to_square=to_square, time_delta=time_delta)
        move, _ = game.implement_user_move(from_square=from_square, to_square=to_square, time_delta=time_delta, estimated_utility=score)

        games = record_new_game(games, game)


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
        success, msg, board_state = success_criteria(game, description=description)
        if success is not None:
            # game.board_state.print_board()
            return success, msg, board_state

        # providing good bot function, implement good bot move and update csv
        move, score = game.implement_computer_move(best_move_function=good_bot)

        games = record_new_game(games, game)

        if write_to_csv:
            csv_write_move_score(
                file_path=csv_path,
                move=move,
                score=game.board_state.static_evaluation(),
                move_counter=game.move_counter
            )


        position_vector, movement_vector = move
        resultant_vector = position_vector + movement_vector
        piece_moved = game.board_state.get_piece_at_vector(resultant_vector)
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




# picks a good move
# has constructor to allow for configuration 
class Good_Bot():
    # configure for depth and allow variable depth
    def __init__(self, depth, cache_allowed=False):
        self.depth = depth
        # self.move_engine = Move_Engine_Prime(cache_allowed=cache_allowed)
        self.move_engine = Move_Engine_Prime()
        self.move_engine.cache_allowed = cache_allowed
    
    # make minimax function call given config
    def __call__(self, game):
        return self.move_engine(
            board_state=game.board_state,
            depth=self.depth
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
                if game.board_state.is_3_board_repeats_in_game_history() and self.allow_stalemate_3_states_repeated:
                    # game.board_state.print_board()
                    # print(f"Success: Stalemate at {game.moves} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes")
                    # return True, f"Success: Stalemate at {game.move_counter} moves in test {description}: 3 repeat board states, outcome specify included in allowed outcomes", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
                    return True, f"Success: Stalemate at in test {description}: 3 repeat board states, outcome specify included in allowed outcomes", map_pieces_matrix_to_symbols(game.board_state.pieces_matrix)
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
        # return pool.map(
        #     func = execute_test_job,
        #     iterable = test_data
        # )
        yield from pool.map(
            func = execute_test_job,
            iterable = test_data
        )

# test case contains unit tests
# multitasking only occurs within a test, tests are themselves executed sequentially 
# I could pool all tests into one test function but this way multiple failures can occur in different tests 
# (one single test would stop at first failure)


overnight = False

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

    # # tests basic minimax vs random moves
    # def test_vanilla_depth_1_vs_randotron(self):
    #     # 10 trials as outcome is linked to a random behaviour
    #     trials = RANDOM_TRIAL_NUM

    #     # test package generated to include relevant data and logic (bots and success criteria)
    #     def generate_jobs():
    #         for num in range(1, trials+1):
    #             yield {
    #                 "description": "test: depth 1 vanilla vs randotron",
    #                 "good_bot": Good_Bot(depth=1, check_extra_depth=False),
    #                 "bad_bot": Random_Bot(),
    #                 "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
    #                 "write_to_csv": True,
    #                 "csv_folder": "./test_reports/test_vanilla_depth_1_vs_randotron",
    #                 "csv_file_name": f"test_{num}"
    #             }

    #     self.check_test_results(
    #         pool_jobs(
    #             generate_jobs()
    #         )
    #     )

    
    # def test_advanced_depth_1_vs_randotron(self):
    #     trials = RANDOM_TRIAL_NUM

    #     # test package generated to include relevant data and logic (bots and success criteria)
    #     def generate_jobs():
    #         for num in range(1, trials+1):
    #             yield {
    #                 "description": "test: depth 1 advanced vs randotron",
    #                 "good_bot": Good_Bot(depth=1, check_extra_depth=True),
    #                 "bad_bot": Random_Bot(),
    #                 "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
    #                 "write_to_csv": True,
    #                 "csv_folder": "./test_reports/test_advanced_depth_1_vs_randotron",
    #                 "csv_file_name": f"test_{num}"
    #             }

    #     self.check_test_results(
    #         pool_jobs(
    #             generate_jobs()
    #         )
    #     )




    # def test_depth_2_vs_randotron(self):
    #     trials = RANDOM_TRIAL_NUM

    #     # test package generated to include relevant data and logic (bots and success criteria)
    #     def generate_jobs():
    #         for num in range(1, trials+1):
    #             yield {
    #                 "description": "test: depth 2 advanced vs randotron",
    #                 "good_bot": Good_Bot(depth=2, check_extra_depth=True),
    #                 "bad_bot": Random_Bot(),
    #                 "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #                 "write_to_csv": True,
    #                 "csv_folder": "./test_reports/test_depth_2_vs_randotron",
    #                 "csv_file_name": f"test_{num}"
    #             }

    #     self.check_test_results(
    #         pool_jobs(
    #             generate_jobs()
    #         )
    #     )



    
    # def test_depth_1_advanced_vs_depth_1_vanilla(self):
    #     # only one trial needed as outcome is deterministic

    #     test_data = {
    #         "description": "test: test depth 1 advanced vs depth_1 vanilla",
    #         "good_bot": Good_Bot(depth=1, check_extra_depth=True),
    #         "bad_bot": Good_Bot(depth=1, check_extra_depth=False),
    #         # they aren't different enough in efficacy to guarantee no draws
    #         "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=True),
    #         "write_to_csv": True,
    #         "csv_folder": "./test_reports/test_depth_1_advanced_vs_depth_1_vanilla",
    #         "csv_file_name": "test_1"
    #     }        
        
    #     self.check_test_results(
    #         pool_jobs(
    #             (test_data,)
    #         )
    #     )


    # def test_depth_2_vs_depth_1(self):

    #     # only one trial needed as outcome is deterministic
    #     test_data = {
    #         "description": "test: depth 2 vs depth 1",
    #         "good_bot": Good_Bot(depth=2, check_extra_depth=True),
    #         "bad_bot": Good_Bot(depth=1, check_extra_depth=True),
    #         "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #         "write_to_csv": True,
    #         "csv_folder": "./test_reports/test_depth_2_vs_depth_1",
    #         "csv_file_name": "test_1"
    #     }

    #     self.check_test_results(
    #         pool_jobs(
    #             (test_data,)
    #         )
    #     )
    # def test_depth_3_vs_depth_2(self):

    #     # only one trial needed as outcome is deterministic
    #     test_data = {
    #         "description": "test: depth 3 vs depth 2",
    #         "good_bot": Good_Bot(depth=3, check_extra_depth=True),
    #         "bad_bot": Good_Bot(depth=2, check_extra_depth=True),
    #         "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #         "write_to_csv": True,
    #         "csv_folder": "./test_reports/test_depth_3_vs_depth_2",
    #         "csv_file_name": "test_1"
    #     }

    #     self.check_test_results(
    #         pool_jobs(
    #             (test_data,)
    #         )
    #     )

    # def test_depth_3_vs_depth_1(self):

    #     # only one trial needed as outcome is deterministic
    #     test_data = {
    #         "description": "test: depth 3 vs depth 1",
    #         "good_bot": Good_Bot(depth=3, check_extra_depth=True),
    #         "bad_bot": Good_Bot(depth=1, check_extra_depth=True),
    #         "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #         "write_to_csv": True,
    #         "csv_folder": "./test_reports/test_depth_3_vs_depth_1",
    #         "csv_file_name": "test_1"
    #     }

    #     self.check_test_results(
    #         pool_jobs(
    #             (test_data,)
    #         )
    #     )

    # def test_depth_3_vs_randotron(self):
    #     trials = RANDOM_TRIAL_NUM

    #     # test package generated to include relevant data and logic (bots and success criteria)
    #     def generate_jobs():
    #         for num in range(1, trials+1):
    #             yield {
    #                 "description": "test: depth 3 vs randotron",
    #                 "good_bot": Good_Bot(depth=3, check_extra_depth=True),
    #                 "bad_bot": Random_Bot(),
    #                 "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #                 "write_to_csv": True,
    #                 "csv_folder": "./test_reports/test_depth_3_vs_randotron",
    #                 "csv_file_name": f"test_{num}"
    #             }

    #     self.check_test_results(
    #         pool_jobs(
    #             generate_jobs()
    #         )
    #     )

    # @unittest.skipIf(not overnight, "Test takes too long")
    # def test_depth_2_vs_depth_1(self):
    #     # only one trial needed as outcome is deterministic
    #     test_data = {
    #         "description": "test: depth 2 vs depth 1",
    #         "good_bot": Good_Bot(depth=2, cache_allowed=False),
    #         "bad_bot": Good_Bot(depth=1, cache_allowed=False),
    #         "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
    #         "write_to_csv": True,
    #         "csv_folder": "./test_reports/test_depth_2_vs_depth_1",
    #         "csv_file_name": "test_1",
    #         # "load_game": (True, -1),
    #         "load_game": False,
    #     }

    #     success, msg, _ = execute_test_job(test_data)
        
    #     if msg is not None:
    #         print(msg)
    #     self.assertTrue(
    #         success,
    #         msg=msg
    #     )

    # @unittest.skipIf(not overnight, "test takes too long")   
    def test_depth_3_vs_depth_2(self):
        # only one trial needed as outcome is deterministic
        test_data = {
            "description": "test: depth 3 vs depth 2",
            "good_bot": Good_Bot(depth=3, cache_allowed=False),
            "bad_bot": Good_Bot(depth=2, cache_allowed=False),
            "success_criteria": Success_Criteria(allow_stalemate_3_states_repeated=False),
            "write_to_csv": True,
            "csv_folder": "./test_reports/test_depth_3_vs_depth_2",
            "csv_file_name": "test_1",
            # "load_game": (True, -1),
            "load_game": False,
        }

        success, msg, _ = execute_test_job(test_data)
        
        if msg is not None:
            print(msg)
        self.assertTrue(
            success,
            msg=msg
        )


    # @unittest.skipIf(not overnight, "test takes too long")   
    def test_deterministic_outcomes_parallel(self):
        with_parallel_engine = Move_Engine_Prime()
        without_parallel_engine = Move_Engine_Prime()

        for engine in (with_parallel_engine, without_parallel_engine):
            engine.cache_allowed = False
            engine.depth = 2
            engine.additional_depth = 0

        def always(*args, **kwargs): return True
        def never(*args, **kwargs): return False

        with_parallel_engine.should_use_parallel = always
        without_parallel_engine.should_use_parallel = never

        for trial in range(1, 101):
            try:
                moves = random_choice(range(10, 50))
                board_state = random_board_state(moves)

                score_parallel, _ = with_parallel_engine(board_state)
                score_non_parallel, _ = without_parallel_engine(board_state)

                fail_msg = f"Test moves={moves} hash={hash(board_state)}: score parallel != without -->  {score_parallel} != {score_non_parallel}"
                assert score_parallel == score_non_parallel, fail_msg
            except AssertionError as e:
                print(f"TEST FAILURE: (trial={trial})")
                board_state.print_board()
                print(repr(board_state))
                self.fail(str(e))
            except Exception as e:
                self.fail(f"UNEXPECTED ERROR (trial = {trial}):   {str(e)}")

    
if __name__ == '__main__':
    unittest.main()