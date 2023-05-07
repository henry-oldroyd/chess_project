# to do: make value and value matrix unchangeable of private
# https://stackoverflow.com/questions/31457855/cant-instantiate-abstract-class-with-abstract-methods

# import libraries and other local modules
import abc
from itertools import chain as iter_chain, product as iter_product
from typing import Callable

from vector import Vector
from assorted import ARBITRARILY_LARGE_VALUE

# Here is an abstract base class for piece,
# it dictates that all child object have the specified abstract attributes else and error will occur
# this ensures that all piece objects have the same interface


class Piece(abc.ABC):

    # required
    # color is public
    color: str | None
    # value and value matrix is protected
    # value is inherent value
    _value: int
    # value matrix is additional value based on location
    _value_matrix: tuple[tuple[float]]

    # must be given before init
    @abc.abstractproperty
    def _value_matrix(): pass

    @abc.abstractproperty
    def _value(): pass

    @abc.abstractproperty
    def color(): pass

    @abc.abstractmethod
    def symbol(self) -> str:
        """uses color to determine the appropriate symbol"""

    # not needed as abstract method as come classes will nor override
    def __init__(self, color):
        self.color = color
        self.last_move = None

    # this should use the position vector and value matrix to get the value of the piece
    def get_value(self, position_vector: Vector):
        # flip if black as matrices are all for white pieces
        if self.color == "W":
            row, column = 7-position_vector.j, position_vector.i
        else:
            row, column = position_vector.j, position_vector.i

        # return sum of inherent value + value relative to positon on board
        return self._value + self._value_matrix[row][column]

    # this function should yield all the movement vector tha the piece can move by
    # this doesn't account for check and is based on rules specific to each piece as well an checking if a vector is outside the board

    @abc.abstractmethod
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        pass

    # when str(piece) called give the symbol

    def __str__(self):
        # return f"{self.color}{self.symbol}"
        return self.symbol()

    # standard repr method
    def __repr__(self):
        return f"{type(self).__name__}(color='{self.color}')"

    # logic that would be otherwise repeated in many of the child classes
    # determines the contents of a given square
    def square_contains(self, square):
        """returns 'enemy' 'ally' or None for empty"""
        # check if empty
        if square is None:
            return "empty"
        # else the square must contain a piece, so examine its color
        if square.color == self.color:
            return "ally"
        else:
            return "enemy"

    # again reduces repeated logic
    # checks the result of a position vector
    # if not illegal (out of board) the square contents is returned
    def examine_position_vector(self, position_vector: Vector, pieces_matrix):
        """returns 'enemy' 'ally' 'empty' or 'illegal'  """
        # check if the vector is out of the board
        if not position_vector.in_board():
            return 'illegal'
        # for the rest of the code I can assume the vector is in board

        # else get the square at that vector
        row, column = 7-position_vector.j, position_vector.i
        square = pieces_matrix[row][column]

        # examine its contents
        return self.square_contains(square)

    # equality operator
    def __eq__(self, other):
        try:
            # assert same subclass like rook
            assert isinstance(other, type(self))
            assert self.color == other.color

            # i am not checking that pieces had the same last move as I want to compare kings without for the check function
            # assert self.last_move == other.last_moves

            # value and value_matrix should never be changes
        except AssertionError:
            return False
        else:
            return True

    # making pieces hashable allows for pieces matrices to be hashed and allows for pieces and pieces matrices to be put in sets,
    # also essential for piping data between python interpreter instances (different threads) for multitasking
    def __hash__(self):
        return hash((self.symbol(), self.color, self.last_move))


# this class inherits from Piece an so it inherits some logic and some requirements as to how its interface should be
# as many child classes are similar I will explain this one in depth and then only explain notable features of others
class Pawn(Piece):
    # defining abstract properties, needed before init
    _value = 100
    _value_matrix: tuple[tuple[float]] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    color = None

    # define symbol method (str method)
    def symbol(self): return f"{self.color}P"

    # override init constructor
    def __init__(self, color):
        # perform super's instructor
        super().__init__(color)

        # but in addition...
        # decide the vectors that the piece can move now as it is based on color
        multiplier = 1 if color == "W" else -1

        # method defined here as it only used here
        # decided if the pawn is allowed to move foreward 2 based on square contents and last move
        def can_move_foreword_2(square):
            return square is None and self.last_move is None

        # tuple contains pairs of vector and contition that must be met
        # (in the form of a function that takes square and returns a boolean)
        self.movement_vector_and_condition: tuple[Vector, Callable] = (
            # v(0, 1) for foreword
            (Vector(0, multiplier), lambda square: self.square_contains(square) == "empty"),
            # v(0, 2) for foreword as first move
            (Vector(0, 2*multiplier), can_move_foreword_2),
            # v(-1, 1) and v(1, 1) for take
            (Vector(1, multiplier), lambda square: self.square_contains(square) == 'enemy'),
            (Vector(-1, multiplier), lambda square: self.square_contains(square) == 'enemy'),
        )

    # generate movement vectors
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # iterate through movement vectors and conditions
        for movement_vector, condition in self.movement_vector_and_condition:
            # get resultant vector
            resultant_vector = position_vector + movement_vector
            # if vector_out of range continue
            if not resultant_vector.in_board():
                continue

            # get the contents of the square corresponding to the resultant
            row, column = 7-resultant_vector.j, resultant_vector.i
            piece = pieces_matrix[row][column]

            # if the condition is met, yield the vector
            if condition(piece):
                yield movement_vector


class Knight(Piece):
    _value = 320
    _value_matrix: tuple[tuple[float]] = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]
    color = None

    # n for knight as king takes k
    def symbol(self): return f"{self.color}N"

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # this function yields all 8 possible vectirs
        def possible_movement_vectors():
            vectors = (Vector(2, 1), Vector(1, 2))
            # for each x multiplier, y multiplier and vector combination
            for i_multiplier, j_multiplier, vector in iter_product((-1, 1), (-1, 1), vectors):
                # yield corresponding vector
                yield Vector(
                    vector.i * i_multiplier,
                    vector.j * j_multiplier
                )
        # iterate through movement vectors
        for movement_vector in possible_movement_vectors():
            # get resultant
            resultant_vector = position_vector + movement_vector
            # look at contents of square
            contents = self.examine_position_vector(position_vector=resultant_vector, pieces_matrix=pieces_matrix)
            # if square is empty yield vector
            if contents == "empty":
                yield movement_vector


class Bishop(Piece):
    _value = 330
    _value_matrix: tuple[tuple[float]] = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]
    color = None

    def symbol(self): return f"{self.color}B"

    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # sourcery skip: use-itertools-product

        # repeat for all 4 vector directions
        for i, j in iter_product((1, -1), (1, -1)):
            unit_vector = Vector(i, j)
            # iterate through length multipliers
            for multiplier in range(1, 8):
                # get movement and resultant vectors
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector

                # examine the contents of the square and use switch case to decide behaviour
                match self.examine_position_vector(position_vector=resultant_vector, pieces_matrix=pieces_matrix):
                    case 'illegal':
                        # if vector extends out of the board stop extending
                        break
                    case 'ally':
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'enemy':
                        # this is a valid move
                        yield movement_vector
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'empty':
                        # is valid
                        yield movement_vector
                        # and keep exploring, don't break


class Rook(Piece):
    _value = 500
    _value_matrix: tuple[tuple[float]] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]
    color = None

    # r for rook
    def symbol(self): return f"{self.color}R"



    # this code is very similar in structure to that of a bishop just with different direction vectors
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # sourcery skip: use-itertools-product
        unit_vectors = (
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        # for unit_vector, multiplier in iter_product(unit_vectors, range(1, 8)):
        for unit_vector in unit_vectors:
            for multiplier in range(1, 8):
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector

                # note cases that contain only break are not redundant, they break the outer for loop
                match self.examine_position_vector(position_vector=resultant_vector, pieces_matrix=pieces_matrix):
                    case 'illegal':
                        # if vector extends out of the board stop extending
                        break
                    case 'ally':
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'enemy':
                        # this is a valid move
                        yield movement_vector
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'empty':
                        # is valid
                        yield movement_vector
                        # and keep exploring, don't break


class Queen(Piece):
    _value = 900
    _value_matrix: tuple[tuple[float]] = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]
    color = None

    def symbol(self): return f"{self.color}Q"

    # this code also uses a similar structure to the rook or bishop
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # unit_vectors = (Vector(i, j) for i, j in iter_product((-1, 0, 1), (-1, 0, 1)) if i != 0 and j != 0)
        unit_vectors = (Vector(i, j) for i, j in iter_product((-1, 0, 1), (-1, 0, 1)) if i != 0 or j != 0)

        # for unit_vector, multiplier in iter_product(unit_vectors, range(1, 8)):
        for unit_vector in unit_vectors:
            for multiplier in range(1, 8):
                movement_vector = unit_vector * multiplier
                resultant_vector = position_vector + movement_vector
                match self.examine_position_vector(position_vector=resultant_vector, pieces_matrix=pieces_matrix):
                    case 'illegal':
                        # if vector extends out of the board stop extending
                        break
                    case 'ally':
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'enemy':
                        # this is a valid move
                        yield movement_vector
                        # break of of for loop (not just match case)
                        # as cannot hop over piece so don't explore longer vectors in same direction
                        break
                    case 'empty':
                        # is valid
                        yield movement_vector
                        # and keep exploring, don't break


class King(Piece):
    # not needed as static eval does't add up kings value
    _value = ARBITRARILY_LARGE_VALUE

    # there are 2 matrices to represent the early and late game for the king
    value_matrix_early: tuple[tuple[float]] = [
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
    color = None

    # initially value matrix is the early one
    _value_matrix: tuple[tuple[float]] = value_matrix_early

    # def __init__(self, *args, **kwargs):
    #     self._value_matrix = self.value_matrix_early
    #     super().__init__(self, *args, **kwargs)

    def symbol(self): return f"{self.color}K"

    # based on total pieces, changes the value matrix
    def update_value_matrix(self, pieces_matrix):
        # counts each empty square as 0 and each full one as 1 then sums them up to get total pieces
        # if total pieces less than or equal to 10: then late game
        if sum(int(isinstance(square, Piece)) for square in iter_chain(pieces_matrix)) <= 10:
            self.value_matrix = self.value_matrix_late
        # else early game
        else:
            self.value_matrix = self.value_matrix_early

    # this generates the movement vectors for the king
    def generate_movement_vectors(self, pieces_matrix, position_vector):
        # take the opportunity to update the value matrix
        self.update_value_matrix(pieces_matrix)

        # all 8 movement vectors
        unit_vectors = (Vector(i, j) for i, j in iter_product((-1, 0, 1), (-1, 0, 1)) if i != 0 or j != 0)

        # for each movement vector, get the resultant vector
        for movement_vector in unit_vectors:
            resultant_vector = position_vector + movement_vector

            # examine contents of square and use switch case to decide behaviour
            match self.examine_position_vector(position_vector=resultant_vector, pieces_matrix=pieces_matrix):
                case 'illegal':
                    continue
                case 'ally':
                    continue
                case 'enemy':
                    # this is a valid move
                    yield movement_vector
                case 'empty':
                    # is valid
                    yield movement_vector


# used by other modules to convert symbol to piece
PIECE_TYPES = {
    'P': Pawn,
    'N': Knight,
    'B': Bishop,
    'R': Rook,
    'K': King,
    'Q': Queen
}

# if __name__ == '__main__':
# ensures that all classes are valid (not missing any abstract properties) whenever the module is imported
Pawn('W')
Knight('W')
Bishop('W')
Rook('W')
Queen('W')
King('W')
