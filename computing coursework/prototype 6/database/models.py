# import external modules
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
import pickle

# cannot be used for type hings as it has a high risk of causing a circular import
# from chess_game import Game_Website

# create a base object with which I will make my database tables (part of the ORM)
Base = declarative_base()


# create an object and a table (ORM used) to represent a cached minimax call
class Minimax_Cache_Item(Base):
    
    # here is the metadata and the columns of the database
    __tablename__ = "Minimax_Cache"

    primary_key = sqla.Column(sqla.Integer, primary_key=True)

    board_state_hash = sqla.Column(sqla.String())
    depth = sqla.Column(sqla.INT())
    score = sqla.Column(sqla.INT())
    # 4 character move string encoded by the 4 digits of the from and movement vectors
    move = sqla.Column(sqla.String)

    # a single entry can be created by initializing an object with this class 
    def __init__(self, board_state_hash: str, depth, move: str, score: int):
        # hash board state
        self.board_state_hash = str(board_state_hash)
        self.depth = depth
        self.move = move
        self.score = score

    # string description of object
    def __repr__(self) -> str:
        return f"Minimax_Cache_Item(board_state_hash='{self.board_state_hash}', depth={self.depth}, move='{self.move}', score={self.score})"



# this object represents an entry in a database table that saves games for later reloading 
class Saved_Game(Base):
    # metadata as well as columns defined here
    __tablename__ = "Saved_Games"

    primary_key = sqla.Column(sqla.Integer, primary_key=True)

    # game_hash = sqla.Column(sqla.String())
    cookie_key = sqla.Column(sqla.String())
    raw_game_data = sqla.Column(sqla.BINARY())

    # initializing an object from this class allow a new entry in the database to be made
    def __init__(self, game, cookie_key):
        self.cookie_key = str(cookie_key)
        self.raw_game_data = bytes(
            pickle.dumps(
                game
            )    
        )

    # string description of object
    def __repr__(self) -> str:
        return f"Saved_Game(cookie_key='{self.cookie_key}')"


# create indexes on cookie key and board state hash as these are the columns that I will use to search for a specific entry
sqla.schema.Index("board_state_hash", Minimax_Cache_Item.board_state_hash)
sqla.schema.Index("cookie_key", Saved_Game.cookie_key)


# for each engine, build these tables
def create_tables(engines_dict):
    for engine in engines_dict.values():
        Base.metadata.create_all(engine, checkfirst=True)
