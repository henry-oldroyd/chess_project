from marshmallow import Schema, fields, pre_load, pre_dump, post_load, post_dump
from chess_functions import Vector, Piece, PIECE_TYPES

# different schema to serialize and deserialize a vector
class Vector_Schema(Schema):
    i = fields.Integer(required=True)
    j = fields.Integer(required=True)

    @post_load
    def get_vector_from_internal_data(self, internal_data, **kwargs):
        # print({"internal_data": internal_data})
        return Vector(**internal_data)

    @pre_load
    def get_internal_data_from_list(self, list_data, **kwargs):
        return {"i": list_data[0], "j": list_data[1]}
    

    @post_dump
    def make_list_from_internal_data(self, internal_data, **kwargs):
        return [internal_data['i'], internal_data['j']]


letter_symbol_pairs = (
    ("P", "♟︎"),
    ("K", "♚"),
    ("Q", "♛"),
    ("R", "♜"),
    ("B", "♝"),
    ("N", "♞"),
)

# these functions get the symbol or letter associated with each piece by searching the above tuple
def get_symbol_from_letter(target_letter):
    for letter, symbol in letter_symbol_pairs:
        if letter == target_letter.strip().upper():
            return symbol
    raise ValueError(f"letter  '{letter}'  not found")

def get_letter_from_symbol(target_symbol):
    for letter, symbol in letter_symbol_pairs:
        if symbol == target_symbol.strip():
            return letter
    raise ValueError(f"symbol  '{symbol}'  not found")


# this schema serialised and deserializes between the Pieces object and format use in JSON sent to the client
class Piece_Schema(Schema):
    color = fields.String(required=True)
    letter = fields.String(required=True)

    @pre_load
    def pre_load(self, data, **kwargs):
        color, symbol = data
        letter = get_letter_from_symbol(symbol)
        return {
            "color": color,
            "letter": letter,
        }

    @post_load
    def post_load(self, data, **kwargs):
        color, letter = data["color"], data["letter"]
        Piece_Type = PIECE_TYPES[letter]
        return Piece_Type(color)

    @pre_dump
    def pre_dump(self, piece: Piece, **kwargs):
        color, letter = piece.symbol()
        return {
            "color": color,
            "letter": letter,
        }

    @post_dump
    def post_dump(self, data, **kwargs):
        color, letter = data["color"], data["letter"]
        symbol = get_symbol_from_letter(letter)
        return [color, symbol]
    

# these function are utility function that can map a function across a 1d or 2d array, transforming all the elements 
def list_map(some_function, array):
    return list(map(some_function, array))

def two_d_list_map(some_function, two_d_array):
    return list_map(
        lambda one_d_array: list_map(
            some_function,
            one_d_array
        ),
        two_d_array
    )

# create objects form the schemas with which to serialize and deserialize
vector_schema = Vector_Schema()
piece_schema = Piece_Schema()


# here are functions that use thee schemas to serialize and deserialize key data points to and from a dictionary (JSON like) format
def serialize_legal_moves(legal_moves):
    return two_d_list_map(vector_schema.dump, legal_moves)

def deserialize_legal_moves(legal_moves):
    return two_d_list_map(vector_schema.load, legal_moves)


def serialize_move(move):
    return list_map(vector_schema.dump, move)

def deserialize_move(move):
    return list_map(vector_schema.load, move)


def serialize_piece(piece):
    if piece is None: 
        return [None, None]
    else:
        return piece_schema.dump(piece)

def deserialize_piece(piece):
    # print(piece, end=";   ")
    if piece == [None, None]: 
        return None
    else:
        return piece_schema.load(piece)

def serialize_pieces_matrix(pieces_matrix):
    return two_d_list_map(serialize_piece, pieces_matrix)

def deserialize_pieces_matrix(pieces_matrix):
    # print("deserialize_pieces_matrix   called")
    return two_d_list_map(deserialize_piece, pieces_matrix)

