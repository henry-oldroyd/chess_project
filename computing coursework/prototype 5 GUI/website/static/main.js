// on load create chess board 

const white_sq_bg_color = '#f5e6bf';
// const white_sq_bg_color = '#d9cba7';
const black_sq_bg_color = '#66443a';
const white_piece_color = '#ffffff';
const black_piece_color = '#000000';
// const white_shadow = '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
const black_shadow = '-1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff'
const white_shadow = '-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000'
// const black_shadow = '-2px -2px 0 #fff, 2px -2px 0 #fff, -2px 2px 0 #fff, 2px 2px 0 #fff'


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

function get_square_at_vector(v) {
    let [i, j] = v;
    let id = `square_${i}${j}`;
    let square = document.getElementById(id);
    return square;
}

function add_pieces(board_array) {
    for (let row = 0; row <= 7; row++) {
        for (let col = 0; col <= 7; col++) {       
            let [i, j] = [col, 7-row]
            let [color_char, symbol] = board_array[row][col];
            let color = (color_char == "W") ? white_piece_color : black_piece_color;

            // console.log(`get_square_at_vector([i, j])   --->   get_square_at_vector(${[i, j]})   --->   ${get_square_at_vector([i, j])}`)
            square = get_square_at_vector([i, j]);

            // square.innerText = `(${i}, ${j})`;
            // square.style.fontSize = "20px"
            square.innerText = symbol;
            square.style.color = color; 
            square.style.textShadow = (color_char == "W") ? white_shadow : black_shadow;
            square.style.fontSize = "9vmin"


            // console.log(square.innerText.trim())
            // if (square.innerText.trim() === "·") {
            // if (square.textContent.trim() === "·") {
            // if (square.textContent.trim() == "·") {
            //     // console.log(`Removing center dot at vector (${[i, j]})`);
            //     remove_green_dot(square);
            // }
        }
    }
}

function add_highlighting(new_highlighting) {
    // console.log(`add_highlighting function called with ${new_highlighting}`)
    for (let i in new_highlighting) {
        let [vector, color] = new_highlighting[i];

        // console.log(`Adding ${color} to square at vector ${vector}`);

        square = get_square_at_vector(vector);
        // console.log({square})
        // if (square.innerText == null) {
        if (square.innerText.trim() == "") {
            square.innerText = "·";
            // square.style.fontSize = "20vmin";
            square.style.fontSize = "10vmin";
        }
        square.style.color = color;
        // square.style.backgroundColor = color;
    }
}

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


function update_board_widget(board) {
    // clear_board();
    add_pieces(board.board_positions);
    add_highlighting(board.get_highlighted_squares());
}

let board = new Chess_Board();

function handle_square_click(i, j) {
    console.log(`Square at (${i}, ${j}) has been clicked`);
    board.handle_square_click([i, j]);
    console.log(board.board_positions);
    update_board_widget(board);
    // alert("about to clear board");
    // clear_board();
}

create_board_widget();
update_board_widget(board);

