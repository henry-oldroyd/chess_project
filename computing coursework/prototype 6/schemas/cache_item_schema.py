# import external and external modules
from marshmallow import Schema, fields, pre_load, pre_dump, post_load, post_dump

from chess_functions import Vector
from database import Minimax_Cache_Item

# the vector schema describes how to serialize and deserialize a vector object
# it converts between Vector(i=a, j=b) and [a, b]
class Vector_Schema(Schema):
    i = fields.Integer(required=True)
    j = fields.Integer(required=True)

    @pre_load
    def pre_load(self, vector, **kwargs):
        data = {}
        data["i"] = vector.i
        data["j"] = vector.j
        return data

    @post_dump
    def post_dump(self, data, **kwargs):
        return Vector(
            i=data["i"],
            j=data["j"]
        )

# this move schema is for database cache
# it converts between [Vector(a, b), Vector(c, d)] and [[a,b], [c,d]]
# is used the nested Vector Schema to do this
class Move_Schema(Schema):
    from_vector = fields.Nested(Vector_Schema, required=True)
    movement_vector = fields.Nested(Vector_Schema, required=True)

    @pre_load
    def pre_load(self, vector_tuple, **kwargs):
        # print({"vector_tuple": vector_tuple})
        from_vector, movement_vector = vector_tuple
        data = {}
        data["from_vector"] = from_vector
        data["movement_vector"] = movement_vector
        return data

    @post_dump
    def post_dump(self, data, **kwargs):
        return (
            data["from_vector"],
            data["movement_vector"]
        )



# this method deserializes a move string into a pair of Vectors stored in a dictionary
def get_deserialized_move(move):
    # assert len(move) == 4
    # if move == "None":
    if move == None:
        return None

    move = move[1:-1]
    move = move.split(", ")
    from_vector = Vector(
        i=move[0],
        j=move[1]
    )
    movement_vector = Vector(
        i=move[2],
        j=move[3]
    )
    return dict(
        from_vector=from_vector,
        movement_vector=movement_vector
    )

# this method converts a pair of vectors stored in a dictionary to a string representation of the move
def get_serialised_move(move):
    if move is None:
        # return "None"
        return None

    return str((
        move["from_vector"]["i"],
        move["from_vector"]["j"],
        move["movement_vector"]["i"],
        move["movement_vector"]["j"],
    ))


# this class uses the move schema and the above methods to serialize and deserialize a move so that it can be stored in a database 
class Minimax_Cache_Item_Schema(Schema):
    board_state_hash = fields.String(required=True, load_only=True)
    depth = fields.Integer(required=True)
    score = fields.Integer(required=True)
    move = fields.Nested(Move_Schema, required=True, allow_none=True)

    @post_load
    def post_load(self, data, **kwargs):
        # assert isinstance(data["depth"], int)
        # assert isinstance(data["score"], int)
        # print(f"post_load: serializing move form {data['move']} to {get_serialised_move(data['move'])}")

        return Minimax_Cache_Item(
            board_state_hash=data["board_state_hash"],
            depth=data["depth"],
            score=data["score"],
            move=get_serialised_move(
                data["move"]
            )
        )

    @pre_dump
    def pre_dump(self, minimax_cache_item: Minimax_Cache_Item, **kwargs):
        # print(f"pre_dump: deserializing move form {minimax_cache_item.move} to {get_deserialized_move(minimax_cache_item.move)}")
        return dict(
            depth=minimax_cache_item.depth,
            move=get_deserialized_move(
                minimax_cache_item.move
            ),
            score=minimax_cache_item.score
        )

# this object can be used to serialize and deserialize moves to be stored in the database
# it is the final product of this file and the object that will be exported
minimax_cache_item_schema = Minimax_Cache_Item_Schema()
