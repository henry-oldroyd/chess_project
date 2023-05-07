# import local modules
# cannot import game as causes circular import, if necessary put in same file
from .board_state import Board_State
from .assorted import ARBITRARILY_LARGE_VALUE, TimeOutError
from .vector import Vector
from . import cache_managers as cm

from collections.abc import Iterable
# import multiprocessing
from time import perf_counter


def print_decorator(function):
    name = function.__name__
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        print(f"{name}(args={args!r}, kwargs={kwargs!r})  -->  {result!r}")
        return result
    return wrapper

class Minimax_Sub_Job:
    def __init__(self, move_engine, board_state, depth, args, kwargs) -> None:
        self.move_engine = move_engine
        self.board_state = board_state
        self.depth = depth
        self.args = args
        self.kwargs = kwargs

    def __call__(self, legal_moves_sub_array):
        return self.move_engine.minimax(
            board_state=self.board_state,
            depth=self.depth,
            legal_moves_to_examine=legal_moves_sub_array,
            *self.args,
            **self.kwargs
        )


class Move_Engine():
    # def __init__(self, variable_depth: bool = True, additional_depth=1, presort_moves: bool = True, color_maximizer_key: dict | None = None, cache_allowed: bool = True, use_validator: bool = False, parallelize: bool=False) -> None:
    # def __init__(self, cache_manager: RAM_cache| None = None, cache_allowed: bool = True, variable_depth: bool = True, additional_depth=1, presort_moves: bool = True, color_maximizer_key: dict | None = None, use_validator: bool = False) -> None:
    def __init__(self, cache_manager: cm.RAM_cache | None = cm.JSON_Cache(), cache_allowed: bool = True, additional_depth=1, presort_moves: bool = True, color_maximizer_key: dict | None = None, use_validator: bool = False) -> None:

        self.additional_depth = additional_depth
        # self.variable_depth = additional_depth >= 1
        self.use_validator = use_validator


        # if parallelize:
        #     self.presort_moves = True
        #     self.parallelize = True
        # else:
        #     self.presort_moves = presort_moves
        #     self.parallelize = False

        self.presort_moves = presort_moves

        if color_maximizer_key is not None:
            self.color_maximizer_key = color_maximizer_key
        else:
            self.color_maximizer_key = {"W": True, "B": False}
        
        # self.cache_allowed = cache_allowed
        # if cache_allowed:
        #     self.cache_manager = JSON_cache()
        #   # print("Reusing json cache singleton object")
        #     self.cache_manager = singleton_JSON_cache
        #     # self.cache_manager = RAM_cache()
        # else:
        #     self.cache_manager = None
    
        if cache_allowed:
            assert cache_manager is not None, f"Cache manager is None, not provided"
            # assert isinstance(cache_manager, cm.RAM_cache), f"Cache manager is of type {type(cache_manager)!r} not of type RAM_cache"
            self.cache_allowed = True
            self.cache_manager = cache_manager
        else:
            self.cache_allowed = False
            self.cache_manager = None
        
        self.static_evaluations_presort = 0
        self.static_evaluations_non_presort = 0
    
    @property
    def variable_depth(self):
        return self.additional_depth > 0

    @property
    def static_evaluations(self):
        return self.static_evaluations_presort + self.static_evaluations_non_presort

    def generate_move_child(self, board_state: Board_State, depth: int, is_maximizer, give_child=True):
        # returns move, child
        if (not self.presort_moves) or (depth <= 1):
            for move in board_state.generate_legal_moves():
                child_board_state: Board_State = board_state.make_move(*move)
                if give_child:
                    yield move, child_board_state
                else:
                    yield move, None


        # else is needed as I used yield above not return
        else:
            # gather triplets of all legal moves as well as corresponding moves and scores
            moves_scores_children = []

            for move in board_state.generate_legal_moves():
                child_board_state = board_state.make_move(*move)
                # appropriate_depth = max(0, depth-2)
                appropriate_depth = max(0, depth-3)

                score, _ = self.minimax(
                    board_state=child_board_state,
                    depth=appropriate_depth,
                    variable_depth=False,
                    part_of_presort=True
                )
                if give_child:
                    moves_scores_children.append([score, move, child_board_state])
                else:
                    moves_scores_children.append([score, move, None])


            # sort by score
            moves_scores_children = sorted(
                moves_scores_children,
                key=lambda triplet: triplet[0],
                reverse=is_maximizer                
            )
            # use map to get rid of score
            moves_scores_children = map(lambda triplet: triplet[1:], moves_scores_children)

            # moves_scores_children = list(moves_scores_children)
            # moves_scores_children_printable = list(map(
            #     lambda x: (x[0], hash(x[1])),
            #     moves_scores_children
            # ))
            # print("Inspecting children:")
            # print(moves_scores_children_printable)

            yield from moves_scores_children
            # for move, child in moves_scores_children:
            #   # print(f"vanilla generate_move_child about to yield:  {(move, child)}")
            #     yield (move, child)

    def pseudo_base_case(self, board_state: Board_State, alpha, beta, part_of_presort: bool):
        # returns score: int, move: (V, V) | None
        # used then depth == 0 or game over

        is_over, _ = board_state.is_game_over_for_next_to_go()
        in_check = board_state.color_in_check()

        # base case has a secret extra recursive case
        if (self.variable_depth) and (not is_over) and (in_check):
            # print("Check extra depth search ")
            score, move = self.minimax(
                board_state=board_state,
                depth = self.additional_depth,
                alpha=alpha,
                beta=beta,
                variable_depth=False
            )
            return score, move, self.additional_depth
        else:
            if part_of_presort:
                self.static_evaluations_presort += 1
            else:
                self.static_evaluations_non_presort += 1
            return board_state.static_evaluation(), None, 0

    # @print_decorator
    def minimax(self, board_state: Board_State, depth, alpha=0-(ARBITRARILY_LARGE_VALUE+1), beta=ARBITRARILY_LARGE_VALUE+1, variable_depth: bool | None = None, part_of_presort=False, legal_moves_to_examine: Iterable | None = None, is_time_expired=None) -> tuple[int, tuple[Vector, Vector]]:

        # not sure why depth sometimes is a single length tuple containing an int
        # here is a quick fix
        if isinstance(depth, tuple):
            if len(depth) == 1:
                depth = depth[0]


                
        # if depth >= 1:
          # print(f"STARTED: minimax(board_state={hash(board_state)}, depth={depth})")
        # print(f"Finished: minimax(board_state={hash(board_state)}, depth={depth}) returned ({}, {})")
       


        
        # returns score, move
        if variable_depth is None:
            variable_depth = self.variable_depth
        
        # if self.cache_allowed and depth >= 1:
        if self.cache_allowed:
            cached_result = self.cache_manager.search_cache(board_state=board_state, depth=depth)
            # print(f"Checked cache  {cached_result}")
            if cached_result is not None:
                # if depth >= 1:
                  # print(f"Finished: minimax(board_state={hash(board_state)}, depth={depth}) returned ({cached_result['score']}, {cached_result['move']})")
                return cached_result["score"], cached_result["move"]

        # put code for minimax function here 
        # use self.color_maximizer_key and board_state.next_to_go to get is maximizer

        # call base case:
        over, _ = board_state.is_game_over_for_next_to_go()
        if depth == 0 or over:
            best_score, best_move, final_depth = self.pseudo_base_case(
                board_state=board_state,
                alpha=alpha,
                beta=beta,
                part_of_presort=part_of_presort
            )
            # if best_move is not None:
            #     best_child_board_state = board_state.make_move(*best_move)
            # else:
            #     best_child_board_state = None
            
            # print("Base case, trying to add to cache")
            if self.cache_allowed:
                self.cache_manager.add_to_cache(
                    board_state=board_state,
                    depth=final_depth,
                    score=best_score,
                    move=best_move
                )

            # print(f"Base Case:   minimax(board_state={board_state!r}, depth={depth}) returned: score={score}, move={move!r}")

            # if depth >= 1:
              # print(f"Finished: minimax(board_state={hash(board_state)}, depth={depth}) returned ({best_score}, {best_move})")
            return best_score, best_move

        best_move: tuple[Vector] | None = None
        # best_child_board_state: Board_State | None = None
        best_score: int | None = None

        is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)
        if legal_moves_to_examine is None:
            legal_moves_to_examine = self.generate_move_child(board_state=board_state, depth=depth, is_maximizer=is_maximizer)


        if is_maximizer:
            best_score = 0-(ARBITRARILY_LARGE_VALUE+1)

            # print("VANILLA: list legal_moves_to_examine:")
            # print(list(legal_moves_to_examine))
            for move, child_board_state in legal_moves_to_examine:
                if is_time_expired is not None:
                    # print(f"Minimax function:   is_time_expired()  -->  {is_time_expired()}")
                    if is_time_expired():
                        raise TimeOutError()

                if child_board_state is None:
                    child_board_state = board_state.make_move(*move)
                # print(f"testing move  {move!r}")
                score, _ = self.minimax(
                    board_state=child_board_state,
                    depth=depth-1,
                    alpha=alpha,
                    beta=beta,
                    is_time_expired=is_time_expired,
                )
                # if depth == 2:
                #     print(f"Move {move} examined, its score was {score}")
                if score > best_score:
                    # print("best score beaten")
                    alpha = max(alpha, score)
                    
                    best_score = score

                    # print(f"updating best move to {best_move}")
                    best_move = move
                    # best_child_board_state = child_board_state
                
                # if beta <= alpha:
                #     if depth == 2:
                #         print(f"Pruning at a best score of {best_score}")
                #     break
                # if beta <= alpha and depth<2:
                #     break
                if beta <= alpha:
                    break
        else:
            best_score = ARBITRARILY_LARGE_VALUE+1

            for move, child_board_state in legal_moves_to_examine:
                if is_time_expired is not None:
                    # print(f"Minimax function:   is_time_expired()  -->  {is_time_expired()}")
                    if is_time_expired():
                        raise TimeOutError()

                if child_board_state is None:
                    child_board_state = board_state.make_move(*move)
                # print(f"testing move  {move!r}")
                score, _ = self.minimax(
                    board_state=child_board_state,
                    depth=depth-1,
                    alpha=alpha,
                    beta=beta,
                    is_time_expired=is_time_expired,
                )
                # if depth == 2:
                #     print(f"Move {move} examined, its score was {score}")
                if score < best_score:
                    # print("best score beaten")
                    beta = min(beta, score)

                    best_score = score

                    # print(f"updating best move to {best_move}")
                    best_move = move
                    # best_child_board_state = child_board_state
                
                # if beta <= alpha:
                #     if depth == 2:
                #         print(f"Pruning at a best score of {best_score}")
                #     break
                # if beta <= alpha and depth<2:
                #     break
                if beta <= alpha:
                    break


        # print("recursive case trying to add to cache")
        if self.cache_allowed:
            self.cache_manager.add_to_cache(
                board_state=board_state,
                depth=depth,
                score=best_score,
                move=best_move
            )

        # print(f"Recursive Case:   minimax(board_state={board_state!r}, depth={depth}) returned: score={score}, move={move!r}")
        # if depth >= 1:
          # print(f"Finished: minimax(board_state={hash(board_state)}, depth={depth}) returned ({best_score}, {best_move})")
        return best_score, best_move

    def validator(self, result, board_state: Board_State):
        try:
            assert len(result) == 2, "result should be of length 2 (score and move)"

            score, move = result
            assert isinstance(score, int), "score should be of type int"

            assert len(move) == 2, "move should be a length 2 array (position vector and movement vector)"
            assert all(isinstance(v, Vector) for v in move), "both elements in move should be of type vector"

            position_vector, move_vector = move
            resultant_vector = position_vector + move_vector

            assert all(v.in_board() for v in (position_vector, resultant_vector)), "both position vector and movement vector must be in board"

            assert move in board_state.generate_legal_moves(), "move must be in the board state legal move generator"

        except AssertionError as e:
            raise ValueError(e)
        # else:
        #   # print("Validator completed all checks")

    # def parallel_minimax(self, board_state, depth, *args, **kwargs):
    #     assert depth >= 2, "depth must be greater or equal to 2 to do parallelization"

    #     is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)
    #     moves_and_child_sorted = list(self.generate_move_child(
    #         board_state=board_state,
    #         depth=depth,
    #         is_maximizer=is_maximizer
    #     ))
    #     cores = multiprocessing.cpu_count()
    #     if cores > len(moves_and_child_sorted):
    #         cores = len(moves_and_child_sorted)

    #     # chop up array into sub arrays
    #     legal_move_sub_arrays = [[],]*cores

    #     # repeatedly add next best move to the end of the sub array
    #     i = 0
        
    #     while moves_and_child_sorted:
    #         legal_move_sub_arrays[i].append(
    #             moves_and_child_sorted.pop(0)
    #         )
    #         i = (i+1) % cores

    #     # reverse sub arrays so in order of best to worst
    #     legal_move_sub_arrays = list(map(
    #         reversed,
    #         legal_move_sub_arrays
    #     ))

    #     # use these legal moves to do many simultaneous minimax operations
    #     job = Minimax_Sub_Job(
    #         move_engine=self,
    #         board_state=board_state,
    #         depth=depth,
    #         args=args,
    #         kwargs=kwargs
    #     )

    #     with multiprocessing.Pool(cores) as pool:
    #         minimax_sub_job_results = pool.map(
    #             func = job,
    #             iterable=legal_move_sub_arrays
    #         )

    #     best_move = None
    #     if is_maximizer:
    #         best_score = 0-(ARBITRARILY_LARGE_VALUE +1)
    #     else:
    #         best_score = ARBITRARILY_LARGE_VALUE +1

        
    #     # select best move
    #     for result in minimax_sub_job_results:
    #         score, move = result
            
    #         if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
    #             best_score = score
    #             best_move = move

    #     return best_score, best_move



    # def minimax_first_call(self, board_state: Board_State, depth, is_time_expired = lambda: False, *args, **kwargs):
    def minimax_first_call(self, board_state: Board_State, depth, *args, **kwargs):
        # if self.parallelize and depth >=2:
        #     if self.cache_allowed:
        #         with self.cache_manager:
        #             result = self.parallel_minimax(board_state=board_state, depth=depth, *args, **kwargs)
        #     else:
        #         result = self.parallel_minimax(board_state=board_state, depth=depth, *args, **kwargs)

        # else:
        #     if self.cache_allowed:
        #         with self.cache_manager:
        #             result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)
        #     else:
        #         result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)

        # if self.use_validator:
        #     self.validator(result=result, board_state=board_state)
        # return result

        if self.cache_allowed:
            with self.cache_manager:
                result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)
        else:
            result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)

        if self.use_validator:
            self.validator(result=result, board_state=board_state)

        return result

    def __call__(self, *args, **kwargs):
        return self.minimax_first_call(*args, **kwargs)

    def benchmark_minimax(self, *args, **kwargs):
        def reset_counts():
            self.static_evaluations_non_presort = 0
            self.static_evaluations_presort = 0

        reset_counts()

        start_time = perf_counter()
        result = self.minimax_first_call(*args, **kwargs)
        end_time = perf_counter()

        time_taken = end_time - start_time

        benchmark_data = {
            "time_duration": time_taken, 
            "evals_presort": self.static_evaluations_presort,
            "evals_non_presort": self.static_evaluations_non_presort
        }

        reset_counts()

        return result, benchmark_data
