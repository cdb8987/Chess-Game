import copy, Util, Functions, Test_Page
empty_grid, file, rank, coordinate_index, setup_grid, display_board, turn, request_move, board_set_up, castle_request = Util.empty_grid, Util.file, Util.rank, Util.coordinate_index, Util.setup_grid, Functions.display_board, Functions.turn, Functions.request_move, Functions.board_set_up, Functions.castle_request

print('Instructions:  White pieces are Capitalized.  Black pieces are lower case. \n K = King     Q = Queen \n B = Bishop   N = Knight \n R = Rook     P = Pawn')
print('To Castle, move the King to the correct post-castle square.')
board_set_up(setup_grid, rank, file) #first function call


display_board(setup_grid)
while not Util.checkmate and not Util.stalemate:

    display_board(setup_grid)
    input = request_move(Util.player_turn)
    if not castle_request(input[0], input[1], input[2], input[3], input[4], input[5]):
        turn(input[0], input[1], input[2],input[3], input[4], input[5])
    display_board(setup_grid)
    print(Util.most_recent_move)
    Functions.pick_winner()
    Test_Page.legal_moves_available(Util.player_turn)
    
print(f'GAME OVER.')


