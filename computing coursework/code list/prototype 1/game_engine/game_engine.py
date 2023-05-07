# the data class library is used to minimize boiler plate code in defining __init__ and __eq__ methods for classes 
from dataclasses import dataclass
# this is used to make a complete and distinct coppy of a 2d array so changes to the original don't affect the coppy
from copy import deepcopy

# this is a class to represent the game state
# its attributes cannot be altered after it is initialized (immutable).
# instead changes to the game state, such as a move, are handled as new game state objects
@dataclass(frozen=True)
class Game_State:
    # there variables hold the data relevant to a game state
    board_positions: list[list]
    moves_left: int
    to_go_next: str
    
    # used for debugging so that the game state can be represented in the console.
    def print_board(self):
        for row in self.board_positions:
            print("|".join(["." if e == "" else e for e in row]))
    

    def is_game_over(self):
        """Returns False, none for still going and True, 1/0/-1 for over.
        1 is user wins, 0 is draw, -1 is user looses"""
        # internal function as it only used here
        # yields all of the sequences of 3 squares
        def gen_triplets():
            # yield rows
            yield from self.board_positions
            # yield columns
            for col in range(3):
                yield [self.board_positions[row][col] for row in range(3)]
            # yield diagonals
            yield [
                self.board_positions[0][0],
                self.board_positions[1][1],
                self.board_positions[2][2],
            ]
            yield [
                self.board_positions[2][0],
                self.board_positions[1][1],
                self.board_positions[0][2],
            ]
        # if there is a sequence that is 3 in a row return True and 1 or -1 for win or loss (user perspective)
        if ["X"]*3 in gen_triplets():
            return True, 1
        if ["O"]*3 in gen_triplets():
            return True, -1
        # note so long as user takes all odd turns 9,7,...3,1 they will have last go so redundant in theory
        # but I left it in incase the code needs to be extended in future
        if self.moves_left == 0:
            return True, 0
        # if not already determined otherwise then the game isn't over
        return False, None

    # this function iterates through and yields the game states that could result form all possible moves on the current game state
    def gen_child_game_states(self):
        """precondition of game not being over"""
        # for each square
        for i, row in enumerate(self.board_positions):
            for j, square in enumerate(row):
                # if the square is empty
                if square == "":
                    # make a coppy of the boards state where the next to move moved there
                    new_board_positions = deepcopy(self.board_positions)
                    new_board_positions[i][j] = self.to_go_next
                    
                    # yield this as a new game state where the user is next to 
                    yield Game_State(
                        board_positions=new_board_positions,
                        moves_left=self.moves_left-1,
                        to_go_next="X" if self.to_go_next == "O" else "O"
                    )
                # else continue to next iteration

# this is so called as it used the minimax algorithm along with alpha beta pruning to navigate the decision tree
# the british museum algorithm is an approach where you explore the tree fully 
# until all terminal nodes are game states where the game is over
# this function returns 2 values, the score and game state object for the best child game state (corresponds to best move)
def british_museum_minimax(game_state: Game_State, maximizing_player:bool, alpha, beta):
    # computer want 0 or -1 so minimizer
    # this is the base case to the recursive function (stop at terminal nodes)
    over, outcome = game_state.is_game_over()
    if over:
        return outcome, game_state

    # recursive case
    best_child= None    

    # even though the initial call is for the servers move (minimizer), recursive calls may be form maximizer
    # I will explain the logic in more depth for the maximizing player
    if maximizing_player:
        # meant to represent negative infinity (arbitrary bad so it is replaced by the best evaluation)
        max_evaluation = -100
        # for each possible game state
        for child in game_state.gen_child_game_states():
            # recursive class to function to evaluate child node 
            # now minimizing player 
            # index for fist element as I only case about score not the actual game state
            evaluation = british_museum_minimax(
                game_state=child,
                maximizing_player=not maximizing_player,
                alpha=alpha,
                beta=beta,
            )[0]
            # max_evaluation = max(max_evaluation, evaluation)
            # if this evaluation is the best so far
            if evaluation > max_evaluation:
                # update the max evaluation and best child (only for this call)
                max_evaluation = evaluation
                best_child = child
                # update the alpha value to represent the best that the maximizing player can get
                alpha = max(alpha, evaluation)

            # if the minimizing player can do better (for them less) than alpha then they have a better option
            # this means that that this won't be the best child of the earlier call 
            # (the minimizer wouldn't need to give the maximizer such a good score)
            if beta <= alpha:
                break
        # return the best child game state and its score
        return max_evaluation, best_child
    # similar for minimizer
    else:
        min_evaluation = 100
        for child in game_state.gen_child_game_states():
            evaluation = british_museum_minimax(
                game_state=child,
                maximizing_player=not maximizing_player,
                alpha=alpha,
                beta=beta,
            )[0]
            # min_evaluation = min(min_evaluation, evaluation)
            if evaluation < min_evaluation:
                min_evaluation = evaluation
                best_child = child
                beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation, best_child

# this main function is an easier wrapper for the app module to use
# it only determines and returns the best child (servers best move)
def main(game_state: Game_State):
    # output for debugging
    print("selecting best move from this game state:")
    game_state.print_board()
    
    # call the recursive function to determine the best child (and score for debugging)
    # start with arbitrarily low alpha value and high beta value
    score, best_child = british_museum_minimax(
        game_state=game_state,
        maximizing_player=False,
        alpha=-100,
        beta=+100
    )
    # more output for debugging
    print("best move is:")
    best_child.print_board()
    print(f"with a guaranteed score of {score} or better (minimizer)")

    # return the best child
    return best_child
    