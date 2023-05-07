# imports
# built in libraries
import flask
# import os
from flask_socketio import SocketIO

# my local code
# import logger as logger_module
import game_engine as ge




# setup flask app
app = flask.Flask(__name__)

# setup sockets
socketio = SocketIO(app, async_mode=None)
# RuntimeError: You need to use the gevent-websocket server
# issue solved by running with 'python -m flask run'


# define socket handler for move request
# decorator on move request sent from client
@socketio.on("server_move_request")
def handle_server_move_request(msg):
    # unpack json data and load into object
    game_state: ge.Game_State = ge.Game_State(
        board_positions=msg['board_positions'],
        to_go_next=msg["next_to_go"],
        moves_left=msg['moves_left']
    )
    # use game engine module's main function to determine the best child state (game state following best move)
    best_child: ge.Game_State = ge.main(game_state)

    # code used for debugging to print out the move 
    # print('selecting move:')
    # for row in best_child.board_positions:
    #     print(row)
    
    # now use emit to give a response in the for of an updated board matrix
    socketio.emit(
        "server_move_response",
        {"board_positions": best_child.board_positions}
    )




# define flask api route handlers
# this endpoint responds with the index.html page which will then load and request files form the static folder.
# this is the main endpoint that hosts the 
@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')



# this function simple runs the app and configures the port that is used.
def run_app():
    app.run(host='127.0.0.1', port=5000, debug=True)

# this code runs the main app function only if this file is run directly and not if it is imported
if __name__ == '__main__':
    run_app()

