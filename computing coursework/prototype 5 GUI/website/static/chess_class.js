const pieces = {
    pawn: '♟︎',
    king: '♚',
    queen: '♛',
    rook: '♜',
    bishop: '♝',
    knight: '♞',
};


let other_row = [
    pieces.rook,
    pieces.knight,
    pieces.bishop,
    pieces.queen,
    pieces.king,
    pieces.bishop,
    pieces.knight,
    pieces.rook,
];


let starting_board_positions = [
    [[], []],
    [[], []],
]


starting_board_positions[0] = other_row.map(function (piece) { return ['B', piece] });
starting_board_positions[1] = Array(8).fill(null).map(function (x) { return ['B', pieces.pawn] });
// starting_board_positions[1] = Array(8).fill(['B', pieces.pawn, null]);
for (let i = 2; i <= 5; i++) {
    starting_board_positions[i] = Array(8).fill(null).map(function (x) { return [null, null] });
    // starting_board_positions[i] = Array(8).fill([null, null, null]); 
}
starting_board_positions[6] = Array(8).fill(null).map(function (x) { return ['W', pieces.pawn] });
// starting_board_positions[6] = Array(8).fill(['W', pieces.pawn, null]);
starting_board_positions[7] = other_row.map(function (piece) { return ['W', piece] });


let starting_legal_moves = [];

// add position and movement vectors of knights
starting_legal_moves.push([[1, 0], [1, 2]]);
starting_legal_moves.push([[1, 0], [-1, 2]]);
starting_legal_moves.push([[6, 0], [1, 2]]);
starting_legal_moves.push([[6, 0], [-1, 2]]);


for (let i = 0; i <= 7; i++) {
    starting_legal_moves.push([[i, 1], [0, 1]])
    starting_legal_moves.push([[i, 1], [0, 2]])
}

function arrays_are_equal(a1, a2) {
    return JSON.stringify(a1) == JSON.stringify(a2)
}

function two_d_array_contains_sub_array(two_d_array, sub_array) {
    for (let i in two_d_array) {
        if (arrays_are_equal(two_d_array[i], sub_array)) {
            return true;
        }
    }
    return false;

}

// console.log({starting_board_positions});
// console.log({starting_legal_moves});

let socket = io();

function external_get_computers_move(chess_board) {
    // gives computers move, new board and new legal moves
    return null;
}

function external_get_game_over(chess_board) {
    return null;
}


class Chess_Board {
    constructor() {
        this.reset_default_start_of_game();
    };

    reset_default_start_of_game() {
        this.possible_to_vectors = [];
        this.selected_from_vector = null;
        this.board_positions = starting_board_positions;
        this.legal_moves = starting_legal_moves;
        this.user_input_disabled = false;
    }

    make_move(from_vector, to_vector) {
        console.log(`making move from (${from_vector}) to (${to_vector})`)
        let [to_i, to_j] = to_vector;
        let [from_i, from_j] = from_vector;

        let [to_row, to_col] = [7 - to_j, to_i];
        let [from_row, from_col] = [7 - from_j, from_i];

        let piece = this.board_positions[from_row][from_col];
        this.board_positions[from_row][from_col] = [null, null];
        this.board_positions[to_row][to_col] = piece;

        this.selected_from_vector = null;
        this.possible_to_vectors = [];
    }

    handle_game_over(winner) {
        alert(`Game is over, ${winner} has won! (resetting board)`);
        this.reset_default_start_of_game();        
    }

    make_user_move(from_vector, to_vector) {
        // disable inputs
        this.user_input_disabled = true;
        // make user move
        this.make_move(from_vector, to_vector)
        // if game over, handle and end function
        let [is_over, winner] = external_get_game_over();
        if (is_over) {
            this.handle_game_over(winner);
            return null;
        }
        // then get computers move
        let [computer_move, new_legal_moves] = external_get_computers_move();
        let [from_vector, to_vector] = computer_move;

        // make computers move
        alert("Ready to see the computers move?")
        this.make_move(from_vector, to_vector)
        
        // if game over, handle and end function
        [is_over, winner] = external_get_game_over();
        if (is_over) {
            this.handle_game_over(winner);
            return null;
        }
        
        // cycle repeats so prepare for users next move
        this.legal_moves = new_legal_moves;
        this.user_input_disabled = false;
    }

    handle_square_click(vector) {
        if (!this.user_input_disabled) {
            return null;
        }
        // let from_square_already_selected = this.selected_from_vector !== null;
        let is_valid_move = two_d_array_contains_sub_array(this.possible_to_vectors, vector);
        console.log(`Checking if  [${vector}]  in  ${JSON.stringify(this.possible_to_vectors)}  -->  result was  ${is_valid_move}`);
        if (is_valid_move) {
            this.make_move(this.selected_from_vector, vector);
        }
        // else if not valid or no piece already selected then reselect
        else {
            // get piece at vector
            let [i, j] = vector;
            let [row, col] = [7-j, i];
            let [color, _] = this.board_positions[row][col];
            if (color == this.next_to_go) {
                this.selected_from_vector = vector;
            }
            else {
                this.selected_from_vector = null;
            }

            let position_vector; let movement_vector; let resultant_vector;
            this.possible_to_vectors = [];
            for (let i in this.legal_moves) {
                [position_vector, movement_vector] = this.legal_moves[i];
                if (arrays_are_equal(position_vector, vector)) {
                    resultant_vector = add_vectors(position_vector, movement_vector);
                    this.possible_to_vectors.push(resultant_vector);
                }
            }
        }
    }

    get_highlighted_squares() {
        // returns a 2d array of vector and then color
        let highlighted_squares = [];
        if (this.selected_from_vector !== null) {
            highlighted_squares.push([
                this.selected_from_vector,
                "red"
            ]);
            for (let i in this.possible_to_vectors) {
                highlighted_squares.push([
                    this.possible_to_vectors[i],
                    "green"
                ]);
            }
        } 
        // console.log({highlighted_squares})
        return highlighted_squares;
    }
    // is_move_valid(move) { return this.legal_moves.includes(move) };
}

