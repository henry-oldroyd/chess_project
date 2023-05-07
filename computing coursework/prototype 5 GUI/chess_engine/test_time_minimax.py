# import unittest
# from random import choice as random_choice
# import multiprocessing

# from board_state import Board_State
# # print("Importing move engine")
# from minimax import Move_Engine, JSON_cache, JSON_cache_manual_save
# # print("Move engine imported")

# class Random_Mutant_Generator():
#     def __call__(self, moves: int, seed_board_state=None):
#         if seed_board_state is None:
#             seed_board_state = Board_State()

#         board_state = seed_board_state

#         for _ in range(moves):
#             random_move = random_choice(list(board_state.generate_legal_moves()))
#             board_state = board_state.make_move(*random_move)
            
#         return board_state
#     # def __hash__(self) -> int:
#     #     hash("This is a general random mutant generator object with no unique features")

# class Multitasker():
#     def __call__(self, job, argument_iterable):
#         # print(f"job --> {job!r}")

#         cores = multiprocessing.cpu_count()
#         with multiprocessing.Pool(cores) as pool:
#             # yield from pool.map(
#             return pool.map(
#                 func=job,
#                 iterable=argument_iterable
#             )
#     # def __hash__(self) -> int:
#     #     hash("This is a general multitasker object that has no unique features")


# class Check_Benchmarks():
#     def __call__(self, game_engine_arguments, good_move_engine: Move_Engine, bad_move_engine: Move_Engine, check_time: bool, check_evals: bool, check_move = True):
#         good_result, good_benchmark_data = good_move_engine.benchmark_minimax(**game_engine_arguments)
#         good_score, _ = good_result

#         bad_result, bad_benchmark_data = bad_move_engine.benchmark_minimax(**game_engine_arguments)
#         bad_score, _ = bad_result
        
#         if check_move:
#             assert good_score == bad_score, f"The minimax calls returned moves of different values:   good_bot={good_score},   bad_score={bad_score}"
        
#         if check_time:
#             good_time, bad_time = good_benchmark_data["time_duration"], bad_benchmark_data["time_duration"]
#             assert good_time < bad_time, "\n" + f"Good bot didn't take less time, good bot took {good_time} and bad bot took {bad_time}"
            

#         if check_evals:
#             good_non_presort_evals, good_presort_evals = good_benchmark_data["evals_non_presort"], good_benchmark_data["evals_presort"]
#             good_total_evals = good_non_presort_evals + good_presort_evals

#             bad_non_presort_evals, bad_presort_evals = bad_benchmark_data["evals_non_presort"], bad_benchmark_data["evals_presort"]
#             bad_total_evals = bad_non_presort_evals + bad_presort_evals

#             msg = f"\nGood bot didn't preform less static evaluation:    good_bot={good_non_presort_evals}+{good_presort_evals}    bad_bot={bad_non_presort_evals}+{bad_presort_evals}"
                
#             assert good_total_evals < bad_total_evals, msg
#     # def __hash__(self) -> int:
#     #     return hash("This is a generic check benchmarks object with no variation between instances")

# class Job_test_cache_vs_normal:
#     def __init__(self, moves, check_time, cache_manager, depth) -> None:
#         self.moves = moves
#         self.check_time = check_time
#         self.cache_manager = cache_manager
#         self.depth = depth

#     def __call__(self, _):
#         board_state = Random_Mutant_Generator()(moves=self.moves)

#         try:
#             Check_Benchmarks()(
#                 game_engine_arguments={
#                     "board_state": board_state,
#                     "depth": self.depth
#                 },
#                 good_move_engine=Move_Engine(variable_depth=False, use_validator=True, presort_moves=True, cache_allowed=True, cache_manager=self.cache_manager),
#                 bad_move_engine=Move_Engine(variable_depth=False, use_validator=True, presort_moves=True, cache_allowed=False, cache_manager=self.cache_manager),
#                 check_time=self.check_time,
#                 check_evals=True,
#                 check_move=False
#             )
#         except AssertionError as e:
#             # self.test_case.fail(msg=str(e))
#             return False, str(e)
#         else:
#             return True, None

#     # def __hash__(self) -> int:
#     #     return hash("unique singleton job object for test test_cache_vs_normal_depth_2")




# class Test_Case(unittest.TestCase):
    
#     @unittest.skip("temporarily broken be cache change")
#     def test_depth_2_presort_vs_normal(self):
#         try:
#             Check_Benchmarks()(
#                 game_engine_arguments={
#                     "board_state": Board_State(),
#                     "depth": 2
#                 },
#                 good_move_engine = Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, presort_moves=True),
#                 bad_move_engine = Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, presort_moves=False),
#                 check_time=True,
#                 check_evals=True
#             )
#         except AssertionError as e:
#             self.fail(msg=str(e))


#     @unittest.skip("temporarily broken be cache change")
#     def test_depth_3_presort_vs_normal(self):
#         try:
#             Check_Benchmarks()(
#                 game_engine_arguments={
#                     "board_state": Board_State(),
#                     "depth": 3
#                 },
#                 good_move_engine = Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, presort_moves=True),
#                 bad_move_engine = Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, presort_moves=False),
#                 check_time=True,
#                 check_evals=True
#             )
#         except AssertionError as e:
#             self.fail(msg=str(e))

#     def test_cache_vs_normal_depth_3(self):

#         trials = 16
#         pass_bar = 12
#         argument_iterable = (None,)*trials

#         cache_manager = JSON_cache_manual_save()

#         job = Job_test_cache_vs_normal(
#             moves=10,
#             check_time=True,
#             cache_manager=cache_manager,
#             depth=3
#         )

#         results = Multitasker()(
#             job=job,
#             argument_iterable=argument_iterable
#         )

#         # assume multitasker is return not yield so all threads now finished
#         cache_manager.save()

#         successes = sum(int(success) for success, _ in results)
#         if successes < pass_bar:
#             error_msgs = "\n\t".join(msg for success, msg in results if not success)
#             # error_msgs = "".join(msg for success, msg in results if not success)
#             self.fail(f"\n{successes}/{trials} were more efficient with cache (bar was {pass_bar}):\n{error_msgs}")

#         # for success, msg in results:
#         #     self.assertTrue(
#         #         success,
#         #         msg=msg
#         #     )



#     def test_cache_vs_normal_depth_2_less_static_evals(self):
#         trials = 16
#         pass_bar = 12
#         argument_iterable = (None,)*trials
        
#         cache_manager = JSON_cache_manual_save()

#         job = Job_test_cache_vs_normal(
#             moves = 10,
#             check_time = False,
#             cache_manager = cache_manager,
#             depth = 2
#         )


#         results = Multitasker()(
#             job=job,
#             argument_iterable = argument_iterable
#         )        

#         # assume multitasker is return not yield so all threads now finished
#         cache_manager.save()
        
#         successes = sum(int(success) for success, _ in results)
#         if successes < pass_bar:
#             error_msgs = "\n\t".join(msg for success, msg in results if not success)
#             # error_msgs = "".join(msg for success, msg in results if not success)
#             self.fail(f"\n{successes}/{trials} were more efficient with cache (bar was {pass_bar}):\n{error_msgs}")

#         # for success, msg in results:
#         #     self.assertTrue(
#         #         success,
#         #         msg=msg
#         #     )

#     @unittest.skip("feature not working")
#     def test_depth_2_parallel_vs_normal(self):
#         try:
#             Check_Benchmarks()(
#                 game_engine_arguments={
#                     "board_state": Board_State(),
#                     "depth": 2
#                 },
#                 good_move_engine=Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, parallelize=True),
#                 bad_move_engine=Move_Engine(variable_depth=False, cache_allowed=False, use_validator=True, parallelize=False),
#                 check_time=True,
#                 check_evals=True
#             )
#         except AssertionError as e:
#             self.fail(msg=str(e))



# if __name__ == "__main__":
#     unittest.main()
#     # input("Continue:  ")
#     # Test_Case().test_cache_vs_normal_depth_2_less_static_evals()