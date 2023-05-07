from .vector import Vector

import os
import json



class Blank_Context():
    def __enter__(self, *args, **kwargs):
        pass
    # def __exit__(self, exception_type, exception_value, traceback):

    def __exit__(self, *args, **kwargs):
        pass


class RAM_cache(Blank_Context):
    def __init__(self) -> None:
        self.memoization_cache = dict()

    def cache_size(self):
        return len(self.memoization_cache)

    def serialize_move(move):
        return (
            (move[0].i, move[0].j),
            (move[1].i, move[1].j)
        )

    def add_to_cache(self, board_state, depth, score, move):
        def serialize_move(move):
            if move is None:
                return None

            return (
                (move[0].i, move[0].j),
                (move[1].i, move[1].j)
            )

        assert self.memoization_cache is not None
        # can use a board_state as a key as it is hashable

        board_state_hash = hash(board_state)

        # print(f"CALL: add_to_cache(self, board_state={hash(board_state)} depth={depth}, score={score}, move={move}")
        # print(f"self.memoization_cache.get(board_state_hash) is None    -->    {self.memoization_cache.get(board_state_hash) is None}")
        if self.memoization_cache.get(board_state_hash) is None:
            needs_update = True
        else:
            best_depth_in_cache = self.memoization_cache[board_state_hash]["depth"]
            # print(f"best_depth_in_cache < depth    -->    {best_depth_in_cache} < {depth}   --->   {best_depth_in_cache < depth}")
            needs_update = best_depth_in_cache < depth

        # print(f"Cache:  {self.memoization_cache}")

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

    def search_cache(self, board_state, depth):
        def deserialize_move(serialised_move):
            if serialised_move is None:
                return None

            return (
                Vector(*serialised_move[0]),
                Vector(*serialised_move[1])
            )

        assert self.memoization_cache is not None

        board_state_hash = hash(board_state)

        if self.memoization_cache.get(board_state_hash) is None:
            if depth >= 2:
                print(f"item {board_state_hash} not in cache (depth={depth})")
            return None
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


class JSON_Cache(RAM_cache):
    def __init__(self, file_path=None) -> None:
        # print("Initializing json cache")
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = r"./minimax_cache.json"

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

    def save(self):
        print(f"Saving cache (size={self.cache_size()}) to json file")
        with open(self.file_path, "w") as file:
            file.write(
                json.dumps(
                    self.memoization_cache
                )
            )

    def __exit__(self, *args, **kwargs):
        self.save()


class JSON_Cache_Manual_Save(JSON_Cache):
    def __exit__(self, *args, **kwargs):
        pass




class DB_cache():
    pass
