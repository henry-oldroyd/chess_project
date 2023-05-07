# import from external modules
import os
import json
from time import perf_counter

# import local modules
from assorted import safe_hash
from chess_functions import Board_State, Vector
from database import create_session, end_session, persistent_DB_engine, volatile_RAM_engine, Minimax_Cache_Item
from schemas import minimax_cache_item_schema


# create an blank object with no logic that can be used with a context manager
class Blank_Context():
    def __enter__(self, *args, **kwargs):
    # def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __exit__(self, *args, **kwargs):
        pass

# ram cache doesn't need access to a context manager so it uses the blank one
class RAM_cache(Blank_Context):
    # cache is stored in a local dictionary property in the ram cache object
    def __init__(self) -> None:
        self.memoization_cache = dict()

    def cache_size(self):
        return len(self.memoization_cache)


    # the result of a minimax call is added to the cache
    def add_to_cache(self, board_state: Board_State, depth, score, move):
        # moves are stored as tuples of integers
        def serialize_move(move):
            if move is None:
                return None

            return (
                (move[0].i, move[0].j),
                (move[1].i, move[1].j)
            )
        # ensure that the cache exists in the memoization_cache property
        assert self.memoization_cache is not None

        # can use a board_state as a key as it is hashable
        # the board state hash is used as the key within the dictionary (which acts as a hash table)
        board_state_hash = board_state.database_hash()

        # print(f"CALL: add_to_cache(self, board_state={hash(board_state)} depth={depth}, score={score}, move={move}")
        # print(f"self.memoization_cache.get(board_state_hash) is None    -->    {self.memoization_cache.get(board_state_hash) is None}")

        # decide if the cache should be updated based on whether the record already existed and if so, its depth
        if self.memoization_cache.get(board_state_hash) is None:
            needs_update = True
        else:
            best_depth_in_cache = self.memoization_cache[board_state_hash]["depth"]
            # print(f"best_depth_in_cache < depth    -->    {best_depth_in_cache} < {depth}   --->   {best_depth_in_cache < depth}")
            needs_update = best_depth_in_cache < depth

        # print(f"Cache:  {self.memoization_cache}")

        # if need an update then add the record (lesser depth cache overwritten)
        if needs_update:
            new_data_item = {
                "depth": depth,
                "score": score,
                "move": serialize_move(move)
            }

            self.memoization_cache[board_state_hash] = new_data_item
            # if depth >= 1:
            # print(f"New data {board_state_hash} added to cache:   {new_data_item}")
            # print(f"new_cache_size:   {self.cache_size()}")
        # print(f"Cache needed updating:   {needs_update}")

    # this function retrieves an item form cache
    def search_cache(self, board_state, depth):
        # move is converted from tuple of integers back to vectors when deserialized
        def deserialize_move(serialised_move):
            if serialised_move is None:
                return None

            return (
                Vector(*serialised_move[0]),
                Vector(*serialised_move[1])
            )

        assert self.memoization_cache is not None


        # get the hash ov hte board state
        # board_state_hash = hash(board_state)
        board_state_hash = board_state.database_hash()

        # if not in cache, return none
        if self.memoization_cache.get(board_state_hash) is None:
            # if depth >= 2:
            #     print(f"item {board_state_hash} not in cache (depth={depth})")
            return None
        # else check the depth is adequate and return if appropriate
        else:
            best_depth_in_cache = self.memoization_cache[board_state_hash]["depth"]
            record_useful = best_depth_in_cache >= depth
            if record_useful:
                # if depth >= 2:
                # print(f"RAM_Cache used for {board_state_hash}:   {self.memoization_cache[board_state_hash]}")

                data_item = self.memoization_cache[board_state_hash].copy()
                data_item["move"] = deserialize_move(data_item["move"])

                return data_item
            else:
                # if depth >= 2:
                    # print(f"cache not useful for item {board_state_hash}:  {self.memoization_cache[board_state_hash]}, required depth is {depth}")
                # print(f"cache searched but not used")
                return None

# this function creates a persistent cache in a json file
class JSON_Cache(RAM_cache):
    # when the object is created, load the contents of the json file into the memoization cache variable
    def __init__(self, file_path=None) -> None:
        # print("Initializing json cache")
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = r"./database/minimax_cache.json"

        # default
        self.memoization_cache = {}

        # try get data from file
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                content = file.read()
            try:
                assert content != "", "Json file was blank / empty"
                cache_data = json.loads(content)

                # fix that in json, board state hash key is sting
                new_items = map(
                    lambda item: (int(item[0]), item[1]),
                    cache_data.items()
                )
                cache_data = dict(tuple(new_items))

                self.memoization_cache = cache_data
            except Exception as e:
                # print(e)
                # print("Failed to load json cache data so using blank cache")
                pass

    # inherited ram cache method add to and retrieve cache form the memoization cache variable

    # write the memoization cache dictionary to a json file 
    def save(self):
        print(f"Saving cache (size={self.cache_size()}) to json file")
        with open(self.file_path, "w") as file:
            file.write(
                json.dumps(
                    self.memoization_cache
                )
            )

    # do this when the cache manager is closed by the context manager
    def __exit__(self, *args, **kwargs):
        self.save()


# this json cache doesn't save automatically
class JSON_Cache_Manual_Save(JSON_Cache):
    def __exit__(self, *args, **kwargs):
        pass


# database cache connects to the database to store minimax cached results
# it uses a database in RAM for small cache and a persistent database for searches at a greater depth
class DB_Cache():
    # by default, depth 0 uses ram cache and greater depth uses persistent cache
    def __init__(self, min_DB_depth=1):
        # set the min depth parameter as a property and then define other properties with starting values
        self.min_DB_depth = min_DB_depth

        self._RAM_cache = None
        self._DB_session = None
        self.engaged = False
        # a cached depth 3 call can be used if a depth 2 call is needed
        self.allow_greater_depth = True

        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0

    def __enter__(self, *args, **kwargs):
        # when the context manager is used and the boot up sequence runs (this method)
        # a database session is created (using the database module)

        # assert all(e is None for e in (self._RAM_cache, self._DB_session))
        assert not self.engaged, "Must not be engaged (entered) already to enter"
        self.engaged = True

        # these variables keep track of various data points while the cache is used within a context manager 
        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0

        # this allows for the cache manager to be entered multiple times on accident without making multiple sessions
        # self._RAM_cache = RAM_cache()
        # self._persistent_DB_session = scoped_session(sessionmaker(bind=persistent_DB_engine))
        # self._volatile_RAM_session = scoped_session(sessionmaker(bind=volatile_RAM_engine))
        self._persistent_DB_session = create_session(persistent_DB_engine)
        self._volatile_RAM_session = create_session(volatile_RAM_engine)

    def __exit__(self, *args, **kwargs):
        # when the context manager runs the close function of the cache manager (this method)
        # the session objects are closed and discarded and tracker variables are set back to 0

        assert self.engaged, "Must be engaged (entered) to exit"
        self.engaged = False

        end_session(self._persistent_DB_session)
        self._persistent_DB_session = None

        end_session(self._volatile_RAM_session)
        self._volatile_RAM_session = None

        # print(f"Cache session lasted {round(self.time_delta_DB, 2)}+{round(self.time_delta_schemas, 2)} sec (DB + schema time): {self.checks_to_cache} checks made, {self.retrieved_item} items retrieved, {self.items_added} items added")

        self.time_delta_DB = 0
        self.time_delta_schemas = 0
        self.checks_to_cache = 0
        self.retrieved_item = 0
        self.items_added = 0

    def _search_DB_cache(self, session, board_state, depth):
        # this function hashes the board state and searches the database for cache corresponding to that hash

        # board_state_hash = str(hash(board_state))
        board_state_hash = board_state.database_hash()

        start = perf_counter()

        # cache must have a matching hash and a sufficient depth
        # ORM allows for queries to be written in a pythonic way
        if self.allow_greater_depth:
            result = session.query(Minimax_Cache_Item)\
                .where(
                    Minimax_Cache_Item.board_state_hash == board_state_hash
            )\
                .where(
                    Minimax_Cache_Item.depth >= depth
            )\
                .first()
        else:
            result = session.query(Minimax_Cache_Item)\
                .where(
                    Minimax_Cache_Item.board_state_hash == board_state_hash
            )\
                .where(
                    Minimax_Cache_Item.depth == depth
            )\
                .first()

        stop = perf_counter()
        self.time_delta_schemas += stop - start

        # if not item found then return none
        if result is None:
            return None

        start = perf_counter()

        # use the schema object to deserialize the cached item before returning it.
        result = minimax_cache_item_schema.dump(result)

        stop = perf_counter()
        self.time_delta_schemas += stop - start

        return result

    def _add_to_DB_cache(self, session, board_state: Board_State, score, depth, move):
        # this function adds an item to the cache

        start = perf_counter()

        # board state is hashed
        # print("adding item to database cache")
        # board_state_hash = str(hash(board_state))
        board_state_hash = board_state.database_hash()

        # if depth >= 2:
        #     print(f"Adding item {board_state_hash} at depth {depth} to cache")

        # new database entry item created with schema
        new_item = minimax_cache_item_schema.load(
            dict(
                board_state_hash=board_state_hash,
                score=score,
                depth=depth,
                move=move
            )
        )

        stop = perf_counter()
        self.time_delta_schemas += stop - start

        start = perf_counter()

        # other searches at a lesses depth are deleted
        # (assumes cache already checked and the other cache is worse)
        session.query(Minimax_Cache_Item)\
            .where(
            Minimax_Cache_Item.board_state_hash == board_state_hash
        )\
            .delete()

        # print(f"move   -->   {move!r}")

        # print(f"New item:   {new_item!r}")

        # the item is added to the database and committed
        session.add(new_item)
        session.commit()

        stop = perf_counter()
        self.time_delta_DB += stop - start

    def search_cache(self, board_state: Board_State, depth):
        # this function searches the cache
        assert self.engaged, "Context manager must be used"

        self.checks_to_cache += 1

        # not sure why depth sometimes is a single length tuple containing an int
        # here is a quick fix
        if isinstance(depth, tuple):
            if len(depth) == 1:
                depth = depth[0]



        # print(f"(depth, self.min_DB_depth)     -->     {(depth, self.min_DB_depth)}")

        # decide which session to use based on depth
        if depth < self.min_DB_depth:
            session = self._volatile_RAM_session
            # return self._RAM_cache.search_cache(board_state=board_state, depth=depth)
        else:
            session = self._persistent_DB_session
            # return self._search_DB_cache(board_state=board_state, depth=depth)

        # search the cache with this session and then return the result
        result = self._search_DB_cache(session=session, board_state=board_state, depth=depth)

        if result is not None:
            self.retrieved_item += 1

        return result


    def add_to_cache(self, board_state: Board_State, score, depth, move):
        # this function adds to the cache
        # this function assumes that no move valuable cache already exists (it overwrites all other cache)
        assert self.engaged, "Context manager must be used"

        # this is used to tackle any bugs elsewhere in the program
        # it ensures that no invalid cache items are added to the database
        def absolute(x): return x if x >= 0 else 0-x
        if absolute(score) > 1_000_000 or (move is None and depth > 0):
            # don't add erroneous data to cache
            return None


        # decides that session to use based on depth
        if depth < self.min_DB_depth:
            session = self._volatile_RAM_session
            # self._RAM_cache.add_to_cache(board_state=board_state, score=score, depth=depth, move=move)
        else:
            session = self._persistent_DB_session
            # self._add_to_DB_cache(board_state=board_state, score=score, depth=depth, move=move)

        # the caches item is added to the database
        self._add_to_DB_cache(session=session, board_state=board_state, score=score, depth=depth, move=move)

        self.items_added += 1

    
    # the hash function describes only the data that makes this cache object unique
    def __hash__(self) -> int:
        hash(safe_hash(
            (
                "DB_Cache",
                # self._RAM_cache,
                # self._DB_session,
                self.min_DB_depth,
                self.engaged,
                self.allow_greater_depth,
                # self.time_delta_DB
                # self.time_delta_schemas
                # self.checks_to_cache
                # self.retrieved_item
                # self.items_added
            )
        ))