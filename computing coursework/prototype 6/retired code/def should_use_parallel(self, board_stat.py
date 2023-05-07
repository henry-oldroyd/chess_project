    def should_use_parallel(self, board_state: Board_State, depth):
        

        # if not self.parallel:
        #     return False

        # if depth >= 3:
        #     print("depth greater than or equal to 3 so returning true")
        #     return True
        
        # def absolute(x): return x if x >=0 else -x

        # few_pieces_left = board_state.number_total_pieces <= 24
        # many_moves_made = board_state.moves_counter >= 22
        # significant_advantage = absolute(board_state.static_evaluation()) >= 1200
        # check_encountered = board_state.check_encountered

        # late_game_score = sum(map(
        #     int,
        #     (few_pieces_left, many_moves_made, significant_advantage, check_encountered),
        # ))

        # if late_game_score >= 2:
        #     # print("Late game score greater of equal to 2 so returning true")
        #     return True


        # if late_game_score == 1:
        #     estimated_total_depth = depth + self.variable_depth
        # else:
        #     estimated_total_depth = depth

        # num_legal_moves = board_state.number_legal_moves
        # # 24 is the number of legal moves at the start of the game
        # # low_moves = num_legal_moves <= 24
        # # moderate_moves = 24 < num_legal_moves <= 40
        # # many_moves = 40 < num_legal_moves

        # # print(f"Late game score: {late_game_score}:  (few_pieces_left, many_moves_made, significant_advantage, check_encountered)  -->  {(few_pieces_left, many_moves_made, significant_advantage, check_encountered)}")


        # # if estimated depth is low then don't parallelize unless there are loads of legal moves
        # if estimated_total_depth == 2:
        #     # print(f"num_legal_moves >= 40   -->   {num_legal_moves >= 40}")
        #     return num_legal_moves >= 40



        # # if the estimated depth is moderate then parallelize if there are not many legal moves
        # if estimated_total_depth == 3:
        #     if depth == 3:
        #         # print("depth == 3 so returning true")
        #         return True

        #     # print(f"num_legal_moves <= 20   -->   {num_legal_moves <= 20}")
        #     return num_legal_moves >= 20
            

        # return False



        # if not self.parallel:
        #     return False

    
        # if board_state.check_encountered:
        #     likely_depth = depth + self.additional_depth   
        # else:
        #     likely_depth = depth
        
        # if likely_depth >= 3:
        #     return True
        # # if likely_depth == 2 and board_state.number_legal_moves >= 32:
        # #     return True
        # return False