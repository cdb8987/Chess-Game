import copy, Util, Functions
empty_grid, file, rank, coordinate_index, setup_grid, display_board, turn, request_move, board_set_up, castle_request, front_end_display_coord = Util.empty_grid, Util.file, Util.rank, Util.coordinate_index, Util.setup_grid, Functions.display_board, Functions.turn, Functions.request_move, Functions.board_set_up, Functions.castle_request, Functions.front_end_display_coord

print('Instructions:  White pieces are Capitalized.  Black pieces are lower case. \n K = King     Q = Queen \n B = Bishop   N = Knight \n R = Rook     P = Pawn \nTo Castle, move the King to the correct post-castle square.' )
board_set_up(setup_grid, rank, file) #first function call

#Continually requests moves, udpates board and switches turns until a game ending condition is met
while not Util.checkmate and not Util.stalemate and not Functions.three_move_rep_check(Util.move_list):   #
    Functions.clear_visual()
    display_board(setup_grid)
    front_end_display_coord(squares=None)
    input = request_move(Util.player_turn)

    if not castle_request(input[0], input[1], input[2], input[3], input[4], input[5]):
        turn(input[0], input[1], input[2],input[3], input[4], input[5])
    display_board(setup_grid)
    Functions.is_time_left()
    Functions.legal_moves_available(Util.player_turn)

print(f'GAME OVER.')


