# import external modules
import flask
import os
from flask_socketio import SocketIO
import datetime
import pickle

# import local modules
from assorted import safe_hash
from database import save_game, get_saved_game, persistent_DB_engine, create_session, end_session
from chess_game import Game_Website
from schemas import serialize_legal_moves, deserialize_move, serialize_pieces_matrix, serialize_piece


# fix tabes don't exist on reload bug: https://stackoverflow.com/questions/44531360/flask-blogging-error-table-doesnt-exist-tables-not-being-created



# establish various important directories in variables
basedir = os.getcwd()

static_folder_path = os.path.join(basedir, 'website', 'static')
template_folder_path = os.path.join(basedir, 'website', 'templates')
key_file_path = os.path.join(basedir, 'website', 'secret_key.key')

# retrieve the secret key
with open(key_file_path, "r") as file:
    secret_key = file.read()

# sanitize secret key to remove white space
secret_key = secret_key\
    .replace(" ", "")\
    .replace("\n", "")\
    .replace(chr(13), "")



# create an app object and configure it
app = flask.Flask(
    __name__,
    static_folder=static_folder_path,
    template_folder=template_folder_path,
)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secret_key


# create the socketio object (bound to the app object)
# socketio = SocketIO(app, async_mode=None)
# socketio = SocketIO(app, async_mode="gevent")
socketio = SocketIO(app, async_mode=None, threaded=True, echo=False)



@app.route("/")
def index():
    # this is the only http endpoint,
    # it renders the appropriate html file

    response = flask.make_response(
        flask.render_template("chess_game.html")
    )

    # ot then adds a cookie to the response that contains a cookie key corresponding to the game in the session
    expires = datetime.datetime.now() + datetime.timedelta(hours=48)

    cookie_key = flask.session["cookie_key"]
    cookie_formatted = str(cookie_key).encode("utf-8")

    response.set_cookie(
        "chess_game_cookie_key",
        cookie_formatted,
        expires=expires
    )

    # print(f"index: cookie created: {cookie_key}")

    # the response is returned, creating the cookie and providing the html file for the webpage
    return response

# the below functions both get and save a Game_Website object to the flask session as a binary blob
# this prevent issues that can occur when python objects are saved directly in the flask session
def get_game_in_session() -> Game_Website:
    # print(repr(flask.session["game"]))
    # print(repr(pickle.loads(flask.session["game"])))
    return pickle.loads(
        flask.session["game"]
    )

def set_game_in_session(game: Game_Website):
    flask.session["game"] = pickle.dumps(
        game
    )


# def get_game_in_session() -> Game_Website:
#     return flask.session["game"]


# def set_game_in_session(game: Game_Website):
#     flask.session["game"] = game



# this handler function is responsible for initializing a flask session
def create_flask_session():
    # if flask.session.get("session_setup_complete"):
    #     return None
    # else:
    #     flask.session["session_setup_complete"] = True

    
    # it first checks the cookies

    # print("Creating session")
    # check cookies
    # game_hash_cookie = flask.request.cookies.get("chess_game_hash")
    game_cookie = flask.request.cookies.get("chess_game_cookie_key")

    # print(f"In creating session, cookie chess_game_cookie_key fetched, it contains:   {game_cookie}")

    # if the appropriate cookie doesn't exist, a random number is used as the cookie key,
    # and a fresh game is created 
    if game_cookie is None:
        print("Cookie was none / doesn't exist")
        game = Game_Website()
        cookie_key = safe_hash(os.urandom(32))

    # if a cookie id was recovered 
    else:

        # the id is converted into a python sting that contains hexadecimal characters
        hex_string = game_cookie.encode("utf-8").hex()
        cookie_key = bytes.fromhex(hex_string).decode('utf-8')
        print(f"flask cookie contained hash: {cookie_key}")


        # a database session is created
        session_DB = create_session(persistent_DB_engine)

        # the game object is retrieved from the database
        # database_lookup_result: Game_Website = get_saved_game(game_hash=game_hash, session=session)
        database_lookup_result: Game_Website = get_saved_game(cookie_key=cookie_key, session=session_DB)
        # print("database_lookup_result")
        # print(database_lookup_result)

        # the session is disposed of
        end_session(session_DB)
        session_DB = None

        # if the game was found in the database, use it, else create a new game
        if database_lookup_result is None:
            print(f"game: NOT successfully read from database (returned None)")
            game = Game_Website()
        else:
            print(f"game successfully read from database")
            game = database_lookup_result
            print(f"game with hash {hash(game)} successfully read from database")

    
    # now that a game object and a cookie_key have been determined, store these in the session object
    # the index http route will create the appropriate cookie using this id

    # print(repr(game))
    set_game_in_session(game)
    # print(f"At the end of create_flask_session, setting cookie_key to :  {cookie_key}")
    flask.session["cookie_key"] = cookie_key

    # print(f"At the end of create_flask_session, game used has ID:  {hash(game)}")

    

# this handler function is responsible for clearing up a flask session
# this involves saving the game to the database
def close_flask_session():
    # if flask.session.get("session_setup_complete"):
    #     flask.session["session_setup_complete"] = False
    # else:
    #     return None

    # print("Closing session")
    # game: Game_Website = get_game_in_session()

    # get tha game from the database
    game: Game_Website = pickle.loads(
        flask.session["game"]
    )

    # if the window was closed part way though the computer move
    # quickly decide the computers move (time=0) so that game can be resorted on the user's turn
    if game.board_state.next_to_go == "B":
        game.implement_computer_move_and_report(0)


    # print("close_flask_session, game in session is: ")
    # game.board_state.print_board()

    # game = session["game"]

    # get the cookie id,
    cookie_key = flask.session["cookie_key"]
    
    # make a database session and save the game to the database using the cookie id
    session_DB = create_session(persistent_DB_engine)

    save_game(game=game, cookie_key=cookie_key, session=session_DB)

    end_session(session_DB)
    session_DB = None   





@app.before_request
def handle_create_session(*args, **kwargs):
    # this runs the handler function to create a session before the first request (using the session created flag)
    if not flask.session.get("session_created"):
        flask.session["session_created"] = True
        # print("before_request, session:")
        # print(flask.session)
        return create_flask_session()


# unfortunately I needed to use 2 separate events to fully close the flask session
# the on socket disconnect event allows me to access the session data but not change it
# the on http request stop_and_save_game event runs after the session data is deleted, 
# it allow me to change the session data and set the session created flag to false

@socketio.on("disconnect")
def handle_close_session(*args, **kwargs):
    # this runs the handler to dispose of the session when the socket connection breaks
    close_flask_session()



@app.route('/stop_and_save_game')
def handle_close_session(*args, **kwargs):
    # this function sets the flag to indicate that the session needs to be reinitialized
    flask.session["session_created"] = False
    return "session closed"



# here I have created a socket handler function
# it is a decorator as it takes a function as a parameter and returns a modified function with additional functionality
def bind_socket_handler(event_name, respond=True):
    def decorator(function):
        request_event = f"{event_name}_request"
        response_event = f"{event_name}_response"

        # new function to be returned takes incoming payload as an argument
        def wrapper(incoming_payload: dict | None = None):
            # print(f"Handling event: {request_event}")
            
            # if there was an incoming payload, this is given to the original function as an argument after being deserialized
            if incoming_payload is None:
                result = function()
            else:
                # print({"incoming_payload": incoming_payload})
                if not isinstance(incoming_payload, dict):
                    raise TypeError(f"incoming payload of unexpected type:   {type(incoming_payload)}")

                result = function(incoming_payload)

            # if the respond flag is true, the return value of the function is send back to the client
            if respond:
                outgoing_payload: dict = result
                # print(f"Sending response payload by event {response_event}")
                # print({"outgoing_payload": outgoing_payload})

                if not isinstance(outgoing_payload, dict):
                    raise TypeError(f"outgoing payload of unexpected type:   {type(outgoing_payload)}")

                socketio.emit(response_event, outgoing_payload)

        # the wrapper function name is set to the name of the original function
        wrapper.__name__= function.__name__

        # bind wrapper function to happen when request corresponding to the event is received
        # use decorator in manual way to not overwrite wrapper
        socketio.on(request_event)(wrapper)

        # return wrapper for any further use
        return wrapper
    
    return decorator


# the below function accesses the game object in the session 
# it returns a dictionary of serialized data about this game object
def generate_game_update_data():
    game: Game_Website = get_game_in_session()
    
    # collect various data point from the game object and serialize as necessary
    next_to_go = game.board_state.next_to_go
    difficulty = game.difficulty

    legal_moves = list(game.board_state.generate_legal_moves())
    legal_moves_serialised = serialize_legal_moves(legal_moves)

    pieces_matrix = game.board_state.pieces_matrix
    pieces_matrix_serialised = serialize_pieces_matrix(pieces_matrix)

    next_to_go_in_check = game.board_state.color_in_check()

    over, winning_player, victory_classification = game.check_game_over()

    game_over_data =  {
        "over": over,
        "winning_player": winning_player,
        "victory_classification": victory_classification,
    }


    pieces_missing = {}
    for color in ("B", "W"):
        pieces_missing[color] = list(map(
            serialize_piece,
            game.board_state.generate_pieces_taken_by_color(color)
        ))

    move_history = game.move_history_output

    # this is the format of the outgoing payload,
    # flask will convert it to JSON automatically
    # this payload contains all the data that the client needs to be updated about the game state
    payload = {
        "difficulty": difficulty,
        "next_to_go":  next_to_go,
        "game_over_data":  game_over_data,
        "legal_moves":  legal_moves_serialised,
        "pieces_matrix": pieces_matrix_serialised,
        "check": next_to_go_in_check,
        "pieces_taken": pieces_missing,
        "move_history": move_history,
    }
    return payload




# using my custom socket decorator greatly simplifies the process of using sockets

# on request get update from the client, return the generic payload of game data
@bind_socket_handler("get_update")
def get_update():
    """Sends all data from game object to client to update chess game
    This data is also updated after the user move and after the computer move"""
    result = generate_game_update_data()
    # print(f"Update payload for game with hash  {hash(get_game_in_session())}")
    # print(result)
    return result


# on request to implement the computer move
@bind_socket_handler("implement_computer_move")
def implement_computer_move():
    
    # get the game and validate that the computer can go
    game = get_game_in_session()
    assert game.board_state.next_to_go == "B"
    assert not game.board_state.is_game_over_for_next_to_go()[0]

    
    # generate the move and a dictionary of data about it for the client
    # print("generating move")
    move_description = game.implement_computer_move_and_report()

    # update the session with the new mutated game object
    set_game_in_session(game)

    # print("after computer move: game in session is:")
    # get_game_in_session().board_state.print_board()

    # generate a generic update payload and add teh move description before returning 
    outgoing_payload = generate_game_update_data()
    outgoing_payload["computer_move_description"] = move_description

    # print(outgoing_payload)

    return outgoing_payload


# when a request comes to reset the game
# (no response needed)
@bind_socket_handler("reset_game", respond=False)
def reset_game():
    # preserve the difficulty setting
    old_game = get_game_in_session()
    # difficulty preserved
    difficulty = old_game.difficulty

    # create a new game object with the old difficulty and update the session
    new_game = Game_Website(difficulty=difficulty)
    
    set_game_in_session(new_game)

    # return generate_game_update_data()

# takes input from client about the user's move
@bind_socket_handler("implement_user_move")
def implement_user_move(incoming_payload):
    game = get_game_in_session()

    # validate that the user can move
    assert game.board_state.next_to_go == "W"
    assert not game.board_state.is_game_over_for_next_to_go()[0]

    # print("python function called: implement_user_move")
    # deserialize the user's move into vectors
    user_move = tuple(
        deserialize_move(
            incoming_payload["user_move"]
        )
    )
    # implement the move on the game object
    game.implement_user_move(user_move)

    # print("python function finished: implement_user_move")
    # update the session with the new mutated game object
    set_game_in_session(game)

    # print("after user move: game in session is:")
    # get_game_in_session().board_state.print_board()

    # generate and return an update payload 
    return generate_game_update_data()


# on request to change difficulty
@bind_socket_handler("change_difficulty", respond=False)
def change_difficulty(incoming_payload):
    game = get_game_in_session()

    # get the new difficulty form the payload
    new_difficulty = incoming_payload["new_difficulty"]
    # print(f"Changing difficulty to {new_difficulty}")

    # mutate the game object and save it to the session
    game.difficulty = new_difficulty
    
    set_game_in_session(game)

    # doesn't return an update
    # return generate_game_update_data()




# this code below was used to generate the initial game data json file that I no longer use
# before the reload game feature, this prevented the client needing to request the initial game data immediately on loading

# app = None
# if __name__ == "__main__":
#     import json
#     game: Game_Website = Game_Website()

#     next_to_go = game.board_state.next_to_go
#     difficulty = game.difficulty

#     legal_moves = list(game.board_state.generate_legal_moves())
#     legal_moves_serialised = serialize_legal_moves(legal_moves)

#     pieces_matrix = game.board_state.pieces_matrix
#     pieces_matrix_serialised = serialize_pieces_matrix(pieces_matrix)

#     next_to_go_in_check = game.board_state.color_in_check()

#     over, winning_player, victory_classification = game.check_game_over()

#     game_over_data =  {
#         "over": over,
#         "winning_player": winning_player,
#         "victory_classification": victory_classification,
#     }


#     pieces_missing = {}
#     for color in ("B", "W"):
#         pieces_missing[color] = list(map(
#             serialize_piece,
#             game.board_state.generate_pieces_taken_by_color(color)
#         ))

#     move_history = game.move_history_output


#     payload = {
#         "difficulty": difficulty,
#         "next_to_go":  next_to_go,
#         "game_over_data":  game_over_data,
#         "legal_moves":  legal_moves_serialised,
#         "pieces_matrix": pieces_matrix_serialised,
#         "check": next_to_go_in_check,
#         "pieces_taken": pieces_missing,
#         "move_history": move_history,
#     }



#     with open("./website/static/initial_game_data.json", "w") as file:
#         file.write(
#             json.dumps(payload)
#         )
