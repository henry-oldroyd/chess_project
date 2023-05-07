

# this error is used to cause the timed minimax function
# raising and then catching this error allows for the algorithm to be self-interrupting 
class TimeOutError(Exception):
    pass


# this is an exception that allows for the game data to be bound to it
# this allows for the relevant chess game that caused the error to be examined afterwards
# it is a normal exception except the constructor has been modified to save the game data as a property
class __ChessExceptionTemplate__(Exception):
    def __init__(self, *args, **kwargs) -> None:
        # none if key not present
        self.game = kwargs.pop("game", None)

        super().__init__(*args, **kwargs)



# these are custom exceptions.
# these are used primarily by the game class
# they contain no logic but have distinct types allowing for targeted error handling
class InvalidMove(__ChessExceptionTemplate__):
    pass


class NotUserTurn(__ChessExceptionTemplate__):
    pass


class NotComputerTurn(__ChessExceptionTemplate__):
    pass


class UnexplainedErroneousMinimaxResultError(__ChessExceptionTemplate__):
    pass
