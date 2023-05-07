import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.pool import QueuePool

from marshmallow import Schema, fields, pre_load, pre_dump, post_load, post_dump

import os
# import sys
import multiprocessing
from time import perf_counter

from .minimax import Move_Engine
from .cache_managers import RAM_cache
from .board_state import Board_State
from .vector import Vector
from .assorted import ARBITRARILY_LARGE_VALUE, TimeOutError



# import time
def get_cores():
    return multiprocessing.cpu_count()
    # return multiprocessing.cpu_count()//2

DB_path = os.path.join(os.getcwd(), 'database.db')

# engine = sqla.create_engine(
#     'sqlite:///' + DB_path,
#     echo=False,
#     future=True,
#     connect_args={'check_same_thread': False},
# )


# try:
#     engine = sqla.create_engine(
#         'sqlite:///' + DB_path,
#         echo=False,
#         pool_size=multiprocessing.cpu_count()
#     )
# except TypeError:
#     engine = sqla.create_engine(
#         'sqlite:///' + DB_path,
#         echo=False,
#         poolclass = QueuePool
#     )
    

Base = declarative_base()


class Minimax_Cache_Item(Base):
    __tablename__ = "Minimax_Cache"
    
    primary_key = sqla.Column(sqla.Integer, primary_key=True)

    board_state_hash = sqla.Column(sqla.String())
    depth = sqla.Column(sqla.INT())
    score = sqla.Column(sqla.INT())
    # 4 character move string encoded by the 4 digits of the from and movement vectors
    move = sqla.Column(sqla.String)

    def __init__(self, board_state_hash: str, depth, move: str, score: int):
        # hash board state
        self.board_state_hash = board_state_hash
        self.depth = depth
        self.move = move
        self.score = score

    def __repr__(self) -> str:
        return f"Minimax_Cache_Item(board_state_hash='{self.board_state_hash}', depth={self.depth}, move='{self.move}', score={self.score})"


class Vector_Schema(Schema):
    i = fields.Integer(required=True)
    j = fields.Integer(required=True)

    @pre_load
    def pre_load(self, vector, **kwargs):
        data = {}
        data["i"] = vector.i
        data["j"] = vector.j
        return data

    @post_dump
    def post_dump(self, data, **kwargs):
        return Vector(
            i=data["i"],
            j=data["j"] 
        )


class Move_Schema(Schema):
    from_vector = fields.Nested(Vector_Schema, required=True)
    movement_vector = fields.Nested(Vector_Schema, required=True)

    @pre_load
    def pre_load(self, vector_tuple, **kwargs):
        from_vector, movement_vector = vector_tuple
        data = {}
        data["from_vector"] = from_vector
        data["movement_vector"] = movement_vector
        return data

    @post_dump
    def post_dump(self, data, **kwargs):
        return (
            data["from_vector"],
            data["movement_vector"]
        )

def get_deserialized_move(move):
    # assert len(move) == 4
    # if move == "None":
    if move == None:
        return None

    move = move[1:-1]
    move = move.split(", ")
    from_vector = Vector(
        i=move[0],
        j=move[1]
    )
    movement_vector = Vector(
        i=move[2],
        j=move[3]
    )
    return dict(
        from_vector = from_vector, 
        movement_vector = movement_vector
    )
    

def get_serialised_move(move):
    # assert len(f"{move['from_vector']['i']}{move['from_vector']['j']}{move['movement_vector']['i']}{move['movement_vector']['j']}") == 4
    # return f"{move['from_vector']['i']}{move['from_vector']['j']}{move['movement_vector']['i']}{move['movement_vector']['j']}"
    
    if move is None:
        # return "None"
        return None

    return str((
        move["from_vector"]["i"],
        move["from_vector"]["j"],
        move["movement_vector"]["i"],
        move["movement_vector"]["j"],
    ))

class Minimax_Cache_Item_Schema(Schema):
    board_state_hash = fields.String(required=True, load_only=True)
    depth = fields.Integer(required=True)
    score = fields.Integer(required=True)
    move = fields.Nested(Move_Schema, required=True, allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        # assert isinstance(data["depth"], int)
        # assert isinstance(data["score"], int)
        # print(f"post_load: serializing move form {data['move']} to {get_serialised_move(data['move'])}")

        return Minimax_Cache_Item(
            board_state_hash = data["board_state_hash"],
            depth  = data["depth"],
            score = data["score"],
            move = get_serialised_move(
                data["move"]
            )
        )

    @pre_dump
    def pre_dump(self, minimax_cache_item: Minimax_Cache_Item, **kwargs):
        # print(f"pre_dump: deserializing move form {minimax_cache_item.move} to {get_deserialized_move(minimax_cache_item.move)}")
        return dict(
            depth = minimax_cache_item.depth,
            move = get_deserialized_move(
                minimax_cache_item.move
            ),
            score = minimax_cache_item.score
        )


persistent_DB_engine = sqla.create_engine(
    'sqlite:///' + DB_path,
    echo=False,
    poolclass = QueuePool
)

volatile_RAM_engine = sqla.create_engine(
    "sqlite:///:memory:",
    echo=False,
    poolclass = QueuePool
)



minimax_cache_item_schema = Minimax_Cache_Item_Schema()

Base.metadata.create_all(persistent_DB_engine, checkfirst=True)
Base.metadata.create_all(volatile_RAM_engine, checkfirst=True)

sqla.schema.Index("board_state_hash", Minimax_Cache_Item.board_state_hash)


class DB_Cache():
    def __init__(self, min_DB_depth = 1):
        self._RAM_cache = None
        self._DB_session = None
        self.min_DB_depth = min_DB_depth
        self.engaged = False

        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0

    def __enter__(self, *args, **kwargs):
        # assert all(e is None for e in (self._RAM_cache, self._DB_session))
        assert not self.engaged, "Must not be engaged (entered) already to enter"
        self.engaged = True

        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0

        # this allows for the cache manager to be entered multiple times on accident without making multiple sessions 
        # self._RAM_cache = RAM_cache()
        self._persistent_DB_session = scoped_session(sessionmaker(bind=persistent_DB_engine))
        self._volatile_RAM_session = scoped_session(sessionmaker(bind=volatile_RAM_engine))

        


    def __exit__(self, *args, **kwargs):
        assert self.engaged, "Must be engaged (entered) to exit"
        self.engaged = False

        self._persistent_DB_session.close()
        self._persistent_DB_session = None

        self._volatile_RAM_session.close()
        self._volatile_RAM_session = None

        # print(f"Cache session lasted {round(self.time_delta_DB, 2)}+{round(self.time_delta_schemas, 2)} sec (DB + schema time): {self.checks_to_cache} checks made, {self.retrieved_item} items retrieved, {self.items_added} items added")

        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0


    def _search_DB_cache(self, session, board_state, depth):
        board_state_hash = str(hash(board_state))

        start = perf_counter()

        result = session.query(Minimax_Cache_Item)\
            .where(
                Minimax_Cache_Item.board_state_hash == board_state_hash
            )\
            .where(
                Minimax_Cache_Item.depth >= depth
            )\
            .first()

        stop = perf_counter()
        self.time_delta_schemas += stop - start


        if result is None:
            return None


        start = perf_counter()

        result = minimax_cache_item_schema.dump(result)

        stop = perf_counter()
        self.time_delta_schemas += stop - start

        return result


    def _add_to_DB_cache(self, session, board_state: Board_State, score, depth, move):
        start = perf_counter()
    
        # print("adding item to database cache")
        board_state_hash = str(hash(board_state))

        # if depth >= 2:
        #     print(f"Adding item {board_state_hash} at depth {depth} to cache")


        new_item = minimax_cache_item_schema.load(
                dict(
                    board_state_hash = board_state_hash,
                    score = score,
                    depth = depth,
                    move = move
                )
            )

        stop = perf_counter()
        self.time_delta_schemas += stop - start

        start = perf_counter()

        session.query(Minimax_Cache_Item)\
            .where(
                    Minimax_Cache_Item.board_state_hash == board_state_hash
            )\
            .delete()

        # print(f"move   -->   {move!r}")

        # print(f"New item:   {new_item!r}")

        session.add(new_item)
        session.commit()

        stop = perf_counter()
        self.time_delta_DB += stop - start


    def search_cache(self, board_state: Board_State, depth):
        assert self.engaged, "Context manager must be used"
        
        self.checks_to_cache += 1

        # not sure why depth sometimes is a single length tuple containing an int
        # here is a quick fix
        if isinstance(depth, tuple):
            if len(depth) == 1:
                depth = depth[0]

        # assert isinstance(depth, int)

        # print(f"(depth, self.min_DB_depth)     -->     {(depth, self.min_DB_depth)}")        

        if depth < self.min_DB_depth:
            session = self._volatile_RAM_session
            # return self._RAM_cache.search_cache(board_state=board_state, depth=depth)
        else:
            session = self._persistent_DB_session
            # return self._search_DB_cache(board_state=board_state, depth=depth)

        result = self._search_DB_cache(session=session, board_state=board_state, depth=depth)

        if result is not None:
            self.retrieved_item += 1

        return result
        

    def add_to_cache(self, board_state: Board_State, score, depth, move):
        assert self.engaged, "Context manager must be used"
        # assert isinstance(depth, int)

        if depth < self.min_DB_depth:
            session = self._volatile_RAM_session
            # self._RAM_cache.add_to_cache(board_state=board_state, score=score, depth=depth, move=move)
        else:
            session = self._persistent_DB_session
            # self._add_to_DB_cache(board_state=board_state, score=score, depth=depth, move=move)

        self._add_to_DB_cache(session=session, board_state=board_state, score=score, depth=depth, move=move)


        self.items_added += 1


class Minimax_Sub_Job:
    def __init__(self, move_engine, board_state, depth, cache_allowed, cache_manager, args, kwargs) -> None:
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

        self.args = args
        self.kwargs = kwargs

    def __call__(self, legal_moves_sub_array):
        # print(f"running minimax job with legal moves sub array: (hash={hash(str(legal_moves_sub_array))})")
      # print(f"STARTING sub job on moves segment:   {hash(str(legal_moves_sub_array))}")
        # print(legal_moves_sub_array)

        result = self.move_engine.minimax_first_call(
            board_state=self.board_state,
            depth=self.depth,
            legal_moves_to_examine=legal_moves_sub_array,
            *self.args,
            **self.kwargs
        )

      # print(f"FINISHING sub job on moves segment:   {hash(str(legal_moves_sub_array))}")
        # print(f"Minimax sub job finished (hash={hash(str(legal_moves_sub_array))})")
        return result



class Presort_Moves_Sub_Job:
    def __init__(self, depth, board_state: Board_State, move_engine: Move_Engine, cache_manager) -> None:
        self.depth = depth
        self.board_state = board_state
        self.move_engine = move_engine
        self.cache_manager = cache_manager
    def __call__(self, move):
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

        child = self.board_state.make_move(*move)
        child_score, _ = self.move_engine.minimax_first_call(
            board_state = child,
            depth = self.depth,
        )
        # print("Closing cache")
        return (child_score, move)


class Parallel_Move_Engine(Move_Engine):
    def __init__(self, cache_manager: RAM_cache | None = DB_Cache(), cache_allowed: bool = True, parallel=True, min_parallel_depth=2, workers=get_cores(), **kwargs) -> None:
        self.parallel = parallel
        if parallel and cache_allowed:
            assert isinstance(cache_manager, DB_Cache), "Only DB cache an be used in parallel"
        self.min_parallel_depth = min_parallel_depth
        self.workers = workers

        super().__init__(cache_manager = cache_manager, cache_allowed = cache_allowed, **kwargs)

    def should_use_parallel(self, board_state: Board_State, depth):
        return depth >= self.min_parallel_depth and self.parallel

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


    def generate_move_child_in_parallel(self, board_state: Board_State, depth: int, is_maximizer, give_child=True):
        # print("generate_move_child_in_parallel called")

        explore_depth = max(depth-3, 0)

        if (not self.cache_allowed):
            yield from super().generate_move_child(
                board_state = board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=give_child
            )
        elif (self.parallel) or (explore_depth < 1):
            with self.cache_manager:
                yield from super().generate_move_child(
                    board_state = board_state,
                    depth=depth,
                    is_maximizer=is_maximizer,
                    give_child=give_child
                )
        else:
        #   # print("getting legal moves")
            legal_moves = list(board_state.generate_legal_moves())

            # print("setting up job")
            basic_move_engine = Move_Engine(
                cache_allowed=True, 
                cache_manager=self.cache_manager,
                presort_moves=True,
                additional_depth=0
            )



            job = Presort_Moves_Sub_Job(
                depth = explore_depth,
                board_state=board_state,
                move_engine=basic_move_engine,
                cache_manager = self.cache_manager
            )

            # print("generate_move_child_in_parallel: Using multiprocessing pool")
            with multiprocessing.Pool(self.workers) as pool:
                moves_and_scores = pool.map(
                    func=job,
                    iterable=legal_moves
                )
            # print("generate_move_child_in_parallel: finished with multiprocessing pool")

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


    def parallel_minimax(self, board_state, depth, cache_allowed, cache_manager, *args, **kwargs):
        # print("Parallel minimax called")

        # assert isinstance(depth, int)

        # assert depth >= 2, "depth must be greater or equal to 2 to do parallelization"

        is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)

        # print("started getting moves_and_child_sorted")
        # print("getting legal moves, presorted")

        if self.parallel:
            moves_sorted = list(self.generate_move_child_in_parallel(
                board_state=board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=False
            ))
        else:
            moves_sorted = list(self.generate_move_child(
                board_state=board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=False
            ))


        # print("finished getting moves_and_child_sorted")
        # print("moves_sorted: ")
        # print(moves_sorted)
        

        legal_move_sub_arrays = self.break_up_legal_moves_to_segments(
            legal_moves=moves_sorted,
            number_sub_arrays=self.workers
        )


        # print("legal moves sub arrays generated")

        # print("Printing legal moves sub arrays")
        # print(legal_move_sub_arrays)

        # print("Defining job for workers")
        # use these legal moves to do many simultaneous minimax operations
        job = Minimax_Sub_Job(
            # move_engine=self,
            move_engine=Move_Engine(
                cache_manager=cache_manager,
                cache_allowed=cache_allowed, 

            

                # is this the miracle fix?
                additional_depth= self.additional_depth,
            
            
            
            ),
            board_state=board_state,
            depth=depth,
            cache_allowed=cache_allowed,
            cache_manager=cache_manager,
            args=args,
            kwargs=kwargs,
        )
        # job = Minimax_Sub_Job(*(None,)*7)
        
        # print(f"dill.pickles(job)    -->    {dill.pickles(job)}")

        # assert dill.pickles(job)
        # assert dill.pickles(legal_move_sub_arrays)

        # print(f"Using pool to complete jobs in parallel (pool size = {cores})")

        # print("parallel_minimax: Using multiprocessing pool")
        with multiprocessing.Pool(self.workers) as pool:
            minimax_sub_job_results = pool.map(
                func = job,
                iterable=legal_move_sub_arrays
            )

        # print("parallel_minimax: multiprocessing finished")

        best_move = None
        if is_maximizer:
            best_score = 0-(ARBITRARILY_LARGE_VALUE +1)
        else:
            best_score = ARBITRARILY_LARGE_VALUE +1

        # select best move
        for result in minimax_sub_job_results:
            score, move = result

            if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
                best_score = score
                best_move = move


        # print("finished getting best outcome")

        return best_score, best_move


    def minimax_first_call_parallel(self, board_state: Board_State, depth, *args, **kwargs):
        # print(f"CALL   minimax_first_call_parallel")
        # print(f"CALL minimax_first_call_parallel(self, board_state={hash(board_state)}, depth={depth}, *args, **kwargs)")
        # assert isinstance(depth, int)
        if self.cache_allowed:
            with self.cache_manager:
                result = self.cache_manager.search_cache(
                    board_state=board_state,
                    depth=depth
                )
            if result is not None:
                # print("no call needed as cache is sufficient")
                return result["score"], result["move"]

        should_use_parallel = self.should_use_parallel(board_state=board_state, depth=depth)
        # print(f"minimax_first_call_parallel  Should use parallel:   {should_use_parallel}")
        if should_use_parallel:
            # print("making parallel call:")
            result = self.parallel_minimax(
                board_state=board_state,
                depth=depth,
                cache_allowed=self.cache_allowed,
                cache_manager=self.cache_manager,
                *args,
                **kwargs
            )

        else:
            # print("making linear call:")
            if self.cache_allowed:
                with self.cache_manager:
                    result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)
            else:
                result = self.minimax(board_state=board_state, depth=depth, *args, **kwargs)

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
    



    def should_use_parallel(self, board_state: Board_State, depth):

        # if not self.parallel:
        #     return False

        # if depth >= 3:
        #     print("depth greater than or equal to 3 so returning true")
        #     return True
        
        # def absolute(x): return x if x >=0 else -x

        # few_pieces_left = board_state.number_total_pieces <= 24
        # many_moves_made = board_state.moves_counter >= 22
        # significant_advantage = absolute(board_state.static_evaluation()) >= 1200
        # check_encountered = board_state.check_encountered

        # late_game_score = sum(map(
        #     int,
        #     (few_pieces_left, many_moves_made, significant_advantage, check_encountered),
        # ))

        # if late_game_score >= 2:
        #     # print("Late game score greater of equal to 2 so returning true")
        #     return True


        # if late_game_score == 1:
        #     estimated_total_depth = depth + self.variable_depth
        # else:
        #     estimated_total_depth = depth

        # num_legal_moves = board_state.number_legal_moves
        # # 24 is the number of legal moves at the start of the game
        # # low_moves = num_legal_moves <= 24
        # # moderate_moves = 24 < num_legal_moves <= 40
        # # many_moves = 40 < num_legal_moves

        # # print(f"Late game score: {late_game_score}:  (few_pieces_left, many_moves_made, significant_advantage, check_encountered)  -->  {(few_pieces_left, many_moves_made, significant_advantage, check_encountered)}")


        # # if estimated depth is low then don't parallelize unless there are loads of legal moves
        # if estimated_total_depth == 2:
        #     # print(f"num_legal_moves >= 40   -->   {num_legal_moves >= 40}")
        #     return num_legal_moves >= 40



        # # if the estimated depth is moderate then parallelize if there are not many legal moves
        # if estimated_total_depth == 3:
        #     if depth == 3:
        #         # print("depth == 3 so returning true")
        #         return True

        #     # print(f"num_legal_moves <= 20   -->   {num_legal_moves <= 20}")
        #     return num_legal_moves >= 20
            

        # return False



        if not self.parallel:
            return False

    
        if board_state.check_encountered:
            likely_depth = depth + self.additional_depth   
        else:
            likely_depth = depth
        
        if likely_depth >= 3:
            return True
        # if likely_depth == 2 and board_state.number_legal_moves >= 32:
        #     return True
        return False


    

    def break_up_legal_moves_to_segments(self, legal_moves: list, number_sub_arrays):
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




class Timed_Minimax_Sub_Job(Minimax_Sub_Job):
    def __init__(self, move_engine: Move_Engine, board_state: Board_State, depth, cache_allowed, cache_manager, args, kwargs, max_time) -> None:
        # print("INIT  Timed_Minimax_Sub_Job", flush=True)
        super().__init__(move_engine, board_state, depth, cache_allowed, cache_manager, args, kwargs)
        self.max_time = max_time

    def is_time_expired(self):
        return perf_counter() >= self.max_time

    def __call__(self, legal_moves_sub_array):
        return self.move_engine.minimax_first_call(
            board_state=self.board_state,
            depth=self.depth,
            legal_moves_to_examine=legal_moves_sub_array,
            is_time_expired = self.is_time_expired,
            *self.args,
            **self.kwargs
        )
        # print(f"Timed_Minimax_Sub_Job call:   self.is_time_expired()   -->   {self.is_time_expired()}", flush=True)
        # sys.stdout.flush()
        # # raise Exception("Testing if this code is run Timed_Minimax_Sub_Job")
        # if self.is_time_expired():
        #     # is_maximizer = self.move_engine.color_maximizer_key[self.board_state.next_to_go]
        #     # worst_score_multiplier = (-1) if is_maximizer else 1
        #     # worst_score = (ARBITRARILY_LARGE_VALUE + 1) * worst_score_multiplier
        #     # return worst_score, None
        #     raise TimeOutError("Time out error in minimax sub job")
        # else:
        #     return super().__call__(legal_moves_sub_array)


class Timed_Presort_Moves_Sub_Job(Presort_Moves_Sub_Job):
    def __init__(self, depth, board_state: Board_State, move_engine: Move_Engine, cache_manager, max_time) -> None:
        # print("INIT  Timed_Presort_Moves_Sub_Job ", flush=True)
        super().__init__(depth, board_state, move_engine, cache_manager)
        self.max_time = max_time

    def is_time_expired(self):
        return perf_counter() >= self.max_time


    def __call__(self, move):
        child = self.board_state.make_move(*move)
        child_score, _ = self.move_engine.minimax_first_call(
            board_state = child,
            depth = self.depth,
            is_time_expired=self.is_time_expired,
        )
        return (child_score, move)

        # # print("Closing cache")
        # return (child_score, move)
        # print(f"Timed_Presort_Moves_Sub_Job call:   self.is_time_expired()   -->   {self.is_time_expired()}", flush=True)
        # sys.stdout.flush()
        # # raise Exception("Testing if this code is run Timed_Minimax_Sub_Job")
        # if self.is_time_expired():
        #     # is_maximizer = self.move_engine.color_maximizer_key[self.board_state.next_to_go]
        #     # is_child_maximizer = not is_maximizer
        #     # worst_score_multiplier = (-1) if is_child_maximizer else 1
        #     # worst_score = (ARBITRARILY_LARGE_VALUE + 1) * worst_score_multiplier
        #     # return worst_score, None
        #     raise TimeOutError("Time out error in presort")
        # else:
        #     return super().__call__(legal_moves_sub_array)




class Timed_Move_Engine(Move_Engine_Prime):
    def timed_call(self, board_state: Board_State, time):
        # so that internal jobs can access the time used up indicator
        self.max_time = perf_counter() + time
        def time_used_up():
            return perf_counter() >= self.max_time

        deepest_result = self.minimax_first_call(board_state=board_state, depth=0)
        depth = 1
        # while True:
        while not time_used_up():
            # print(f"Iterating again: time_used_up()   -->   {time_used_up()}")
            try:
                deepest_result = self.minimax_first_call_parallel(board_state=board_state, depth=depth)
                # print(f"Result at depth {depth}:   {deepest_result}")
            except TimeOutError:
                # print(f"Breaking: time_used_up()   -->   {time_used_up()}")
                break 
            else:
                # print(f"Completes depth={depth} so incrementing depth")
                depth += 1

        # print(f"Returning result at greatest depth={depth}")
        return deepest_result, depth

    def __call__(self, board_state: Board_State, time, *args, **kwargs):
        return self.timed_call(board_state=board_state, time=time)

    def generate_move_child_in_parallel(self, board_state: Board_State, depth: int, is_maximizer, give_child=True):
        # print("CALL TIMED generate_move_child_in_parallel")
        # print("generate_move_child_in_parallel called")

        explore_depth = max(depth-3, 0)

        if (not self.cache_allowed):
            yield from super().generate_move_child(
                board_state=board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=give_child
            )
        elif (self.parallel) or (explore_depth < 1):
            with self.cache_manager:
                yield from super().generate_move_child(
                    board_state=board_state,
                    depth=depth,
                    is_maximizer=is_maximizer,
                    give_child=give_child
                )
        else:
            #   # print("getting legal moves")
            legal_moves = list(board_state.generate_legal_moves())

            # print("setting up job")
            basic_move_engine = Move_Engine(
                cache_allowed=True,
                cache_manager=self.cache_manager,
                presort_moves=True,
                additional_depth=0
            )

            job = Timed_Presort_Moves_Sub_Job(
                depth=explore_depth,
                board_state=board_state,
                move_engine=basic_move_engine,
                cache_manager=self.cache_manager,
                max_time=self.max_time,
            )

            # print("generate_move_child_in_parallel: Using multiprocessing pool")
            try:
                with multiprocessing.Pool(self.workers) as pool:
                    moves_and_scores = pool.map(
                        func=job,
                        iterable=legal_moves
                    )
                    pool.close()
                    pool.join()
            except TimeOutError:
                # anticipated
                raise
            # print("generate_move_child_in_parallel: finished with multiprocessing pool")

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

    def parallel_minimax(self, board_state, depth, cache_allowed, cache_manager, *args, **kwargs):
        # print("CALL TIMED parallel_minimax")
        # print("Parallel minimax called")

        # assert isinstance(depth, int)

        # assert depth >= 2, "depth must be greater or equal to 2 to do parallelization"

        is_maximizer = self.color_maximizer_key.get(board_state.next_to_go)

        # print("started getting moves_and_child_sorted")
        # print("getting legal moves, presorted")

        if self.parallel:
            moves_sorted = list(self.generate_move_child_in_parallel(
                board_state=board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=False
            ))
        else:
            moves_sorted = list(self.generate_move_child(
                board_state=board_state,
                depth=depth,
                is_maximizer=is_maximizer,
                give_child=False
            ))

        # print("finished getting moves_and_child_sorted")
        # print("moves_sorted: ")
        # print(moves_sorted)

        legal_move_sub_arrays = self.break_up_legal_moves_to_segments(
            legal_moves=moves_sorted,
            number_sub_arrays=self.workers
        )
        
        # print("legal moves sub arrays generated")

        # print("Printing legal moves sub arrays")
        # print(legal_move_sub_arrays)

        # print("Defining job for workers")
        # use these legal moves to do many simultaneous minimax operations
        job = Timed_Minimax_Sub_Job(
            # move_engine=self,
            move_engine=Move_Engine(
                cache_manager=cache_manager,
                cache_allowed=cache_allowed,

                # is this the miracle fix?
                additional_depth=self.additional_depth,

            ),
            board_state=board_state,
            depth=depth,
            cache_allowed=cache_allowed,
            cache_manager=cache_manager,
            args=args,
            kwargs=kwargs,
            max_time=self.max_time,
        )
        # job = Minimax_Sub_Job(*(None,)*7)

        # print(f"dill.pickles(job)    -->    {dill.pickles(job)}")

        # assert dill.pickles(job)
        # assert dill.pickles(legal_move_sub_arrays)

        # print(f"Using pool to complete jobs in parallel (pool size = {cores})")

        # print("parallel_minimax: Using multiprocessing pool")
        try:
            with multiprocessing.Pool(self.workers) as pool:
                minimax_sub_job_results = pool.map(
                    func=job,
                    iterable=legal_move_sub_arrays
                )
                pool.close()
                pool.join()
        except TimeOutError:
            # error anticipated hear
            raise

        # print("parallel_minimax: multiprocessing finished")

        best_move = None
        if is_maximizer:
            best_score = 0-(ARBITRARILY_LARGE_VALUE + 1)
        else:
            best_score = ARBITRARILY_LARGE_VALUE + 1

        # select best move
        for result in minimax_sub_job_results:
            score, move = result

            if (is_maximizer and score > best_score) or (not is_maximizer and score < best_score):
                best_score = score
                best_move = move

        # print("finished getting best outcome")

        return best_score, best_move

def check_timed():
    board_state = Board_State()
    move_engine = Timed_Move_Engine()
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