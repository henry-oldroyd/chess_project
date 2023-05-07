# import local modules
# cannot import game as causes circular import, if necessary put in same file
from board_state import Board_State
from assorted import ARBITRARILY_LARGE_VALUE
from vector import Vector

# my minimax function takes as arguments:
# Board_State, is_maximiser, alpha and beta (used for pruning) and check_extra_depth (produces better outcome but slower)
# it returns
# score, child, move

def minimax(board_state: Board_State, is_maximizer: bool, depth, alpha, beta, check_extra_depth=True):
    # sourcery skip: low-code-quality, remove-unnecessary-else, swap-if-else-branches
    # assume white is maximizer
    # when calling, if give appropriate max min arg
    
    # base case 
    # if over or depth==0 return static evaluation
    over, _ = board_state.is_game_over_for_next_to_go()
    if depth == 0 or over:
        # special recursive case 1
        # examine terminal nodes that are check to depth 2 (variable depth)

        # to avoid goose chaises, extra resources are allowed if check not already explored
        if board_state.color_in_check() and check_extra_depth and not over:
            # print(f"checking board state {hash(board_state)} at additional depth due to check")
            return minimax(
                board_state=board_state,
                is_maximizer=is_maximizer,
                depth=2,
                alpha=alpha,
                beta=beta,
                check_extra_depth=False
            )
        else:
            # static eval works for game over to
            return board_state.static_evaluation(), None, None

    # define variables used to return more that just score (move and child)
    best_child_game_state: Board_State | None = None
    best_move_vector: Vector | None = None

    # function yields move ordered by how favorable they are (low depth minimax approximation)
    def gen_ordered_child_game_states():
        # this function does a low depth minimax recursive call (special recursive case 2) to give a move a score
        def approx_score_move(move):
            child_game_state = board_state.make_move(*move)

            return minimax(
                board_state=child_game_state,
                depth=depth-2,
                is_maximizer=not is_maximizer,
                alpha=alpha,
                beta=beta,
                check_extra_depth=False
            )[0]
            # print(f"approx_score_move(move={move!r})  ->  {result!r}")

        # if depth is 1 or less just yield moves form legal moves
        if depth <= 1 :
            yield from board_state.generate_legal_moves()
        # else sort them
        else:
            # sort best to worse
            # sort ascending order if minimizer, descending if maximizer
            yield from sorted(
                board_state.generate_legal_moves(),
                key=approx_score_move,
                reverse=is_maximizer
            )




    
    if is_maximizer:
        # set max to -infinity
        maximum_evaluation = (-1)*ARBITRARILY_LARGE_VALUE

        # iterate through moves and resulting game states
        for position_vector, movement_vector in gen_ordered_child_game_states():
            child_game_state = board_state.make_move(from_position_vector=position_vector, movement_vector=movement_vector)

            # evaluate each one
            # general recursive case 1
            evaluation, _, _ = minimax(
                board_state=child_game_state,
                is_maximizer=not is_maximizer,
                depth=depth-1,
                alpha=alpha,
                beta=beta,
                check_extra_depth=check_extra_depth
            )

            # update alpha and max evaluation
            if evaluation > maximum_evaluation:
                maximum_evaluation = evaluation
                best_child_game_state = child_game_state
                best_move_vector = (position_vector, movement_vector)
                alpha = max(alpha, evaluation)

            # where possible, prune
            if beta <= alpha:
                # print("Pruning!")
                break
        # once out of loop, return result
        return maximum_evaluation, best_child_game_state, best_move_vector

    else:
        minimum_evaluation = ARBITRARILY_LARGE_VALUE

        for position_vector, movement_vector in gen_ordered_child_game_states():
            child_game_state = board_state.make_move(from_position_vector=position_vector, movement_vector=movement_vector)
            evaluation, _, _ = minimax(
                board_state=child_game_state,
                is_maximizer=not is_maximizer,
                depth=depth-1,
                alpha=alpha,
                beta=beta,
                check_extra_depth=check_extra_depth
            )

            if evaluation < minimum_evaluation:
                minimum_evaluation = evaluation
                best_child_game_state = child_game_state
                best_move_vector = (position_vector, movement_vector)
                beta = min(beta, evaluation)

            if beta <= alpha:
                # print("Pruning!")
                break
        return minimum_evaluation, best_child_game_state, best_move_vector
