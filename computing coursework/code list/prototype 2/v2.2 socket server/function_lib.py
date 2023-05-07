from dataclasses import dataclass


@dataclass(frozen=True)
class Vector():
    i: int
    j: int

    def __add__(self, other):
        assert isinstance(other, Vector), "both objects must be instances of the Vector class"
        return Vector(
            i=self.i + other.i,
            j=self.j + other.j
        )
    
    def __mul__(self, multiplier):
        return Vector(
            i=self.i * multiplier,
            j=self.j * multiplier
        )
    
    def position_vector_in_board(self):
        """Assumes that the current represented vector is a position vector
        checks if it points to a square that isn't in the chess board"""
        return self.i in range(8) and self.j in range(8)
