# import dataclass to reduce boilerplate code
from dataclasses import dataclass

from assorted import cache_decorator


# frozen = true means that the objects will be immutable 
@dataclass(frozen=True)
class Vector():
    # 2d vector has properties i and j
    i: int
    j: int


    # code to allow for  +  -  and  *  operators to be used with vectors

    @cache_decorator
    def __add__(self, other):
        assert isinstance(other, Vector), "both objects must be instances of the Vector class"
        return Vector(
            i=self.i + other.i,
            j=self.j + other.j
        )

    @cache_decorator
    def __sub__(self, other):
        assert isinstance(other, Vector), "both objects must be instances of the Vector class"
        return Vector(
            i=self.i - other.i,
            j=self.j - other.j
        )

    @cache_decorator
    def __mul__(self, multiplier: int | float):
        return Vector(
            i=int(self.i * multiplier),
            j=int(self.j * multiplier)
        )

    # check if a vector is in board
    @cache_decorator
    def in_board(self):
        """Assumes that the current represented vector is a position vector
        checks if it points to a square that isn't in the chess board"""
        return self.i in range(8) and self.j in range(8)
    

    # alternative way to create instance, construct from chess square
    @classmethod
    @cache_decorator
    def construct_from_square(cls, to_sqr):
        """Example from and to squares are A3 -> v(0, 2) and to B4 -> v(1, 3)"""
        to_sqr = to_sqr.upper()
        letter, number = to_sqr

        # map letters and numbers to 0 to 7 and create new vector object
        return cls(
            i=ord(letter.upper()) - ord("A"),
            j=int(number)-1
        )

    # this function is the reverse and converts a position vector to a square
    @cache_decorator
    def to_square(self) -> str:
        letter = chr(self.i + ord("A"))
        number = self.j+1
        return f"{letter}{number}"

    @cache_decorator
    def magnitude_and_unit_vector(self):
        def sqrt(x):
            return x**(1/2)
        def square(x):
            return x**2
        
        magnitude: float = sqrt(square(self.i) + square(self.j))
        # unit_vector: Vector = self.__mul__(1/magnitude)
        # return magnitude, unit_vector

        return magnitude

    # this function checks if 2 vectors are equal
    def __eq__(self, other) -> bool:
        try:
            # assert same subclass like rook
            assert isinstance(other, type(self))
            assert self.i == other.i
            assert self.j == other.j

        except AssertionError:
            return False
        else:
            return True

    # used to put my objects in set
    def __hash__(self):
        return hash((self.i, self.j))