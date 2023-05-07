# this file is just a file of short assorted constants and functions that are general in use
# It only contains small functions as I have tried to group large, similar functions logically in there own file 

# from functools import lru_cache
# cache_decorator = lru_cache(maxsize=10000)
def cache_decorator(func): return func


# this is used in the static evaluation and minimax process. It is used to represent infinity in a way that still allows comparrison
ARBITRARILY_LARGE_VALUE = 1_000_000


# this function is relatively redundant but allows for print statements in debugging
# in later iteration this may be replaced with logging. 
# it is useful as it allows for DEBUG print statements without needing to remove them when finished
DEBUG = False
def dev_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


