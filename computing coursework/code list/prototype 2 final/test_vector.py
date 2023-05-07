import ddt
import unittest

# from vector.vector import Vector
from vector import Vector

# function for path to vector related test data
def test_path(file_name): 
    return f"./test_data/vector/{file_name}.yaml"

# augment my test case class with ddt decorator
@ddt.ddt
class Test_Case(unittest.TestCase):
    
    # performs many checks of construct form square
    @ddt.file_data(test_path("from_square"))
    def test_square_to_vector(self, square, expected_vector):
        self.assertEqual(
            Vector.construct_from_square(square),
            Vector(*expected_vector),
            msg=f"\nVector.construct_from_square('{square}')  !=  Vector(i={expected_vector[0]}, j={expected_vector[1]})"
        )
    
    # performs many checks of adding vectors
    @ddt.file_data(test_path("vector_add"))
    def test_add_vectors(self, vector_1, vector_2, expected_vector):
        self.assertEqual(
            Vector(*vector_1) + Vector(*vector_2),
            Vector(*expected_vector),
            msg=f"\nVector(*{vector_1}) + Vector(*{vector_2})  !=  Vector(*{expected_vector})"
        )
    
    # performs many checks of multiplying vectors
    @ddt.file_data(test_path("vector_multiply"))
    def test_multiply_vectors(self, vector, multiplier, expected):
        self.assertEqual(
            Vector(*vector) * multiplier,
            Vector(*expected)
        )

    # many tests of vector in board
    @ddt.file_data(test_path("vector_in_board"))
    def test_in_board(self, vector, expected):
        self.assertEqual(
            Vector(*vector).in_board(),
            expected,
            msg=f"\nVector(*{vector}).in_board()  !=  {expected}"
        )

    # many tests of vector out of board
    @ddt.file_data(test_path('vector_to_square'))
    def test_to_square(self, vector, expected):
        self.assertEqual(
            Vector(*vector).to_square(),
            expected
        )

# if __name__ == '__main__':
#     unittest.main()