import random
from minimax_parallel import Move_Engine_Prime, DB_Cache
from board_state import Board_State

from random import choice as random_choice, randint as random_int
from time import perf_counter
from math import sqrt
from itertools import product as iter_product



def mean_and_standard_deviation(times):
    f = len(times)
    if f == 0:
        return None, None
    sum_x = sum(times)
    sum_x_squared = sum(time**2 for time in times)

    mean = sum_x / f
    variance = (sum_x_squared/f) - mean**2
    standard_deviation = sqrt(variance)

    return round(mean, 2), round(standard_deviation, 2)

def run_benchmark():

    # move_engine = Move_Engine_Prime()
    # board_state = random_board_state(30)
    # print("Performing minimax at variable depth on this board state:")
    # board_state.print_board()

    # print("\n")
    # for depth in range(6):
        
    #     start = perf_counter()
    #     result = move_engine(board_state, depth)
    #     time_delta = perf_counter() - start

    #     print(f"\nRESULT:  move_engine(board_state, {depth}) finished in {time_delta}   -->   {result}\n")

    # cache_manager = DB_Cache(min_DB_depth=1)
    
    move_engine_4_workers = Move_Engine_Prime(cache_allowed=False, workers=4)
    move_engine_8_workers = Move_Engine_Prime(cache_allowed=False, workers=8)
    move_engine_linear = Move_Engine_Prime(cache_allowed=False, parallel=False)

    num_workers_move_engine_times_array = (
        (4, move_engine_4_workers, []),
        (8, move_engine_8_workers, []),
        (1, move_engine_linear, []),
    )

    trials = 10
    depth = 3

    print(f"Completing time trial testing for {len(num_workers_move_engine_times_array)} variables across {trials} trials")
    print(f"controlling depth at {depth} and disabling cacheting")
    print()
    try:
        for trial in range(1, trials+1):
            board_state = random_board_state(random_int(0, 30))

            for workers, move_engine, times in num_workers_move_engine_times_array:
                start = perf_counter()
                move_engine(board_state, depth)
                end = perf_counter()

                time_delta = end - start
                times.append(time_delta)

                print(f"Trial {trial} completed for {workers} workers in {round(time_delta, 2)} sec")
    except KeyboardInterrupt:
        pass

    for workers, _, times in num_workers_move_engine_times_array:
        mean, standard_deviation = mean_and_standard_deviation(times)
        print()
        print(f"For {trials} trials, {workers} workers:")
        print(f"The mean time was: {mean} sec    with a standard deviation of: {standard_deviation}sec")
        print()


# def main():
#     # cache_manager = DB_Cache(min_DB_depth=0)
#     cache_manager = DB_Cache(min_DB_depth=1)
#     move_engine_with_cache = Move_Engine_Prime(cache_allowed=True, cache_manager=cache_manager)
#     move_engine_no_cache = Move_Engine_Prime(cache_allowed=False)

#     trials = 5
#     depth = 4
#     moves_range = range(4, 10)


#     times_with_cache = []
#     times_no_cache = []
#     for trial in range(1, trials+1):
#         board_state = random_board_state(
#             random_choice(moves_range)            
#         )
#         print(f"trial {trial}, analysing the following board state:  {hash(board_state)}")
#         board_state.print_board()
#         print("\n")


#         start = perf_counter()
#         result_with_cache = move_engine_with_cache(board_state, depth)
#         end = perf_counter()
#         time_delta_with_cache = end - start
#         times_with_cache.append(time_delta_with_cache)

#         start = perf_counter()
#         result_no_cache = move_engine_no_cache(board_state, depth)
#         end = perf_counter()
#         time_delta_no_cache = end - start
#         times_no_cache.append(time_delta_no_cache)

#         error_msg = f"Error: Minimax functions returned results of different score:  cache != no cache --->  {result_with_cache[0]} != {result_no_cache[0]}"
#         # cache may use a more in depth search leading to a different score
#         # assert result_with_cache[0] == result_no_cache[0], error_msg

#         print(f"trial {trial} of board state {hash(board_state)}:   with cache {round(time_delta_with_cache, 2)} sec,    no cache {round(time_delta_no_cache, 2)} sec")
#         print("\n")

#     mean_cache, standard_deviation_cache = mean_and_standard_deviation(times_with_cache)
#     print()
#     print(f"For {trials} trials, with cache")
#     print(f"The mean time was: {mean_cache} sec    with a standard deviation of: {standard_deviation_cache}sec")
#     print()

#     mean_no_cache, standard_deviation_no_cache = mean_and_standard_deviation(times_no_cache)
#     print()
#     print(f"For {trials} trials, with cache")
#     print(f"The mean time was: {mean_no_cache} sec    with a standard deviation of: {standard_deviation_no_cache}sec")
#     print()

def time_function(function):
    start = perf_counter()
    result = function()
    end = perf_counter()
    time_delta = end - start
    return result, time_delta


def main():
    worker_values = [1, 2, 4, 8, 5]

    move_engines_by_workers = {
        1: Move_Engine_Prime(),
        2: Move_Engine_Prime(),
        4: Move_Engine_Prime(),
        8: Move_Engine_Prime(),
        5: Move_Engine_Prime(),
    }
    move_engines_by_workers[1].parallel = False
    move_engines_by_workers[2].workers = 2
    move_engines_by_workers[4].workers = 4
    move_engines_by_workers[8].workers = 8
    move_engines_by_workers[5].workers = 5

    for workers in worker_values:
        move_engines_by_workers[workers].cache_allowed = False
        move_engines_by_workers[workers].additional_depth = False


    times_by_workers_by_depth = {
        2: {
            1: [],
            2: [],
            4: [],
            8: [],
            5: [],
        },
        3: {
            1: [],
            2: [],
            4: [],
            8: [],
            5: [],
        },
    }
    


    trials = 1
    # moves_range = range(0, 50)
    moves_range = (30,)


    for trial in range(1, trials+1):
        moves = random_choice(moves_range)
        board_state = random_board_state(moves)
        print(f"trial {trial}, analysing the following board state:  {hash(board_state)}  (moves={moves})")
        board_state.print_board()
        print("\n")

        for depth in (2, 3):
            print(f"trial {trial}, analysing board state:  {hash(board_state)}  (moves={moves}, depth={depth})")

            result_scores = []

            for workers in worker_values:
                result, time_delta = time_function(lambda: move_engines_by_workers[workers](board_state, depth))
                score, _ = result

                times_by_workers_by_depth[depth][workers].append(time_delta)
                result_scores.append(score)
            
            try: 
                assert all(result == result_scores[0] for result in result_scores)
            except AssertionError:
                raise ValueError(f"Result scores where different (deterministic no caching so should be the same):  {result_scores}")
            else:
                print(f"Common minimax score:  {result_scores[0]}")

            print(f"trial {trial} of board state {hash(board_state)} at depth={depth} finished")
            print()

    for depth in (2, 3):
        for workers, times_array in times_by_workers_by_depth[depth].items():
            # mean, standard_deviation = mean_and_standard_deviation(times_array)
            mean, _ = mean_and_standard_deviation(times_array)
            print()
            print(f"For {trials} trials, with {workers} workers at depth {depth}: the mean time was {mean} sec")
            # print(f"The mean time was {mean} sec    with a standard deviation was {standard_deviation} sec")
            # print(f"The mean time was {mean} sec")
            # print()


def build_cache():
    cache_manager = DB_Cache(min_DB_depth=0)
    move_engine = Move_Engine_Prime(cache_manager=cache_manager)

    while True:
        moves_advanced = random.randint(16, 48)
        board_state = random_board_state(moves_advanced)
        for depth in (2, 3):
            start = perf_counter()
            score, move = move_engine(board_state, depth)
            duration = perf_counter() - start

            duration = round(duration, 2)

            from_v, move_v = move
            to_v = from_v + move_v
            from_v, to_v = from_v.to_square(), to_v.to_square()

            print(f"{moves_advanced} moves in: move_engine(<{hash(board_state)}>, {depth}) took {duration} sec  -->  score: {score} with move {from_v} to {to_v}")

if __name__ == "__main__":
    main()