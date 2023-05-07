// utility functions for use in the program

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


function assert(condition, message) {
    if (!condition) {
        message = (message === null? "Assertion error": message);
        throw new Error(message);
    }
}


// socket object to manage socket connection
let socket = io();


// this is a factory function that takes an event and returns an asynchronous function 
// the function will send a request to the server and then await and return the server's resonance
function async_function_factory_send_and_receive(event_name) {
    // returns an async function
    async function external_get_response(outgoing_payload = null) {

        // this promise resolves then a response from the server is received, the response is given
        const server_response_promise = new Promise(function (resolve) {
            socket.on(`${event_name}_response`, function (data) {
                resolve(data);
            })
        });

        // the request is sent to the server, along with an outgoing payload if appropriate
        if (outgoing_payload === null) {
            socket.emit(`${event_name}_request`);
        }
        else {
            socket.emit(
                `${event_name}_request`,
                outgoing_payload
            );
        }

        // the server's response is then awaited
        let response_payload = await server_response_promise
        // console.log({ response_payload })

        // if the response contains any actual data then it is returned
        var is_null = (response_payload === null)
        var is_empty_sting = (response_payload === "")
        var is_empty_dict = (Object.keys(response_payload).length === 0)
        
        if (is_null || is_empty_sting || is_empty_dict) {
            return null;
        }
        else {
            return response_payload
        }

    // the async function with this behaviour is returned to be reused
    }
    return external_get_response
}


// define async functions to make requests to server

// simpler functions that don't need to send and data to the server
external_get_update = async_function_factory_send_and_receive("get_update");
external_implement_computer_move_and_update = async_function_factory_send_and_receive("implement_computer_move")
external_reset_game = async_function_factory_send_and_receive("reset_game")

// more complex functions that must crate an outgoing payload and send it to the server, then return the response
async function external_implement_user_move_and_update(from_vector, to_vector) {
    movement_vector = subtract_vectors(to_vector, from_vector);
    outgoing_payload = {
        "user_move": [from_vector, movement_vector],
    };
    
    data_exchange_handler_function = async_function_factory_send_and_receive("implement_user_move")
    server_data = await data_exchange_handler_function(outgoing_payload);

    return server_data;
}

async function external_change_difficulty(new_difficulty) {
    // console.log(`sending server new difficulty of ${new_difficulty}`)
    outgoing_payload = { "new_difficulty": new_difficulty }
    external_reset_game = async_function_factory_send_and_receive("reset_game")
    data_exchange_handler_function = async_function_factory_send_and_receive("change_difficulty")
    await data_exchange_handler_function(outgoing_payload);
}


// this class contains all the data and behaviour of the client side chess game
class Chess_Board {
    // before reload feature, constructor just used initial game data
    // constructor(update_board_widget_function) {
    //     this.update_board_widget = function () {
    //         update_board_widget_function(this)
    //     }

    //     this.update_from_server_data(INITIAL_GAME_DATA)
    //     this.just_reset = true
    //     this.just_conceded = false
    // };

    // new constructor sets dom manipulation as properties 
    // then makes a request to the server to determine it properties
    constructor(update_board_widget_function, update_main_title_widget) {
        this.update_board_widget = function () {
            update_board_widget_function(this)
        }
        this.update_main_title_widget = function (msg) {
            update_main_title_widget(this, msg)
        }

        // this.update_from_server_data(INITIAL_GAME_DATA)
        this.direct_server_grand_update()

    };

    // this updates the board with the server's data but also sets reset flags to false
    async direct_server_grand_update() {
        let server_data = await external_get_update();
        this.update_from_server_data(server_data);
        this.just_reset = false
        this.just_conceded = false

        assert(this.next_to_go !== "B") 

    }

    // this function takes server data and unpacks it, 
    // the properties of the board object are then updated with this new server data
    // the board widget is then redrawn
    update_from_server_data(server_data, user_input_disabled = false) {
        this.possible_to_vectors = [];
        this.selected_from_vector = null;
        this.user_input_disabled = user_input_disabled

        this.pieces_matrix = server_data.pieces_matrix;
        this.legal_moves = server_data.legal_moves;
        this.next_to_go = server_data.next_to_go;
        this.check = server_data.check;
        this.just_reset = false

        // console.log("server_data")
        // console.log(server_data)

        // console.log("server_data.game_over_data")
        // console.log(server_data.game_over_data)

        this.game_over = server_data.game_over_data.over;
        delete server_data.game_over_data.over;
        this.over_data = server_data.game_over_data;

        this.pieces_taken = server_data.pieces_taken;
        this.move_history = server_data.move_history;
        this.difficulty = server_data.difficulty;

        this.update_board_widget();

    }


    // these 3 functions are run when certain buttons are clicked
    
    // changes difficulty property and conveys the change to the server
    change_difficulty(new_difficulty) {
        this.difficulty = new_difficulty
        external_change_difficulty(new_difficulty);
    }
 
    // simply disables the game, the only option now it to restart
    concede_game() {
        this.just_conceded = true
        this.user_input_disabled = true;

        this.over = true;
        this.highlighted_squares = []
        this.selected_from_vector = null
        this.update_board_widget()
    }

    // this function resets the board properties to the initial game data and then informs the server of this change
    reset_game() {
        let temp_difficulty = this.difficulty;
        this.update_from_server_data(INITIAL_GAME_DATA);
        this.difficulty = temp_difficulty;
        this.just_reset = true
        this.just_conceded = false
        this.update_board_widget()
        external_reset_game();
    }


    // this function handles implementing a user move
    // it validates that the user can go
    // it then updates board's properties with the new board data from the server
    async make_user_move(from_vector, to_vector) {
        assert(
            this.next_to_go == "W",
            "User must be next to go in order to implement a user move"
        )
        // console.log("make_user_move called")
        let server_data = await external_implement_user_move_and_update(from_vector, to_vector);
        // console.log("updating the board with this server data")
        // console.log({server_data})
        this.update_from_server_data(server_data, true)
        
    }

    // this function implements a computer move
    async make_computer_move() {
        console.log("make_computer_move called")

        // validates that it is the computer's turn
        assert(
            this.next_to_go == "B",
            "User must be next to go in order to implement a user move"
        )

        // created a promise to wait some amount of time (1 sec)
        const wait_before_displaying_promise = new Promise((resolve) => setTimeout(resolve, 1000))
        // const wait_a_second_promise = new Promise((resolve) => setTimeout(resolve, 0))

        // gets the new server data after computer move 
        let server_data = await external_implement_computer_move_and_update();
        // console.log({server_data})


        // get and remove move special data
        let move_description = server_data["computer_move_description"];
        delete server_data["computer_move_description"];
        // console.log({ move_description })

        
        // move description unpacked
        let [from_vector, movement_vector] = move_description.move
        let resultant_vector = add_vectors(from_vector, movement_vector)

        // no change made for a second to the user can see the board after their move
        await wait_before_displaying_promise
        
        // of the game is reset of conceded in that time, abort the function
        if (this.just_reset || this.just_conceded) {
            return null
        }

        // the relevant highlighting is applied to show the computer's move
        this.selected_from_vector = from_vector
        this.possible_to_vectors = [resultant_vector,]
        this.update_board_widget()

        // the move is highlighted for 0.8 seconds before the new board state is shown
        const wait_to_show_move_highlights = new Promise((resolve) => setTimeout(resolve, 800));
        await wait_to_show_move_highlights

        // again, abort function if game reset / conceded in that time
        if (this.just_reset || this.just_conceded) {
            return null
        }

        // console.log(`Implementing computer move:`)
        // console.log(JSON.stringify(move_description))
        // console.log(`Updating board to:`)
        // console.log(JSON.stringify(server_data.pieces_matrix))

        // show the new board positions after the computer's move
        this.update_from_server_data(server_data, true);

        // console.log("move_description.taken_piece")
        // console.log(move_description.taken_piece)

        // if (arrays_are_equal(move_description.taken_piece, [null, null])) {
        //     alert(`Computer moved ${move_description.moved_piece[1]} from ${move_description.from_square} to ${move_description.to_square}`)
        // }
        // else {
        //     alert(`Computer moved ${move_description.moved_piece[1]} from ${move_description.from_square} to ${move_description.to_square} taking ${move_description.taken_piece}`)
        // }      

    }

    // this function choreographs implementing the user move and then the computer move
    // if checks if the game is over after each one
    async user_move_and_computer_move_cycle(from_vector, to_vector) {
        await this.make_user_move(from_vector, to_vector)
        
        if (this.game_over) {
            this.handle_game_over()
            return null
        }

        // if (this.check) {
        //     alert("CHECK");
        // }

        await this.make_computer_move()



        if (this.game_over) {
            this.handle_game_over()
            return null
        }

        // if (this.check) {
        //     alert("CHECK");
        // }

        // the user can now access the board to input another move
        this.user_input_disabled = false

    }

    // this function displays the appropriate output when the game is over
    handle_game_over() {
        // make sure the game is over
        assert(this.game_over)
        let winning_player = this.over_data.winning_player;
        let victory_classification = this.over_data.victory_classification;

        
        // manually set the title message to show this
        let msg;
        switch (victory_classification) {
            case "checkmate":
                msg = (winning_player == 1) ? "Checkmate: congratulations, you won!" : "Checkmate: you lost, better luck next time"
                break
            case "stalemate board repeat":
                msg = "Stalemate: Threefold Repetition (Draw)"
                break
            case "stalemate no legal moves":
                msg = "Stalemate (Draw)"
                break
            default:
                throw new error("Invalid victory classification")
        }

        // update the title message
        this.update_main_title_widget(msg);

        // the board remains disabled
        
        // alert(msg)

        // this.reset_game();
    }
    

    // this handler function responds to the user clicking a certain square
    handle_square_click(vector) {

        // if user input is disabled, ignore the click 
        if (this.user_input_disabled) {
            // alert("board disabled")
            // console.log("board disabled")
            return null;
        }

        // else disable the board and decide what to do
        this.user_input_disabled = true;

        // check if they have clicked a green highlighted square they could move to,
        // let from_square_already_selected = this.selected_from_vector !== null;
        let is_valid_move = two_d_array_contains_sub_array(this.possible_to_vectors, vector);
        // console.log(`Checking if  [${vector}]  in  ${JSON.stringify(this.possible_to_vectors)}  -->  result was  ${is_valid_move}`);

        // if they have, cause the appropriate user then computer move
        if (is_valid_move) {
            // async function call
            // console.log("about to call make_user_move")
            // this.make_user_move(this.selected_from_vector, vector);
            this.user_move_and_computer_move_cycle(this.selected_from_vector, vector);
        }

        // else if not valid or no piece already selected then reselect
        else {
            // get piece at vector clicked
            let [i, j] = vector;
            let [row, col] = [7 - j, i];
            let [color, _] = this.pieces_matrix[row][col];

            // if the piece is one of the users then highlight red
            // if (color == this.next_to_go) {
            if (color == "W") {
                this.selected_from_vector = vector;
            }
            else {
                this.selected_from_vector = null;
            }

            // then iterate through the legal moves and identify any squares that the user could move the selected piece to 
            // if there are any, highlight green
            if (color == this.next_to_go) {
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
            // update the board to show any highlighting changes
            this.update_board_widget()
        }
        this.user_input_disabled = false
    }

    // this method returns an array of position vectors of squares and there color
    // it highlights the selected from vector red and all selected to vectors green
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
}

