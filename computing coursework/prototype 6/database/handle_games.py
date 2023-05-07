# import external modules and local models
import pickle

from .models import Saved_Game

# cannot import for type hint due to high risk of circular imports
# from chess_game import Game_Website

# this method queries the database for a game by cookie id 
# and then deserializes the binary data to restore the game 
def get_saved_game(cookie_key, session):
    
    # query database for game by cookie key
    result: Saved_Game = session.query(Saved_Game)\
        .where(
            # Saved_Game.game_hash == str(hash(game_hash))
            Saved_Game.cookie_key == str(cookie_key)
        )\
            .first()
    
    # if the result is none (possible if browser has cookie that is invalid) then return none
    if result is None:
        print(f"get_saved_game game not in database so returning none")
        print(f"Couldn't retrieve game with cookie_key:  {cookie_key}")
        return None
    
    # now deserialize the game from the binary data
    game = pickle.loads(
        result.raw_game_data     
    )
    # print(f"this game recovered from database under cookie_key:  {cookie_key}")
    # game.board_state.print_board()

    # print(f"game recovered from database:  {hash(game)}")
    # return the game
    return game


# this function saves a game to the database under a certain cookie ID.
def save_game(game, cookie_key, session):
    # print("saving this game into database")
    # game.board_state.print_board()
    # print(f"saving game in database game with hash {hash(game)} under cookie_key:  {cookie_key}")

    # delete any old games with the same cookie id
    session.query(Saved_Game)\
        .where(
            # Saved_Game.game_hash == str(hash(game_hash))
            Saved_Game.cookie_key == str(cookie_key)
        )\
        .delete()

    # create a new entry in the database and commit
    session.add(
        Saved_Game(game, cookie_key)    
    )
    session.commit()