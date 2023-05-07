import abc
from itertools import product as iter_product, chain as iter_chain
from typing import Callable

from assorted_functions import Vector, ARBITRARILY_LARGE_VALUE


class Piece(abc.ABC):
    owner: int
    color: str
    symbol: str
    last_move: Vector = None

    # required
    value: int
    value_matrix: tuple[tuple[float]]

    # must be given before init
    @abc.abstractproperty
    def value_matrix(): pass

    @abc.abstractproperty
    def value(): pass


    @abc.abstractmethod
    def __init__(self, color, owner, symbol):
        # color is W or B
        # owner is 1 for user or -1 for computer
        self.color = color
        self.owner = owner
        self.symbol = symbol
        # needed for foreword 2 and on-passion
        # self.last_move: Vector = None

    def get_value(self, position_vector: Vector):
        row, column = 7-position_vector.j, position_vector.i
        return self.value + self.value_matrix[row][column]

    @abc.abstractmethod
    # def generate_movement_vectors(self, piece_at_movement_vector: Callable):
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        """Square_at_movement_vector is a function that
        takes a movement vector as a parameter
        it uses the board state and position vector that is encoded on function definition
        it returns the contents of the square at that """


def square_contains_no_piece(square):
    return square is None


class Pawn(Piece):
    value = 100
    value_matrix: tuple[tuple[float]] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]


    def __init__(self, color, owner):
        super().__init__(
            color=color,
            owner=owner,
            # symbol="♟" if color == "B" else "♙"
            symbol="BP" if color == "B" else "WP"
        )

        # multiplier = 1 if self.color == "W" else -1
        # users pieces will be at the bottom and computers at the top
        multiplier = self.owner

        def square_contains_enemy_piece(square):
            if square is None:
                return False
            return square.owner != self.owner


        def can_move_foreword_2(square):
            return square is None and self.last_move is None

        self.movement_vector_and_condition: tuple[Vector, Callable] = (
            # v(0, 1) for foreword
            (Vector(0, 1*multiplier), square_contains_no_piece),
            # v(-1, 1) and v(1, 1) for take
            (Vector(1*multiplier, 1), square_contains_enemy_piece),
            (Vector(-1*multiplier, 1), square_contains_enemy_piece),
            (Vector(0, 2*multiplier), can_move_foreword_2),
        )

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        for movement_vector, condition in self.movement_vector_and_condition:
            resultant_vector = position_vector + movement_vector
            # if vector_out of range continue
            if not resultant_vector.in_board():
                continue

            row, column = 7-resultant_vector.j, resultant_vector.i
            piece = pieces_matrix[row][column]

            if condition(piece):
                yield movement_vector


class Knight(Piece):
    value=320
    value_matrix: tuple[tuple[float]] = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    def __init__(self, color, owner):
        super().__init__(
            color,
            owner,
            # k for king h for horse
            # symbol="WK" if color=="W" else "BK"
            symbol="WH" if color=="W" else "BH"
        )

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        def possible_movement_vectors():
            vectors = (
                Vector(2, 1),
                Vector(1, 2)
            )

            for i_multiplier, j_multiplier in iter_product((-1, 1), (-1, 1)):
                for vector in vectors:
                    yield Vector(
                        vector.i * i_multiplier,
                        vector.j * j_multiplier
                    )
        for movement_vector in possible_movement_vectors():
            resultant_vector = position_vector + movement_vector
            # if vector_out of range continue
            if not resultant_vector.in_board():
                continue

            row, column = 7-resultant_vector.j, resultant_vector.i
            piece = pieces_matrix[row][column]

            if square_contains_no_piece(piece):
                yield movement_vector


class Bishop(Piece):
    value=330
    value_matrix: tuple[tuple[float]] = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    def __init__(self, color, owner):
        super().__init__(
            color,
            owner,
            symbol="WB" if color=="W" else "BB"
        )


    def generate_movement_vectors(self, pieces_matrix, position_vector):
        def square_empty_or_contains_enemy_piece(square):
            if square is None:
                return True
            piece_owner = square.owner
            if piece_owner != self.owner:
                return True
            else:
                return False

        unit_vectors = (
            Vector(1, 1),
            Vector(1, -1),
            Vector(-1, 1),
            Vector(-1, -1),
        )
        for unit_vector in unit_vectors:
            for multiplier in range(8):
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector
                # if vector extends out of the board stop extending the diagonal
                if not resultant_vector.in_board():
                    break
                row, col = 7-resultant_vector.j, resultant_vector.i
                piece: Piece = pieces_matrix[row][col]
                # if piece
                if square_empty_or_contains_enemy_piece(piece):
                    yield movement_vector


class Castle(Piece):
    value=500
    value_matrix: tuple[tuple[float]] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]

    def __init__(self, color, owner):
        super().__init__(
            color,
            owner,
            symbol="WC" if color == "W" else "BC"
        )

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        def square_empty_or_contains_enemy_piece(square):
            if square is None:
                return True
            piece_owner = square.owner
            if piece_owner != self.owner:
                return True
            else:
                return False

        unit_vectors = (
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        for unit_vector in unit_vectors:
            for multiplier in range(1, 8):
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector
                # if vector extends out of the board stop extending the diagonal
                if not resultant_vector.in_board():
                    break
                row, col = 7-resultant_vector.j, resultant_vector.i
                piece: Piece = pieces_matrix[row][col]
                # if piece
                if square_empty_or_contains_enemy_piece(piece):
                    yield movement_vector


class Queen(Piece):
    value=900
    value_matrix: tuple[tuple[float]] = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    def __init__(self, color, owner):
        super().__init__(
            color,
            owner,
            symbol="WQ" if color == "W" else "BQ"
        )

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        def square_empty_or_contains_enemy_piece(square):
            if square is None:
                return True
            piece_owner = square.owner
            if piece_owner != self.owner:
                return True
            else:
                return False

        unit_vectors = (
            Vector(1, 1),
            Vector(1, -1),
            Vector(-1, 1),
            Vector(-1, -1),
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        for unit_vector in unit_vectors:
            for multiplier in range(8):
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector
                # if vector extends out of the board stop extending the diagonal
                if not resultant_vector.in_board():
                    break
                row, col = 7-resultant_vector.j, resultant_vector.i
                piece: Piece = pieces_matrix[row][col]
                # if piece
                if square_empty_or_contains_enemy_piece(piece):
                    yield movement_vector


class King(Piece):
    value = ARBITRARILY_LARGE_VALUE
    value_matrix: tuple[tuple[float]] = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]
    value_matrix_late = [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
    ]

    def __init__(self, color, owner):
        super().__init__(
            color,
            owner,
            symbol="WK" if color == "W" else "BK"
        )

    def update_value_matrix(self, pieces_matrix):
        if sum(int(isinstance(square, Piece)) for square in iter_chain(pieces_matrix)) <= 14:
            self.value_matrix = self.value_matrix_late

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        self.update_value_matrix(pieces_matrix)

        def square_empty_or_contains_enemy_piece(square):
            if square is None:
                return True
            piece_owner = square.owner
            if piece_owner != self.owner:
                return True
            else:
                return False

        unit_vectors = (
            Vector(1, 1),
            Vector(1, -1),
            Vector(-1, 1),
            Vector(-1, -1),
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        for movement_vector in unit_vectors:
            resultant_vector = position_vector + movement_vector
            # if vector extends out of the board stop extending the diagonal
            if not resultant_vector.in_board():
                # print(f"Rv {repr(resultant_vector)} not in board")
                break
            row, col = 7-resultant_vector.j, resultant_vector.i
            piece: Piece = pieces_matrix[row][col]
            # if piece
            if square_empty_or_contains_enemy_piece(piece):
                yield movement_vector
            # else:
                # print(f"Rv {repr(resultant_vector)} Move illegal as results in check)")
