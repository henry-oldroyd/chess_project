# this file is just a file of short assorted constants and functions that are general in use
# It only contains small functions as I have tried to group large, similar functions logically in there own file 

# this is used in the static evaluation and minimax process. It is used to represent infinity in a way that still allows comparrison
ARBITRARILY_LARGE_VALUE = 1_000_000

# this function is relatively redundant but allows for print statements in debugging
# in later iteration this may be replaced with logging. 
# it is useful as it allows for DEBUG print statements without needing to remove them when finished
DEBUG = True
def dev_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


# this is an exception that allows for the game data to be bound to it
# this allows for the relevant chess game that caused the error to be examined afterwards
# it is a normal exception except the constructor has been modified to save the game data as a property
class __ChessExceptionTemplate__(Exception):
    def __init__(self, *args, **kwargs) -> None:        
        # none if key not present 
        self.game = kwargs.pop("game", None)

        super().__init__(*args, **kwargs)

# these are custom exceptions.
# they contain no logic but have distinct types allowing for targeted error handling
class InvalidMove(__ChessExceptionTemplate__):
    pass
class NotUserTurn(__ChessExceptionTemplate__): 
    pass