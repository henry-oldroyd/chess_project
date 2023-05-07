from marshmallow import Schema, fields, pre_load, pre_dump, post_load, post_dump
import flask
import os
from flask_socketio import SocketIO

from chess_engine import Piece, PIECE_TYPES, Board_State

basedir = os.getcwd()
PORT = 5000


app = flask.Flask(
    __name__,
    static_folder=os.path.join(basedir, 'website', 'static'),
    template_folder=os.path.join(basedir, 'website', 'templates'),
)
socketio = SocketIO(app, async_mode=None)

    
# class Piece_Schema(Schema):
#     color = fields.String(required=True)
#     symbol = fields.String(required=True)

#     @pre_load
#     def pre_load(self, piece: Piece, **kwargs):
#         color, symbol = piece.symbol()
#         return [color, symbol]

#     @post_dump
#     def post_dump(self, data, **kwargs):
#         color, symbol = data
#         Piece_type = PIECE_TYPES[symbol]
#         piece = Piece_type(color)
#         return piece

# class Board_Positions_Schema(Schema):
#     board_positions = fields.List(
#         fields.List(
#             fields.Nested(
#                 Piece_Schema,
#                 required=True,
#             ),
#             validate=lambda x: len(x) == 8),
#             requires = True,
#         validate=lambda x: len(x) == 8,
#         required = True
#     )
#     next_to_go = fields.String(required=True)


#     @post_dump
#     def post_dump(self, board_positions, next_to_go, **kwargs):
        
#         return Board_State(
#             next_to_go=next_to_go,
#             pieces_matrix=board_positions
#         )
    
# board_positions_schema = Board_Positions_Schema()

# @socketio.on("server_move_request")
# def handle_server_move_request(msg):
#     # board_positions_json_data: dict = msg['board_positions']
#     # next_to_go: str = msg["next_to_go"]
#     board_state: Board_State = board_positions_schema.load(msg)


# on session creation, create game

@app.route("/")
def index():
    html = flask.render_template("chess_game.html")
    # html = html.replace("((((", "{{").replace("))))", "}}")
    return html


def run_app():
    app.run(host='127.0.0.1', port=PORT, debug=True)

if __name__ == "__main__":
    run_app()