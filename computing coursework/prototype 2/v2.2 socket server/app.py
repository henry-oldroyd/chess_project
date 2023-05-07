# imports
# built in libraries
import flask
# import os
from flask_socketio import SocketIO
from copy import deepcopy

# my local code
# import logger as logger_module
import game_engine as ge


# define constants


# setup logger
# basedir = os.getcwd()
# LOG_DIR = os.path.join(basedir, 'server.log')
# lgr = logger_module.setup_logger('server', LOG_DIR, level='INFO')
# log_dec = logger_module.logging_decorator_factory(lgr)

# setup flask app
app = flask.Flask(__name__)
# setup sockets
socketio = SocketIO(app, async_mode=None)

# define socket handlers


@socketio.on("server_move_request")
def handle_server_move_request(msg):
    pass

# define flask api route handlers


def run_app():
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    run_app()
