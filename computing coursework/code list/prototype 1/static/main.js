// create a socket object form the online socket library
let socket = io();

// global constants to show game state
let moves_left = 9;
let next_to_go= "X";
let board_positions= [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
];

// this function takes a row and column 1 to 3 and gives the html element
function get_square(row, col){
    // console.log('get_square called');
    // return document.querySelector(`#sq_${row.toString() + col.toString()}`);
    return document.getElementById(`sq_${row.toString() + col.toString()}`);
};

// this returns an array or all rows, columns and diagonals on the board for examination
function get_triplets(){
    triplets = []
    // push all rows
    for(i=0; i<=2; i++){
        triplets.push(board_positions[i])
    }
    // push all columns
    for(j=0; j<=2; j++){
        column = []
        for (i = 0; i <= 2; i++) {
            column.push(board_positions[i][j])
        }
        triplets.push(column);
    }
    // add diagonals
    triplets.push([board_positions[0][0], board_positions[1][1], board_positions[2][2]])
    triplets.push([board_positions[0][2], board_positions[1][1], board_positions[2][0]])
    return triplets
}

// changes the next to go to the next player based on current player
function toggle_next_to_go(){
    // console.log('toggle_next_to_go called');
    if(next_to_go === "X"){
        next_to_go = "O"
    }
    else {
        next_to_go = "X"
    }
};


// this function updates the table tag in html so the contents reflects the board positions array.
function update_widget(){
    // console.log("update_widget called");
    // console.log({board_positions})
    var row; var col;
    for (let i = 0; i <= 2; i++) {
        for (let j = 0; j <= 2; j++) {
            row=i+1; col=j+1;
            square = get_square(row, col);
            // console.log("changing content of this tag")
            // console.log(`square ${row.toString()} ${col.toString()}`)
            // console.log({square})
            // console.log(`to ${board_positions[i][j]}`)
            // square.innerText = board_positions[i][j];
            square.textContent = board_positions[i][j];
            // square.textContent = "Test";
        };
    };
};

// checks if the target square is empty and returns a boolean
function is_legal_move(row, col){
    // console.log("is_legal_move called");
    // console.log({row})
    // console.log({col})
    i=row-1; j=col-1;
    return board_positions[i][j] === ''
};

// this function is run once the users move has been validated and is responsible for executing
// it orchestrates the various functions that must be called in the process of making a move
function make_move(row, col){
    // console.log("make_move called");
    i=row-1; j=col-1;
    // alter board position array to make the move
    board_positions[i][j] = next_to_go;
    // change who is next to go
    toggle_next_to_go();
    // console.log({next_to_go})
    // there is now one less move left in the game
    moves_left += -1;
    // update the visual widget in html
    update_widget();

    // if the game is over handle else request the server's move
    if(is_game_over()){
        handle_game_over();
        // alert("game over")
    }
    else {
        request_server_move();
    };
};

// this is the method that is run whenever a square is clicked
function square_click(row, col){
    // console.log("square_click called");

    // validate that the square clicked is a legal move for the user to make
    // if the game isn't over
    if (!(is_game_over())){
        // and if the next to go is X, the user
        if(next_to_go === "X"){
            // and if clicked square is a legal move
            if(is_legal_move(row, col)){
                // run the make move function
                make_move(row, col);
            };
        }
        // else do nothing and ignore the click input as if the square tag were disabled.
        // else {
        //     console.log({next_to_go})
        //     console.log("user move ignored as server next to go")
        // }
    };
};

// this function emits a request to the server for its move
function request_server_move(){
    // console.log("request_server_move called");
    // it uses socket emit
    // is provides the server with the relevant game data
    socket.emit(
        'server_move_request',
        {
            board_positions,
            next_to_go,
            moves_left
        }
    );
};

// this function is responsible for determining if the current game is over.
// this is done be examining moves left to detect draws and triplet sequences to detect wins
// this function only returns a boolean value and not how the game is over
function is_game_over(){
    // console.log("is_game_over called");
    // if no moves left then the game must be over
    if(moves_left === 0){
        return true;
    };

    // get the relevant triplet sequences
    triplets = get_triplets();
    console.log({triplets})

    // iterate through the 8 triplets
    // for(i=0; i<=8; i++){
    for(i=0; i<=7; i++){
        triplet = triplets[i];
        // using 2 equals comparrison on purpose
        // i am using JSON.stringify to compare arrays to see if they are 3 in a row
        if (JSON.stringify(triplet) == JSON.stringify(["X", "X", "X"]) || JSON.stringify(triplet) == JSON.stringify(["O", "O", "O"])){
            return true;
        };
    };
    // if not already determined that the game is over then it must not be over
    return false;
};

// this function is run once the game is over
// it determines how the game is over and takes displays the appropriate message
function handle_game_over(){
    // precondition game is over so function is_game_over returned true
    // determine who won or if it was a draw
    // 1 is user (X) won, 0 is draw, -1 is user (X) lost
    // console.log("handle_game_over called");

    // variable initialized with 0 to represent draw
    winner = 0;

    // get triplets and iterate through them
    triplets = get_triplets();
    // for (i = 0; i <= 8; i++) {
    for (i = 0; i <= 7; i++) {
        triplet = triplets[i];
        // for each triplet make a comparison to check if the triplet means that the user has won or lost
        // using 2 equals comparrison on purpose
        if (JSON.stringify(triplet) == JSON.stringify(["X", "X", "X"])) {
            winner = 1;
            // no real need to break out of the loop as their can only be one or zero winning or loosing sequence
            // but it makes the code more efficient and readable
            break;
        }
        else if (JSON.stringify(triplet) == JSON.stringify(["O", "O", "O"])){
            winner = -1
            break;
        };
    };
    // if there were no winning sequences then the outcome will remain the default: 0 for draw


    // display the appropriate message to the user in each case
    if(winner === 1){
        alert("congratulations you won");
    }
    else if(winner === 0){
        alert("the game was a draw");
    }
    else{
        alert("unfortunately you lost");
    };
    // no need to disable the game as the is_game_over check will fail whenever the user clicks a square
};

// this function is called to handle a response from the server and execute the server's move
// the global board positions will have already been updated with the ones returned by the server
function handle_server_move(){
    // update the html to show the user the updated game state
    update_widget();
    // decrement the moves left
    moves_left += -1;
    // toggle who is next to go to the user
    toggle_next_to_go();
    // check if the servers move is a winning one and if so handle appropriately
    if (is_game_over()) {
        handle_game_over();
        // alert("game over")
    };
    // no else needed to enable the user to have a turn as game over validation included before user's turn
};

// tie the handler method to the socket event.
socket.on('server_move_response', function(msg){
    // console.log({msg})
    // update global for board positions with the new one that the server has sent
    board_positions = msg.board_positions
    // call handler function
    handle_server_move();
    // i believe all the handler function have to return false
    return false;
})

// this function is run when the user clicks the reset the game button

function reset_game(){
    // reset globals
    // if the user has just in the last second moved and then clicked reset before the computers move
    //  a logic error could occur where the game resets and then the server responds with its move
    // this is prevented here by ensuring that a server move isn't pending

    // // LOGIC ERROR HERE, FAILS TO RESET WHEN DRAW
    // // if(next_to_go === "O"){
    // //      return false
    // // }

    // corrected code after reset button test
    if(next_to_go === "O" && !(is_game_over())){
        return false
    }

    moves_left = 9;
    next_to_go = "X";
    board_positions = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ];
    // update the html to reflect the board position matrix
    update_widget();
}

// code to be executed when the page loads
window.addEventListener('load', function(){
    // for testing (if loading with a non blank game state)
    // update_widget();


    // the following blocks of code bind the appropriate handler method to each square
    // I tried to use iteration but it results in a logic error that I struggled to debug
    // I therefore adopted the the less elegant manual approach
    // the looping code is still here commented out as I have tried to make it work

    // for(i=1; i<=3; i++){
    //     for(j=1; j<=3; j++){
    //         get_square(i, j).addEventListener('click', function () { square_click(i, j) });
    //     }
    // }
    get_square(1,1).addEventListener('click', function(){square_click(1, 1)});
    get_square(1,2).addEventListener('click', function(){square_click(1, 2)});
    get_square(1,3).addEventListener('click', function(){square_click(1, 3)});
    get_square(2,1).addEventListener('click', function(){square_click(2, 1)});
    get_square(2,2).addEventListener('click', function(){square_click(2, 2)});
    get_square(2,3).addEventListener('click', function(){square_click(2, 3)});
    get_square(3,1).addEventListener('click', function(){square_click(3, 1)});
    get_square(3,2).addEventListener('click', function(){square_click(3, 2)});
    get_square(3,3).addEventListener('click', function(){square_click(3, 3)});

    // tie the reset the game handler function to the reset button on click
    document.getElementById('reset_btn').addEventListener('click', reset_game)
});
