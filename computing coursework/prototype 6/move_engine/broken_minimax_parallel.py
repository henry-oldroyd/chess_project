# import external and local modules

# import sys
import multiprocessing
from time import perf_counter

from .minimax import Move_Engine, is_time_expired
from .cache_managers import RAM_cache, DB_Cache

from chess_functions import Board_State
from assorted import ARBITRARILY_LARGE_VALUE, TimeOutError


# import time
def get_cores():
    return multiprocessing.cpu_count()
    # return multiprocessing.cpu_count()//2



# Classes with the name of JOB are essentially functions that represent a general task that can be completed concurrently
# they are classes as functions cannot be easily piped between threads


# this object represents a job that a concurrent worker should complete, 
# I used an object as a function cannot be sent between workers 
class Minimax_Sub_Job:
    # contractor: configure bot by setting these parameters as properties
    def __init__(self, move_engine, board_state, depth, cache_allowed, cache_manager, args, kwargs, max_time=None) -> None:
        self.move_engine: Move_Engine = move_engine
        self.board_state: Board_State = board_state

        # # not sure why depth sometimes is a single length tuple containing an int
        # # here is a quick fix
        # if isinstance(depth, tuple):
        #     if len(depth) == 1:
        #         depth = depth[0]
        # assert isinstance(depth, int)

        self.depth = depth,
        self.cache_allowed = cache_allowed
        self.cache_manager = cache_manager

        self.max_time = max_time


        # these are other erroneous argument that could be passed to the minimax call
        self.args = args
        self.kwargs = kwargs

    def __call__(self, legal_moves_sub_array):
        # perform part of a minimax search using a sub set of legal moves

        # print(f"running minimax job with legal moves sub array: (hash={hash(str(legal_moves_sub_array))})")
        # print(f"STARTING sub job on moves segment:   {hash(str(legal_moves_sub_array))}")
        # print(legal_moves_sub_array)d_state,
        result = self.move_engine.minimax_first_call(
            board_state=self.board_state,
            depth=self.depth,
            legal_moves_to_examine=legal_moves_sub_array,
            # is_time_expired = self.is_time_expired,
            max_time = self.max_time,
            *self.args,
            **self.kwargs
        )

      # print(f"FINISHING sub job on moves segment:   {hash(str(legal_moves_sub_array))}")
        # print(f"Minimax sub job finished (hash={hash(str(legal_moves_sub_array))})")
        return result


# this bot is responsible for performing a low depth search of a move to be used to presort the moves
class Presort_Moves_Sub_Job:
    # construct object 
    # def __init__(self, depth, board_state: Board_State, move_engine: Move_Engine, cache_manager, max_time=None) -> None:
    def __init__(self, depth, board_state: Board_State, move_engine: Move_Engine, max_time=None) -> None:
        # cache manager parameter may not be needed if the cache manager object is also bound to the move engine
        self.depth = depth
        self.board_state = board_state
        self.move_engine = move_engine
        # self.cache_manager = cache_manager
        # self.is_time_expired = is_time_expired
        self.max_time = max_time

    
    def __call__(self, move):
        # cache manager already built into the minimax move engine first call method

        # print(f"Presort job using cache manager:   {self.cache_manager!r}")
        # with self.cache_manager:
        #     child = self.board_state.make_move(*move)
        #     child_score, _ = self.move_engine.minimax_first_call(
        #         board_state = child,
        #         depth = self.depth
        #     )
        #     # print("Closing cache")
        #     result = (child_score, move)
        # return result
        
        # self interrupting
        if is_time_expired(self.max_time):
            raise TimeOutError()

        # score a child, use minimax first call to add caching
        # no need to say no parallel as a basic move engine is used
        child = self.board_state.make_move(*move)
        child_score, _ = self.move_engine.minimax_first_call(
            board_state = child,
            depth = self.depth,
            # is_time_expired = self.is_time_expired,                    
            max_time=self.max_time,
            
        )
        return (child_score, move)


# this is the main class to complete a minimax search in parallel. 
# some methods inherited form parent class while some are overwritten
class Parallel_Move_Engine(Move_Engine):
    # construct the engine using parameters
    def __init__(self, cache_manager: RAM_cache | None = DB_Cache(), cache_allowed: bool = True, parallel=True, min_parallel_depth=2, workers=get_cores(), **kwargs) -> None:
        self.parallel = parallel
        if parallel and cache_allowed:
            assert isinstance(cache_manager, DB_Cache), "Only DB cache an be used in parallel"
        self.min_parallel_depth = min_parallel_depth
        self.workers = workers

        # use parent class construction 
        super().__init__(cache_manager = cache_manager, cache_allowed = cache_allowed, **kwargs)

    def should_use_parallel(self, board_state: Board_State, depth):
        return depth >= self.min_parallel_depth and self.parallel

    # this function breaks up the legal moves array into many sub arrays that have a similar distribution of good and bad moves
    def break_up_legal_moves_to_segments(self, legal_moves: list, number_sub_arrays):
        # print("Legal moves:")
        # print(legal_moves)

        legal_move_sub_arrays = [[] for _ in range(number_sub_arrays)]

        # repeatedly add next best move to the end of the sub array
        i = 0
        while legal_moves:
            legal_move_sub_arrays[i].append(
                legal_moves.pop(0)
            )
            i = (i+1) % number_sub_arrays

        # reverse sub arrays so in order of best to worst
        
        legal_move_sub_arrays = list(map(
            lambda e: list(reversed(e)),
            legal_move_sub_arrays
        ))

        # print("Broken down")
        # for sub_array in legal_move_sub_arrays:
        #     print(sub_array)

        return legal_move_sub_arrays


    # this function runs the presort moves process in parallel 
    def generate_move_child_in_parallel(self, board_state: Board_State, depth: int, is_maximizer, give_child=True, max_time = None):
        # print("generate_move_child_in_parallel called")

        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()


        # explore_depth = max(depth-3, 0)
        explore_depth = max(depth-2, 0)

        # if cannot use cache then just use standard generate move child
        # if or if cannot use parallel of the explore depth is too low for it to be worth it 
        # then use standard generate move child method with caching, caching already initiated by first call
        # if (not self.cache_allowed):
        #     yield from super().generate_move_child(
        #         board_state = board_state,
        #         depth=depth,
        #         is_maximizer=is_maximizer,
        #         give_child=give_child,
        #         # is_time_expired=is_time_expired
        #         max_time=max_time
        #     )
        # elif (not self.parallel) or (explore_depth < 1):
        #     with self.cache_manager:
        #         yield from super().generate_move_child(
        #             board_state = board_state,
        #             depth=depth,
        #             is_maximizer=is_maximizer,
        #             give_child=give_child,
        #             # is_time_expired=is_time_expired
        #             max_time=max_time
        #         )

        # if (not self.parallel) or (explore_depth < 1):
        if (not self.parallel):
            yield from super().generate_move_child(
                board_state = board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=give_child,
                # is_time_expired=is_time_expired
                max_time=max_time
            )
        else:
            # if can do presort concurrently
        #   # print("getting legal moves")
            legal_moves = list(board_state.generate_legal_moves())

            # print("setting up job")
            # create move engine
            basic_move_engine = Move_Engine(
                presort_moves=True,
                additional_depth=0,
                use_validator=self.use_validator,






                cache_allowed=False, 
                cache_manager=None,
                # cache_allowed=True, 
                # cache_manager=self.cache_manager,
            )

            # create job
            job = Presort_Moves_Sub_Job(
                depth = explore_depth,
                board_state=board_state,
                move_engine=basic_move_engine,














                # cache_manager = self.cache_manager,
            








                max_time=max_time,
            )

            
            # concurrently map the job onto the iterable of legal moves
            print("generate_move_child_in_parallel: Using multiprocessing pool to presort in parallel")
            with multiprocessing.Pool(self.workers) as pool:
                moves_and_scores = pool.map(
                    func=job,
                    iterable=legal_moves
                )
            # print("generate_move_child_in_parallel: finished with multiprocessing pool")

            # self interrupting  
            if is_time_expired(max_time):
                raise TimeOutError()

            # sort by score
            moves_and_scores = sorted(
                moves_and_scores,
                key=lambda triplet: triplet[0],
                reverse=is_maximizer
            )
            # use map to get rid of score
            def move_and_blank_child(score_and_move):
                _, move = score_and_move
                return (move, None)
        
            moves_scores_children = map(move_and_blank_child, moves_and_scores)
            
            # print("children sorted by score")

            yield from moves_scores_children


    # this function performs a minimax search in parallel
    def parallel_minimax(self, board_state, depth, cache_allowed, cache_manager, max_time=None, *args, **kwargs):
        # print("Call  parallel_minimax")
        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()
        
        # print("parallel_minimax, checking cache")
        # if cache can be used then check if this search has already been complete
        if self.cache_allowed:
            result = self.cache_manager.search_cache(
                board_state=board_state,
                depth=depth
            )
            if result is not None:
                # print("no call needed as cache is sufficient")
                return result["score"], result["move"]

        # print("Parallel minimax called")

        # assert isinstance(depth, int)

        # assert depth >= 2, "depth must be greater or equal to 2 to do parallelization"

        is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)

        # print("started getting moves_and_child_sorted")
        # print("getting legal moves, presorted")

        # generate presorted moves iterable
        # print("parallel_minimax: calling generate_move_child_in_parallel")
        moves_sorted = list(self.generate_move_child_in_parallel(
            board_state=board_state,
            depth=depth,
            is_maximizer=is_maximizer,
            give_child=False,
            # is_time_expired=is_time_expired,
            max_time=max_time,
        ))

        # print("parallel_minimax: finished generate_move_child_in_parallel")

        # print("finished getting moves_and_child_sorted")
        # print("moves_sorted: ")
        # print(moves_sorted)
        

        # break up these pre sorted legal moves into segments for each sub job to work on
        # print("parallel_minimax, breaking up moves into sub arrays")
        legal_move_sub_arrays = self.break_up_legal_moves_to_segments(
            legal_moves=moves_sorted,
            number_sub_arrays=self.workers
        )

        # print("parallel_minimax: finished break_up_legal_moves_to_segments")

        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()

        # print("legal moves sub arrays generated")

        # print("Printing legal moves sub arrays")
        # print(legal_move_sub_arrays)

        # print("Defining job for workers")

        # print("parallel_minimax, defining sub job")
        # use these legal moves to do many simultaneous minimax operations
        # create a job function
        job = Minimax_Sub_Job(
            # move_engine=self,
            move_engine=Move_Engine(




                cache_manager=cache_manager,
                cache_allowed=cache_allowed, 
                # cache_allowed=False,
                # cache_manager=None,
        


                # is this the miracle fix?
                additional_depth= self.additional_depth,
                use_validator=self.use_validator,
                presort_moves=False,            
            ),
            board_state=board_state,
            depth=depth,













            cache_allowed=False,
            cache_manager=None,
            # cache_allowed=cache_allowed,
            # cache_manager=cache_manager,












            # is_time_expired = is_time_expired,
            max_time=max_time,

            args=args,
            kwargs=kwargs,
        )
        
        # job = Minimax_Sub_Job(*(None,)*7)
        
        # print(f"dill.pickles(job)    -->    {dill.pickles(job)}")

        # assert dill.pickles(job)
        # assert dill.pickles(legal_move_sub_arrays)

        # print(f"Using pool to complete jobs in parallel (pool size = {cores})")

        # map this job function onto the legal moves sub array in parallel
        # print("parallel_minimax: Using multiprocessing pool")
        with multiprocessing.Pool(self.workers) as pool:
            minimax_sub_job_results = pool.map(
                func = job,
                iterable=legal_move_sub_arrays
            )

        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()

        # print("parallel_minimax: multiprocessing finished")

        # set a best move and score variable with starting values
        best_move = None
        if is_maximizer:
            best_score = 0-(ARBITRARILY_LARGE_VALUE +1)
        else:
            best_score = ARBITRARILY_LARGE_VALUE +1

        # select best move
        for result in minimax_sub_job_results:
            score, move = result

            # if this move is better then update the best move and score variables
            if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
                best_score = score
                best_move = move

        if self.cache_allowed:
            self.cache_manager.add_to_cache(
                board_state=board_state,
                depth=depth,
                move=best_score,
                score=best_score
            )

        # print("finished getting best outcome")

        return best_score, best_move


    # this function is able to perform handle the initial non recursive call for a parallel minimax search
    def minimax_first_call_parallel(self, board_state: Board_State, depth, max_time=None, *args, **kwargs):
        # print(f"CALL   minimax_first_call_parallel")
        # print(f"CALL minimax_first_call_parallel(self, board_state={hash(board_state)}, depth={depth}, *args, **kwargs)")
        # assert isinstance(depth, int)
        
        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()
        

        should_use_parallel = self.should_use_parallel(board_state=board_state, depth=depth)
        # print(f"minimax_first_call_parallel:   should_use_parallel   -->   {should_use_parallel}")

        # self interrupting
        if is_time_expired(max_time):
            raise TimeOutError()
        

        # if should_use_parallel:
        #     def chosen_minimax_function(): 
        #         return self.parallel_minimax(
        #             board_state=board_state,
        #             depth=depth,
        #             cache_allowed=self.cache_allowed,
        #             cache_manager=self.cache_manager,
        #             # is_time_expired = is_time_expired,
        #             max_time=max_time,
        #             *args,
        #             **kwargs
        #         )
        # else:
        #     def chosen_minimax_function():
        #         return self.minimax(
        #             board_state=board_state,
        #             depth=depth,
        #             max_time=max_time,
        #             *args, **kwargs
        #         )


        # if self.cache_allowed:
        #     with self.cache_manager:
        #         result = chosen_minimax_function()
            
        # else:
        #     result = chosen_minimax_function()

        if should_use_parallel:
            if self.cache_allowed:
                with self.cache_manager:
                    result = self.parallel_minimax(
                        board_state=board_state,
                        depth=depth,
                        cache_allowed=self.cache_allowed,
                        cache_manager=self.cache_manager,
                        # is_time_expired = is_time_expired,
                        max_time=max_time,
                        *args,
                        **kwargs
                    )
            else:
                result = self.parallel_minimax(
                    board_state=board_state,
                    depth=depth,
                    cache_allowed=self.cache_allowed,
                    cache_manager=self.cache_manager,
                    # is_time_expired = is_time_expired,
                    max_time=max_time,
                    *args,
                    **kwargs
                )
                
        else:
            if self.cache_allowed:
                with self.cache_manager:
                    result = self.minimax(
                        board_state=board_state,
                        depth=depth,
                        max_time=max_time,
                        *args, **kwargs
                    )
            else:
                result = self.minimax(
                    board_state=board_state,
                    depth=depth,
                    max_time=max_time,
                    *args, **kwargs
                )


        if self.use_validator:
            self.validator(result=result, board_state=board_state)

        return result



    def __call__(self, *args, **kwargs):
        return self.minimax_first_call_parallel(*args, **kwargs)

class Move_Engine_Prime(Parallel_Move_Engine):
    def __init__(self) -> None:
        super().__init__(
            parallel=True,
            cache_allowed=True,
            cache_manager=DB_Cache(min_DB_depth=1),
            additional_depth=1,
            # additional_depth=0,
            presort_moves=True,
            color_maximizer_key={"W": True, "B": False},
            use_validator=False,
            # workers = get_cores()
            workers = 5
        )
        self.depth = 3


    def __call__(self, board_state: Board_State, depth=None, *args, **kwargs):
        if depth is None:
            return super().__call__(board_state=board_state, depth=self.depth, *args, **kwargs)
        else:
            return super().__call__(board_state=board_state, depth=depth, *args, **kwargs)
    

    # this function returns a boolean to decide if parallel processing is needed.
    # it takes the board state as a parameter as the evaluation could depend on the legal moves to analyze
    def should_use_parallel(self, board_state: Board_State, depth):
        # print("Calling (from prime class) should_use_parallel")

        if not self.parallel: 
            return False

        over, _ = board_state.is_game_over_for_next_to_go()
        if over:
            return False

        if board_state.check_encountered:
            likely_depth = depth + 0.5 * self.additional_depth
        else:
            likely_depth = depth

        board_state_a = board_state
        legal_moves_a = list(board_state.generate_legal_moves())
        some_legal_move_a = legal_moves_a[0]

        board_state_b = board_state_a.make_move(*some_legal_move_a)

        branching_factor_a = len(legal_moves_a)
        branching_factor_b = len(list(board_state_b.generate_legal_moves()))

        

        likely_branching_factor= 1/2 * (branching_factor_a + branching_factor_b)

        estimated_static_eval = likely_branching_factor ** likely_depth
        # print({"estimated_static_eval": estimated_static_eval})

        return (estimated_static_eval >= 400)
    

    def break_up_legal_moves_to_segments(self, legal_moves: list, number_sub_arrays):
        # print("Calling (from prime class) break_up_legal_moves_to_segments")

        legal_move_sub_arrays = [[] for _ in range(number_sub_arrays)]

        number_legal_moves = len(legal_moves)
        number_workers = self.workers

        moves_per_worker = number_legal_moves // number_workers

        workers_with_extra = number_legal_moves % number_workers
        workers_without_extra = number_workers - workers_with_extra

        moves_per_sub_array = [moves_per_worker] * workers_without_extra + [moves_per_worker+1] * workers_with_extra
        assert sum(moves_per_sub_array) == number_legal_moves

        # print(moves_per_sub_array)

        # >>> x = [1,2,3,4,5]
        # >>> x[:2]
        # [1, 2]
        # >>> x[2:]
        # [3, 4, 5]

        for worker_index in range(number_workers):
            moves_in_array = moves_per_sub_array[worker_index]
            legal_move_sub_arrays[worker_index] = legal_moves[:moves_in_array]
            legal_moves = legal_moves[moves_in_array:]

        # print("Broken down")
        # for sub_array in legal_move_sub_arrays:
        #     print(sub_array)

        yield from legal_move_sub_arrays






class Move_Engine_Timed(Move_Engine_Prime):
    def timed_call(self, board_state: Board_State, time):
        # so that internal jobs can access the time used up indicator
        # self.max_time = perf_counter() + time
        # take 3 seconds to close threads

        time_delta_allowed = time
        # time_delta_allowed = max(time - 3, 0)
        # time_delta_allowed = max(time - 10, 0)
        # time_delta_allowed = max(time - 4, 0.5)
        # print({"time_delta_allowed": time_delta_allowed})


        self.max_time = perf_counter() + time_delta_allowed
        def time_used_up():
            return perf_counter() >= self.max_time

        # need minimum of depth 1 as depth 0 doesn't give a move
        # deepest_result = self.minimax_first_call(board_state=board_state, depth=1)
        deepest_result = self.minimax_first_call(board_state=board_state, depth=1, variable_depth = 0)
        depth = 2
        # while True:
        while not time_used_up() and time_delta_allowed > 0:
            # print(f"Iterating again: time_used_up()   -->   {time_used_up()}")
            try:
                # deepest_result = self.minimax_first_call_parallel(board_state=board_state, depth=depth, is_time_expired=time_used_up)
                deepest_result = self.minimax_first_call_parallel(board_state=board_state, depth=depth, max_time=self.max_time, variable_depth=0)
                # print(f"Result at depth {depth}:   {deepest_result}")
            except TimeOutError:
                # print(f"Breaking: time_used_up()   -->   {time_used_up()}")
                break 
            else:
                # print(f"Completes depth={depth} so incrementing depth")
                depth += 1

        move, _ = deepest_result
        assert move is not None

        # print(f"Returning result at greatest depth={depth}")
        return deepest_result, depth

    def __call__(self, board_state: Board_State, time, *args, **kwargs):
        assert not board_state.is_game_over_for_next_to_go()[0]


        # start = perf_counter()
        deepest_result, _ = self.timed_call(board_state=board_state, time=time)
        # end = perf_counter()

        # time_delta = end - start
        # print(f"timed minimax set to {time} seconds actually took {round(time_delta, 3)} seconds")
        return deepest_result

def check_timed():
    board_state = Board_State()
    move_engine = Move_Engine_Timed()
    time=0

    # for _ in range(6):
    #     start = perf_counter()
    #     result, depth = move_engine(board_state, 1)
    #     time += perf_counter() - start
    #     print(f"At total time {time} sec: depth={depth};  result={result}")

    # for _ in range(6):
    #     start = perf_counter()
    #     result, depth = move_engine(board_state, 2)
    #     time += perf_counter() - start
    #     print(f"At total time {time} sec: depth={depth};  result={result}")

    # for _ in range(6):
    #     start = perf_counter()
    #     result, depth = move_engine(board_state, 5)
    #     time += perf_counter() - start
    #     print(f"At total time {time} sec: depth={depth};  result={result}")

    # for _ in range(6):
    #     start = perf_counter()
    #     result, depth = move_engine(board_state, 10)
    #     time += perf_counter() - start
    #     print(f"At total time {time} sec: depth={depth};  result={result}")

    # for _ in range(6):
    #     start = perf_counter()
    #     result, depth = move_engine(board_state, 15)
    #     time += perf_counter() - start
    #     print(f"At total time {time} sec: depth={depth};  result={result}")

    while True:
        start = perf_counter()
        result, depth = move_engine(board_state, 20)
        time += perf_counter() - start
        print(f"At total time {time} sec: depth={depth};  result={result}")
    
if __name__ == "__main__":
    check_timed()