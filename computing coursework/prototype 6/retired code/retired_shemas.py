# from marshmallow import Schema, fields, pre_load, pre_dump, post_load, post_dump



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


# # this move schema is for socket transmission
# class Move_Schema(Schema):
#     from_vector = fields.Nested(Vector_Schema, required=True)
#     movement_vector = fields.Nested(Vector_Schema, required=True)

#     @pre_load
#     def pre_load(self, vector_tuple, **kwargs):
#         from_vector, movement_vector = vector_tuple
#         return {
#             "from_vector": from_vector,
#             "movement_vector": movement_vector
#         }

#     @post_dump
#     def post_dump(self, data, **kwargs):
#         print({"data": data})
#         return [
#             data["from_vector"],
#             data["movement_vector"]
#         ]
#         # return data


# class Move_Schema(Schema):
#     from_vector = fields.Nested(Vector_Schema, required=True)
#     movement_vector = fields.Nested(Vector_Schema, required=True)

#     @pre_load
#     def pre_load(self, vector_tuple, **kwargs):
#         from_vector, movement_vector = vector_tuple
#         return {
#             "from_vector": from_vector,
#             "movement_vector": movement_vector
#         }

#     @post_dump
#     def post_dump(self, data, **kwargs):
#         print({"data": data})
#         return [
#             [data["from_vector"]["i"], data["from_vector"]["j"]],
#             [data["movement_vector"]["i"], data["movement_vector"]["j"]]
#         ]

# class Legal_Moves_Schema(Schema):
#     moves = fields.List(fields.Nested(Move_Schema), required=True)

#     # @pre_load
#     # def pre_load(self, moves_list, **kwargs):
#     #     print("pre_load")
#     #     print({"moves_list": moves_list})
#     #     data = {}
#     #     data["moves"] = moves_list
#     #     return data

#     # @post_dump
#     # def post_dump(self, data, **kwargs):
#     #     return data
#     #     # print("post_dump")
#     #     # print({"data": data})
#     #     # return data["move"]
