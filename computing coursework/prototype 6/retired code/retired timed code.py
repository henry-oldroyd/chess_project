
    # def generate_move_child_in_parallel(self, board_state: Board_State, depth: int, is_maximizer, give_child=True, is_time_expired=lambda: False):
    #     if is_time_expired():
    #         raise TimeOutError()
    #     # print("CALL TIMED generate_move_child_in_parallel")
    #     # print("generate_move_child_in_parallel called")

    #     explore_depth = max(depth-3, 0)

    #     if (not self.cache_allowed):
    #         yield from super().generate_move_child(
    #             board_state=board_state,
    #             depth=depth,
    #             is_maximizer=is_maximizer,
    #             give_child=give_child,
    #             is_time_expired=is_time_expired,
    #         )
    #     elif (self.parallel) or (explore_depth < 1):
    #         with self.cache_manager:
    #             yield from super().generate_move_child(
    #                 board_state=board_state,
    #                 depth=depth,
    #                 is_maximizer=is_maximizer,
    #                 give_child=give_child,
    #                 is_time_expired=is_time_expired,
    #             )
    #     else:
    #         #   # print("getting legal moves")
    #         legal_moves = list(board_state.generate_legal_moves())

    #         if is_time_expired():
    #             raise TimeOutError()

    #         # print("setting up job")
    #         basic_move_engine = Move_Engine(
    #             cache_allowed=True,
    #             cache_manager=self.cache_manager,
    #             presort_moves=True,
    #             additional_depth=0
    #         )

    #         job = Timed_Presort_Moves_Sub_Job(
    #             depth=explore_depth,
    #             board_state=board_state,
    #             move_engine=basic_move_engine,
    #             cache_manager=self.cache_manager,
    #             max_time=self.max_time,
    #         )

    #         # print("generate_move_child_in_parallel: Using multiprocessing pool")
    #         try:
    #             with multiprocessing.Pool(self.workers) as pool:
    #                 moves_and_scores = pool.map(
    #                     func=job,
    #                     iterable=legal_moves
    #                 )
    #                 pool.close()
    #                 pool.join()
    #         except TimeOutError:
    #             # anticipated
    #             raise
            
    #         if is_time_expired():
    #             raise TimeOutError()
    #         # print("generate_move_child_in_parallel: finished with multiprocessing pool")

    #         # sort by score
    #         moves_and_scores = sorted(
    #             moves_and_scores,
    #             key=lambda triplet: triplet[0],
    #             reverse=is_maximizer
    #         )
    #         # use map to get rid of score

    #         def move_and_blank_child(score_and_move):
    #             _, move = score_and_move
    #             return (move, None)

    #         moves_scores_children = map(move_and_blank_child, moves_and_scores)

    #         # print("children sorted by score")

    #         yield from moves_scores_children


    # def parallel_minimax(self, board_state, depth, cache_allowed, cache_manager, *args, **kwargs):
    #     # print("CALL TIMED parallel_minimax")
    #     # print("Parallel minimax called")

    #     # assert isinstance(depth, int)

    #     # assert depth >= 2, "depth must be greater or equal to 2 to do parallelization"

    #     is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)

    #     # print("started getting moves_and_child_sorted")
    #     # print("getting legal moves, presorted")

    #     if self.parallel:
    #         moves_sorted = list(self.generate_move_child_in_parallel(
    #             board_state=board_state,
    #             depth=depth,
    #             is_maximizer=is_maximizer,
    #             give_child=False
    #         ))
    #     else:
    #         moves_sorted = list(self.generate_move_child(
    #             board_state=board_state,
    #             depth=depth,
    #             is_maximizer=is_maximizer,
    #             give_child=False
    #         ))

    #     # print("finished getting moves_and_child_sorted")
    #     # print("moves_sorted: ")
    #     # print(moves_sorted)

    #     legal_move_sub_arrays = self.break_up_legal_moves_to_segments(
    #         legal_moves=moves_sorted,
    #         number_sub_arrays=self.workers
    #     )
        
    #     # print("legal moves sub arrays generated")

    #     # print("Printing legal moves sub arrays")
    #     # print(legal_move_sub_arrays)

    #     # print("Defining job for workers")
    #     # use these legal moves to do many simultaneous minimax operations
    #     job = Timed_Minimax_Sub_Job(
    #         # move_engine=self,
    #         move_engine=Move_Engine(
    #             cache_manager=cache_manager,
    #             cache_allowed=cache_allowed,

    #             # is this the miracle fix?
    #             additional_depth=self.additional_depth,

    #         ),
    #         board_state=board_state,
    #         depth=depth,
    #         cache_allowed=cache_allowed,
    #         cache_manager=cache_manager,
    #         args=args,
    #         kwargs=kwargs,
    #         max_time=self.max_time,
    #     )
    #     # job = Minimax_Sub_Job(*(None,)*7)

    #     # print(f"dill.pickles(job)    -->    {dill.pickles(job)}")

    #     # assert dill.pickles(job)
    #     # assert dill.pickles(legal_move_sub_arrays)

    #     # print(f"Using pool to complete jobs in parallel (pool size = {cores})")

    #     # print("parallel_minimax: Using multiprocessing pool")
    #     try:
    #         with multiprocessing.Pool(self.workers) as pool:
    #             minimax_sub_job_results = pool.map(
    #                 func=job,
    #                 iterable=legal_move_sub_arrays
    #             )
    #             pool.close()
    #             pool.join()
    #     except TimeOutError:
    #         # error anticipated hear
    #         raise

    #     # print("parallel_minimax: multiprocessing finished")

    #     best_move = None
    #     if is_maximizer:
    #         best_score = 0-(ARBITRARILY_LARGE_VALUE + 1)
    #     else:
    #         best_score = ARBITRARILY_LARGE_VALUE + 1

    #     # select best move
    #     for result in minimax_sub_job_results:
    #         score, move = result

    #         if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
    #             best_score = score
    #             best_move = move

    #     # print("finished getting best outcome")

    #     return best_score, best_move


# class Timed_Minimax_Sub_Job(Minimax_Sub_Job):
#     def __init__(self, move_engine: Move_Engine, board_state: Board_State, depth, cache_allowed, cache_manager, args, kwargs, max_time) -> None:
#         # print("INIT  Timed_Minimax_Sub_Job", flush=True)
#         super().__init__(move_engine, board_state, depth, cache_allowed, cache_manager, args, kwargs)
#         self.max_time = max_time

#     def is_time_expired(self):
#         return perf_counter() >= self.max_time

#     def __call__(self, legal_moves_sub_array):
#         # return self.move_engine.minimax_first_call(
#         return self.move_engine.minimax_first_call_parallel(
#             board_state=self.board_state,
#             depth=self.depth,
#             legal_moves_to_examine=legal_moves_sub_array,
#             is_time_expired = self.is_time_expired,
#             *self.args,
#             **self.kwargs
#         )
#         # print(f"Timed_Minimax_Sub_Job call:   self.is_time_expired()   -->   {self.is_time_expired()}", flush=True)
#         # sys.stdout.flush()
#         # # raise Exception("Testing if this code is run Timed_Minimax_Sub_Job")
#         # if self.is_time_expired():
#         #     # is_maximizer = self.move_engine.color_maximizer_key[self.board_state.next_to_go]
#         #     # worst_score_multiplier = (-1) if is_maximizer else 1
#         #     # worst_score = (ARBITRARILY_LARGE_VALUE + 1) * worst_score_multiplier
#         #     # return worst_score, None
#         #     raise TimeOutError("Time out error in minimax sub job")
#         # else:
#         #     return super().__call__(legal_moves_sub_array)


# class Timed_Presort_Moves_Sub_Job(Presort_Moves_Sub_Job):
#     def __init__(self, depth, board_state: Board_State, move_engine: Move_Engine, cache_manager, max_time) -> None:
#         # print("INIT  Timed_Presort_Moves_Sub_Job ", flush=True)
#         super().__init__(depth, board_state, move_engine, cache_manager)
#         self.max_time = max_time

#     # def is_time_expired(self):
#     #     return perf_counter() >= self.max_time


#     def __call__(self, move):
#         child = self.board_state.make_move(*move)
#         child_score, _ = self.move_engine.minimax_first_call(
#             board_state = child,
#             depth = self.depth,
#             # is_time_expired=self.is_time_expired,
#             max_time=self.max_time,
#         )
#         return (child_score, move)

#         # # print("Closing cache")
#         # return (child_score, move)
#         # print(f"Timed_Presort_Moves_Sub_Job call:   self.is_time_expired()   -->   {self.is_time_expired()}", flush=True)
#         # sys.stdout.flush()
#         # # raise Exception("Testing if this code is run Timed_Minimax_Sub_Job")
#         # if self.is_time_expired():
#         #     # is_maximizer = self.move_engine.color_maximizer_key[self.board_state.next_to_go]
#         #     # is_child_maximizer = not is_maximizer
#         #     # worst_score_multiplier = (-1) if is_child_maximizer else 1
#         #     # worst_score = (ARBITRARILY_LARGE_VALUE + 1) * worst_score_multiplier
#         #     # return worst_score, None
#         #     raise TimeOutError("Time out error in presort")
#         # else:
#         #     return super().__call__(legal_moves_sub_array)
