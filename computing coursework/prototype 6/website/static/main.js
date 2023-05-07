// these constants define the colors of text, squares and text shadow throughout the program 
const white_sq_bg_color = '#f5e6bf';
// const white_sq_bg_color = '#d9cba7';
const black_sq_bg_color = '#66443a';
const white_piece_color = '#ffffff';
const black_piece_color = '#000000';
// const white_shadow = '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
const black_shadow = '-1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff'
const white_shadow = '-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000'
// const black_shadow = '-2px -2px 0 #fff, 2px -2px 0 #fff, -2px 2px 0 #fff, 2px 2px 0 #fff'


// this function created a series of div tags that represent the individual squared in the chess board
// it decides their color, position vector and hence their ID and click event functions
function create_board_widget() {
    let board = document.getElementById("board");
    for (let row = 0; row <= 7; row++) {
        for (let col = 0; col <= 7; col++) {
            let i = col;
            let j = 7-row;

            // if row and column are both odd or both even then white, so add together and check if even
            let sum_is_even = ((row + col) % 2 == 0);
            // console.log(`square (${i},${j}), sum is even -->  ${sum_is_even}`)
            let square_bg_color = sum_is_even ? white_sq_bg_color : black_sq_bg_color;
            let square = document.createElement("div");
            // square.textContent = `(${i},${j})`;
            square.id = `square_${i}${j}`;

            square.classList.add("square");
            square.style.backgroundColor = square_bg_color;
            square.addEventListener("click", function(){handle_square_click(i, j)})
            board.append(square)
        }
    }
}

// this function returns the html element of a square given a position vector 
function get_square_at_vector(v) {
    let [i, j] = v;
    let id = `square_${i}${j}`;
    let square = document.getElementById(id);
    return square;
}


// this function uses the pieces matrix from the board object to populate the board and its squares with pieces
// it must decide their color and text shadow as well
function add_pieces(board) {
    let pieces_matrix = board.pieces_matrix
    // iterate through rows and columns
    for (let row = 0; row <= 7; row++) {
        for (let col = 0; col <= 7; col++) { 
            // get the vector and decide the color   
            let [i, j] = [col, 7-row]
            let [color_char, symbol] = pieces_matrix[row][col];
            let color = (color_char == "W") ? white_piece_color : black_piece_color;

            // console.log(`get_square_at_vector([i, j])   --->   get_square_at_vector(${[i, j]})   --->   ${get_square_at_vector([i, j])}`)
            square = get_square_at_vector([i, j]);

            // square.innerText = `(${i}, ${j})`;
            // square.style.fontSize = "20px"
            square.innerText = symbol;
            square.style.color = color; 
            square.style.textShadow = (color_char == "W") ? white_shadow : black_shadow;
            square.style.fontSize = "9vmin"

        }
    }
}

// this function uses the highlighted squares method of the board object to add highlighting to the chess board
// this highlights clicked pieces red and squares they can move to green
function add_highlighting(board) {
    let new_highlighting = board.get_highlighted_squares()
    // console.log(`add_highlighting function called with ${new_highlighting}`)

    // iterate through the position vectors and colors form the get_highlighted_squares method
    for (let i in new_highlighting) {
        let [vector, color] = new_highlighting[i];

        // console.log(`Adding ${color} to square at vector ${vector}`);

        square = get_square_at_vector(vector);
        // console.log({ vector })
        // console.log({ square })
        // if (square.innerText == null) {

        // if a square should be highlighted but is empty: add a center dot
        if (square.innerText.trim() == "") {
            square.innerText = "·";
            // square.style.fontSize = "20vmin";
            square.style.fontSize = "10vmin";
        }
        square.style.color = color;
        // square.style.backgroundColor = color;
    }
}

// this function was not needed in the end
// if wipes the board of all pieces and highlighting
function clear_board() {
    for (let i = 0; i <= 7; i++) {
        for (let j = 0; j <= 7; j++) {
            square = get_square_at_vector([i, j]);
            // console.log(`Square at vector (${[i, j]}) is ${square}`);
            square.textContent = "";
            // square.innerText = "";
            square.style.color = "black";
            square.style.textShadow = "";
            square.style.fontSize = "9vmin"
        }
    }
}

// this function updates the main title widget with a new title based on the board object
function update_main_title(board, manual_new_title=null) {

    if (manual_new_title !== null) {
        document.getElementById("top_title").innerText = manual_new_title
        return null;
    }


    let title_msg

    if (board.just_conceded) {
        // console.log({board})
        // console.log(JSON.stringify(board))
        // console.log(board.just_conceded)
        title_msg = "Game Over: You Conceded"
    }
    else {
        title_msg = `${(board.next_to_go === "W") ? "Your Go:" : "Computer's Go... (please wait)"}${(board.check) ? "   (CHECK)" : ""}`
    }

    document.getElementById("top_title").innerText = title_msg
}



// this function adds the pieces taken data (number and specific pieces) to the table
function update_pieces_taken(board) {

    let num_B_taken = board.pieces_taken.B.length
    let num_W_taken = board.pieces_taken.W.length
    let B_pieces_conjugation = (num_B_taken == 1) ? "Piece": "Pieces"    
    let W_pieces_conjugation = (num_W_taken == 1) ? "Piece": "Pieces"    

    document.getElementById("num_pieces_taken_black").innerText = (num_B_taken > 0) ? `${num_B_taken} ${B_pieces_conjugation} Taken`: "No Pieces Taken";
    document.getElementById("num_pieces_taken_white").innerText = (num_W_taken > 0) ? `${num_W_taken} ${W_pieces_conjugation} Taken` : "No Pieces Taken";

    // document.getElementById("which_pieces_taken_black").innerText = (board.pieces_taken.B.length > 0) ? `Pieces Lost: ${board.pieces_taken.B.map(x => x[1]).join(", ")}`: "-";
    document.getElementById("which_pieces_taken_black").innerText = (board.pieces_taken.B.length > 0) ? `${board.pieces_taken.B.map(x => x[1]).join(", ")}`: "-";
    // document.getElementById("which_pieces_taken_white").innerText = (board.pieces_taken.W.length > 0) ? `Pieces Lost: ${board.pieces_taken.W.map(x => x[1]).join(", ")}`: "-";
    document.getElementById("which_pieces_taken_white").innerText = (board.pieces_taken.W.length > 0) ? `${board.pieces_taken.W.map(x => x[1]).join(", ")}`: "-";
}

// this function auto selects one of the difficulty radio buttons
function set_selected_difficulty(board) {
    let difficulty = board.difficulty
    // console.log({difficulty})

    document.querySelector(`input[value=${difficulty}]`).checked = true;
    // document.querySelector(`input[value="${difficulty}"]`).checked = true;
    // document.querySelector(`input[value=${difficulty}]`).checked = true;
}



// this function adds moves to the move history table
function set_widget_move_history(board) {
    let moves = board.move_history.length;

    let rows
    let move_history_output = Array.from(board.move_history)
    // depending on the number of moves made in the game, extra cells may need to be added to make the table look right
    if (moves == 0) {
        rows = 1;
        move_history_output.push("-")
        move_history_output.push("-")
    }
    else if (moves % 2 == 0) {
        rows = moves / 2
    }
    else {
        rows = (moves + 1) / 2
        move_history_output.push("-")
    }
    // console.log({half_moves_rounded_up});
    // have a row for each number in half_moves_rounded_up


    // delete old elements from the table
    let old_rows = Array.from(document.querySelectorAll('.temporary_previous_moves_table_item'));

    if (old_rows.length > 0) {
        for (let i in old_rows) {
            old_rows[i].removeChild(old_rows[i].firstChild);
            old_rows[i].removeChild(old_rows[i].firstChild);
            old_rows[i].parentNode.removeChild(old_rows[i]);
        }
    }

    // iterate through the rows and add new TD tags to add the new row to the table
    table = document.getElementById("pieces_taken_table_table_tag")
    // console.log({table})

    let white_move
    let black_move
    let new_row
    let cells
    for (let r=0; r<rows; r++) {
        white_move = move_history_output[2*r];
        black_move = move_history_output[1+ 2*r];

        new_row = document.createElement("tr")
        cells = [
            document.createElement("td"),
            document.createElement("td")
        ]

        cells[0].innerText = white_move;
        cells[1].innerText = black_move;

        new_row.classList.add("temporary_previous_moves_table_item")
        cells[0].classList.add("small_text")
        cells[1].classList.add("small_text")


        new_row.appendChild(cells[0]);
        new_row.appendChild(cells[1]);

        table.appendChild(new_row)

    }
}



// gets the hash of a given piece of data
// https://stackoverflow.com/questions/54701686/matching-cryptojs-sha256-with-hashlib-sha256-for-a-json
function get_hash_of_data(data, stringify = true) {
    let data_string
    if (stringify) {
        data_string = JSON.stringify(data)
    }
    else {
        data_string = data
    }
    
    return CryptoJS.SHA256(data_string).toString(CryptoJS.enc.Base64);
}

// holds a table that keep track of the hashes of various items of data
// includes data item name as a key and current hash + function to find hash as values
previous_data_hashes = {
    pieces_taken: [null, (board) => get_hash_of_data(board.pieces_taken)],
    move_history: [null, (board) => get_hash_of_data(board.move_history)],
    piece_layout: [null, (board) => get_hash_of_data([board.pieces_matrix, board.possible_to_vectors, board.selected_from_vector])],
    highlighting: [null, (board) => get_hash_of_data([board.possible_to_vectors, board.selected_from_vector])],
    difficulty: [null, (board) => get_hash_of_data(board.difficulty, stringify=false)]
};

// this function only runs the DOM update method given if the data to display changed 
function update_as_necessary(board, update_function, hashes_table_key) {
    // create a new hash
    // only if it is different from the old hash, then update the board and the hash in the data previous_data_hashes object

    // console.log(previous_data_hashes[hashes_table_key])
    let [old_hash, compute_hash] = previous_data_hashes[hashes_table_key];
    let new_hash = compute_hash(board);

    if (new_hash !== old_hash) {
        // console.log(`hashes are different, updating ${hashes_table_key}`)
        previous_data_hashes[hashes_table_key][0] = new_hash
        update_function(board)
    }
    // else {
    //     console.log(`hashes the same, NOT updating ${hashes_table_key}`)
    // }
}



// update all dom widgets as necessary, always update title
function update_board_widget(board) {
    // clear_board();
    // console.log("board.pieces_matrix")
    // console.log(board.pieces_matrix)


    // add_pieces(board);
    // add_highlighting(board);
    // update_main_title(board);
    // set_selected_difficulty(board);
    // update_pieces_taken(board);
    // set_widget_move_history(board);

    update_main_title(board);
    update_as_necessary(board, add_pieces, "piece_layout")
    update_as_necessary(board, add_highlighting, "highlighting")
    update_as_necessary(board, set_selected_difficulty, "difficulty")
    update_as_necessary(board, update_pieces_taken, "pieces_taken")
    update_as_necessary(board, set_widget_move_history, "move_history")
}


// calls teh appropriate square click function on the board and then updates the DOM
function handle_square_click(i, j) {

    // board is a global variable
    // console.log(`Square at (${i}, ${j}) has been clicked`);
    board.handle_square_click([i, j]);
    // console.log(board.pieces_matrix);

    // update_board_widget(board);

    // alert("about to clear board");
    // clear_board();
}



// whole file loads after html

// create chess board html element
create_board_widget();

// create board class
let board = new Chess_Board(
    update_board_widget,
    update_main_title
);

// bind buttons to methods of the board class
document.getElementById("restart_button").addEventListener("click", function () {
    board.reset_game()
})
document.getElementById("concede_button").addEventListener("click", function () {
    // update_main_title(null, "You Conceded The Game")
    board.concede_game()
})

// bind a change to the radio buttons to a handler method in the board class
function handle_radio_button_click(radio_button) {
    let new_difficulty = radio_button.value;
    if (new_difficulty !== board.difficulty) {
        // console.log(`Setting new difficulty to ${new_difficulty}`)
        board.change_difficulty(new_difficulty);
    }
}

// before letting the window close, send the server a warning so it can save the game
// also produces a pop up box to prevent accidental closing of the game
window.onbeforeunload = () => fetch('/stop_and_save_game');

