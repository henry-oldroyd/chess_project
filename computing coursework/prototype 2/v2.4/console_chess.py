from game import Game
from assorted import InvalidMove
import pieces as pieces_mod
from board_state import Board_State

# create new chess game
# difficulty set to depth 2
game = Game(depth=2)

# pieces_matrix = (
#     (None, None, None, None, None, None, pieces_mod.King("B"), pieces_mod.Rook("B")),
#     (None, None, None, None, None, pieces_mod.Pawn("B"), pieces_mod.Pawn("B"), pieces_mod.Pawn("B")),
#     (None, None, None, None, None, None, None, None),
#     (None, None, None, None, None, None, None, None),
#     (None, None, None, None, None, None, None, None),
#     (None, None, None, None, None, None, None, None),
#     (None, None, None, None, None, None, None, None),
#     (None, None, None, pieces_mod.Rook("W"), None, None, None, None),
# )

pieces_matrix = (
    (None, None, None, pieces_mod.Rook("B"), None, None, None, None),
    (None, None, None, None, None, None, None, None),
    (None, None, None, None, None, None, None, None),
    (None, None, None, None, None, None, None, None),
    (None, None, None, None, None, None, None, None),
    (None, None, None, None, None, None, None, None),
    (None, None, None, None, None, pieces_mod.Pawn("W"), pieces_mod.Pawn("W"), pieces_mod.Pawn("W")),
    (None, None, None, None, None, pieces_mod.King("W"), None, pieces_mod.Rook("W")),
)

game.board_state = Board_State("W", pieces_matrix)

# this function informs the user of the details when the game is over
def handle_game_over(winner, classification):
    print(f"The game is over, the {'user' if winner==1 else 'computer'} has won in a {classification}")

# print out the starting board
game.board_state.print_board()
print()

# keep game going until loop broken
while True:
    # user goes first
    print("Your go USER:")

    # while loop and error checking used to ensure move input
    while True:
        try:
            print("Please enter move in 2 parts")
            from_square = input("From square:  ")
            to_square = input("To square:   ")
            # check
            game.implement_user_move(from_square, to_square)
        except InvalidMove:
            print("This isn't a legal move, try again")
        except ValueError:
            print("This isn't valid input, try again")
        else:
            # if it worked break out of the loop
            break
    
    # if move results in check then output this
    if game.board_state.color_in_check():
            print("CHECK!")
    # print out the current board_state
    game.board_state.print_board()
    print()
    
    # check if game over after user's move
    over, winner, classification = game.check_game_over()   
    # if over, handle it.
    if over:
        handle_game_over(winner=winner, classification=classification)
        break

    # alternate, it is now the computers go
    print("Computer's go: ")
    
    # get the computers move
    move, _ = game.implement_computer_move()
    
    # print out the board again
    game.board_state.print_board()
    
    # print out the computer's move in terms of squares
    position_vector, movement_vector = move
    resultant_vector = position_vector + movement_vector
    piece_symbol = game.board_state.get_piece_at_vector(resultant_vector).symbol()
    print(f"Computer Moved  {piece_symbol}:  {position_vector.to_square()} to {resultant_vector.to_square()}")
    
    # print check if applicable
    if game.board_state.color_in_check():
            print("CHECK!")
    
    # check if the game is over, if so handle it 
    over, winner, classification = game.check_game_over()
    if over:
        handle_game_over(winner=winner, classification=classification)
        break
    # create a new line to separate for the user's next move
    print()
