# import json

from function_lib import Vector
from game_engine import Board_State


def test_gen_position_vectors():
    result_pawn_position_vectors = Board_State((
        (None, None, None, None, None, None, None, None),
        ('UP', 'UP', 'UP', 'UP', 'UP', 'UP', 'UP', 'UP'),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        ('CP', 'CP', 'CP', 'CP', 'CP', 'CP', 'CP', 'CP'),
        (None, None, None, None, None, None, None, None)
    )).pawn_position_vector_generator()


    expected_pawn_position_vector = (
        Vector(0, 1),
        Vector(1, 1),
        Vector(2, 1),
        Vector(3, 1),
        Vector(4, 1),
        Vector(5, 1),
        Vector(6, 1),
        Vector(7, 1)
    )

    assert sorted(result_pawn_position_vectors, key=repr) == sorted(expected_pawn_position_vector, key=repr)


def test_take_vectors():

    legal_moves = Board_State((
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, "UP", None),
        (None, None, None, "UP", None, None, "CP", "CP"),
        (None, None, "CP", None, "CP", None, None, None),
        ("CP", None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None)
    )).legal_moves_generator()


    expected_legal_moves = (
        (Vector(0, 2), Vector(0, 3)),
        (Vector(2, 3), Vector(2, 4)),
        (Vector(2, 3), Vector(3, 4)),
        (Vector(4, 3), Vector(4, 4)),
        (Vector(4, 3), Vector(3, 4)),
        (Vector(7, 4), Vector(7, 5)),
        (Vector(7, 4), Vector(6, 5)),
    )

    assert sorted(legal_moves, key=repr) == sorted(expected_legal_moves, key=repr)


def test_legal_moves_initial_positions():

    legal_moves = Board_State((
        (None, None, None, None, None, None, None, None),
        ('UP', 'UP', 'UP', 'UP', 'UP', 'UP', 'UP', 'UP'),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        ('CP', 'CP', 'CP', 'CP', 'CP', 'CP', 'CP', 'CP'),
        (None, None, None, None, None, None, None, None)
    )).legal_moves_generator()


    expected_legal_moves = (
        (Vector(0, 1), Vector(0, 2)),
        (Vector(1, 1), Vector(1, 2)),
        (Vector(2, 1), Vector(2, 2)),
        (Vector(3, 1), Vector(3, 2)),
        (Vector(4, 1), Vector(4, 2)),
        (Vector(5, 1), Vector(5, 2)),
        (Vector(6, 1), Vector(6, 2)),
        (Vector(7, 1), Vector(7, 2)),
    )


    assert sorted(legal_moves, key=repr) == sorted(expected_legal_moves, key=repr)


def test_legal_moves_random_positions():

    legal_moves = Board_State((
            (None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, 'CP'),
            (None, None, None, 'CP', None, None, 'CP', None),
            (None, None, None, None, 'CP', None, None, None),
            (None, 'CP', None, None, None, None, None, None),
            ('CP', None, 'CP', None, None, 'CP', None, None),
            (None, None, None, None, None, None, None, None)
    )).legal_moves_generator()


    expected_legal_moves = (
        (Vector(0, 1), Vector(0, 2)),
        (Vector(1, 2), Vector(1, 3)),
        (Vector(2, 1), Vector(2, 2)),
        (Vector(3, 4), Vector(3, 5)),
        (Vector(4, 3), Vector(4, 4)),
        (Vector(5, 1), Vector(5, 2)),
        (Vector(6, 4), Vector(6, 5)),
        (Vector(7, 5), Vector(7, 6))
    )

    assert sorted(legal_moves, key=repr) == sorted(expected_legal_moves, key=repr)


def test_execute_move():

    resulting_game_state = Board_State((
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, 'CP'),
        (None, None, None, 'CP', None, None, 'CP', None),
        (None, None, None, None, 'CP', None, None, None),
        (None, 'CP', None, None, None, None, None, None),
        ('CP', None, 'CP', None, None, 'CP', None, None),
        (None, None, None, None, None, None, None, None)
    )).execute_move(
        Vector(0, 1),
        Vector(0, 2)
    )

    expected_game_state = Board_State((
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, None, 'CP'),
        (None, None, None, 'CP', None, None, 'CP', None),
        (None, None, None, None, 'CP', None, None, None),
        ('CP', 'CP', None, None, None, None, None, None),
        (None, None, 'CP', None, None, 'CP', None, None),
        (None, None, None, None, None, None, None, None)
    ))

    assert resulting_game_state == expected_game_state
