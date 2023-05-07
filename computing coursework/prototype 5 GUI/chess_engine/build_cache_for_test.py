import multiprocessing
from random import randint, choice as random_choice
import time

from minimax import Move_Engine, JSON_Cache_Manual_Save
from board_state import Board_State


def random_board_state(moves: int, seed_board_state=None):
    if seed_board_state is None:
        seed_board_state = Board_State()

    board_state = seed_board_state

    for _ in range(moves):
        random_move = random_choice(list(board_state.generate_legal_moves()))
        board_state = board_state.make_move(*random_move)

    return board_state


def multi_processor(job, argument_iterable):
    cores = multiprocessing.cpu_count()
    with multiprocessing.Pool(cores) as pool:
        return pool.map(
            func=job,
            iterable=argument_iterable
        )

print("creating json cache manager manual save")
cache_manager = JSON_Cache_Manual_Save()

move_engine = Move_Engine(
    cache_allowed=True,
    cache_manager=cache_manager,
    variable_depth=False
)


def job(job_data):
    depth, moves = job_data["depth"], job_data["moves"]
    start = time.perf_counter()
    move_engine(
        board_state=random_board_state(moves),
        depth=depth
    )
    return time.perf_counter() - start


def generate_argument_iterable(batch_size, depth, moves_range):
    for _ in range(batch_size):
        yield {
            "depth": depth,
            "moves": random_choice(moves_range)
        }



def execute_batch_and_save(batch_size, depth, moves_range):
    argument_iterable = generate_argument_iterable(batch_size=batch_size, depth=depth, moves_range=moves_range)
    previous_cache_size = move_engine.cache_manager.cache_size()

    print(f"STARTING:   execute_batch_and_save(batch_size={batch_size}, depth={depth}, moves_range={moves_range})")
    times = multi_processor(
        job=job,
        argument_iterable=argument_iterable
    )
    mean_time = sum(times) / len(times)
    print(f"FINISHED:   execute_batch_and_save(batch_size={batch_size}, depth={depth}, moves_range={moves_range})")
    print(f"Mean time:   {mean_time}")

    new_cache_size = move_engine.cache_manager.cache_size()
    new_cache = move_engine.cache_manager.memoization_cache
    print(f"New cache:\n{new_cache}")


    print(f"Saving {new_cache_size - previous_cache_size} new cache items...")
    cache_manager.save()
    print("Cache saved to json")

def main():
    execute_batch_and_save(batch_size=2, depth=2, moves_range=range(1))
    # execute_batch_and_save(batch_size=1, depth=4, moves_range=range(1))
    # execute_batch_and_save(batch_size=40, depth=2, moves_range=range(1, 11))
    # execute_batch_and_save(batch_size=16, depth=3, moves_range=range(1, 11))

if __name__ == "__main__":
    main()



# def job(i): return f"HI:  {i}"

# cores = multiprocessing.cpu_count()

# def main():
#     with multiprocessing.Pool(cores) as p:
#         result = (
#             p.map(
#                 job, 
#                 range(8)
#             )
#         )

#     print(result)

# if __name__ == "__main__":
#     main()