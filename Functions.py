import Util  #7:23 (pre-board configuration change)
import time
import copy
import Test_Page
rank, file, setup_grid, most_recent_move, white_material, black_material = Util.rank, Util.file, Util.setup_grid, Util.most_recent_move, Util.white_material, Util.black_material

def board_set_up(setup_grid, rank, file):
    'Board_set_up creates 8x8 grid, outlines rank/file and populates pieces.  Only needs to happen once.'
    while Util.white_clock < 300 or Util.black_clock < 300 or Util.increment < 0:
        print('''To set up the clock you will need to enter MINUTES for each side and SECONDS for increment. 
        \n Each side must have a minimum of 5 minutes.  If you do not want increment, please enter 0.''')
        try:
            Util.white_clock = 60 * int(input('Please Select White Clock time in Minutes.'))
            Util.black_clock = 60 * int(input('Please Select Black Clock time in Minutes.'))
            Util.increment = int(input('For no increment, enter 0.  Otherwise, please enter increment (in seconds).'))
        except:
                print('Please enter a whole number of minutes (minimum 5 minutes) i.e 5, 10, 15, etc.  No spaces, decimals or letters.')
                Util.white_clock = 0
                Util.black_clock = 0
        print(Util.white_clock, Util.black_clock)
    backline = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    border = '  ________________________'
    for i in range(len(setup_grid[1])):
        setup_grid[i][1]='P'
    for i in range(len(setup_grid[6])):
        setup_grid[i][6]='p'
    for i in range(len(setup_grid[0])):
        setup_grid[i][0] = backline[i].upper()
    for i in range(len(setup_grid[7])):
        setup_grid[i][7] = backline[i]
    for x in [2, 3, 4, 5]:
        for y in range(8):
            setup_grid[y][x] = ' '
    #display's board in readable format while maintaining correct X,Y coordinates in Directory
def display_board(setup_grid):
    border = '  ________________________'
    print(border)
    for x in range(0, 8)[::-1]:
        row = [(setup_grid[y][x]) for y in range(0, 8)]
        print(rank[x], ("[{0}]".format(', '.join(map(str, row)))))
    print(border)
    print(' ', ("[{0}]".format(', '.join(map(str, file)))))
def request_move(player_color):
    if Util.check == True:
        print(f'Your {player_color} king is in check.  You must 1) move the king, 2) Capture the attacking piece or 3. Block the attack line.')
    else:
        pass

    turn_approved = False
    if player_color == 'WHITE':
        print(f'WHITE you have {int(Util.white_clock / 60)} minutes and {int(Util.white_clock % 60)} second remaining.' )
    elif player_color == 'BLACK':
        print(f'BLACK you have {int(Util.black_clock / 60)} minutes and {int(Util.black_clock % 60)} second remaining.' )

    Util.timer_start = time.time()
    player_color = player_color
    valid_squares = False
    starting_square_valid = False
    ending_square_valid = False

    while valid_squares == False:
        current_notation = input(f'PLAYER {player_color}: Which piece are you trying to move? (i.e.(E2)')
        if current_notation in Util.coordinate_index:
            current_coordinates = Util.coordinate_index[current_notation]
            starting_square_valid = True
            print('Starting Square Valid = True')
        new_notation = input(f'PLAYER {player_color}:Which square would you like to move to?')
        if new_notation in Util.coordinate_index:
            new_coordinates = Util.coordinate_index[new_notation]
            ending_square_valid = True
            print('Ending Square valid = True')

        if starting_square_valid == ending_square_valid == True:
            valid_squares = True
        else:
            print('One of your requested squares is not a valid square on the chessboard.  Please try again.')
    piece_on_current_square = setup_grid[current_coordinates[0]][current_coordinates[1]]
    piece_on_new_square = setup_grid[new_coordinates[0]][new_coordinates[1]]
    turn_approved = True
    #print('Current coordinates is passed as:',current_coordinates, '\n New coordinates is passed as:', new_coordinates)
    return turn_approved, player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates
def turn(turn_approved, player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates):
    vector, distance = None, None
    def create_future_grid(piece_on_current_square, current_coordinates, new_coordinates):
        future_grid = copy.deepcopy(setup_grid)
        future_grid[new_coordinates[0]][new_coordinates[1]] = piece_on_current_square
        future_grid[current_coordinates[0]][current_coordinates[1]] = ' '
        return future_grid
    def check_starting_piece(piece_on_current_square):
        if player_color == 'WHITE' and piece_on_current_square in Util.white_material:
            return True
        elif player_color == 'BLACK' and piece_on_current_square in Util.black_material:
            return True
        else:
            print(f'{player_color} does not have a piece on your starting square.  Please try again.')
            return False
    def check_destination_square(piece_on_new_square):
        if player_color == 'WHITE' and piece_on_new_square not in Util.white_material:
            return True
        elif player_color == 'BLACK' and piece_on_new_square not in Util.black_material:
            return True
        else:
            print(f'{player_color} already has a piece on your requested square.  Please try again.')
            return False
    def calc_vector_distance_map(player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates, setup_grid):
        'Calculates piece vector and if piece made single or multiple hops on available line. Knight Vector will always return distance 1.'
        vector, distance = None, 'Single'
        print('PLAYER COLOR IS:', player_color)
        #SERIES OF IF STATEMENTS TO DETERMINE PIECE VECTOR FIRST
        if current_coordinates[0] == new_coordinates[0] and current_coordinates[1] == new_coordinates[1]:
            vector = None
            print('Piece Cannot remain on its current square.  Please make a move.')
        elif current_coordinates[0] == new_coordinates[0] and current_coordinates[1] != new_coordinates[1]:
            if current_coordinates[1] == 1 and new_coordinates[1] == 3 and player_color == "WHITE" and piece_on_current_square == 'P' and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'First_Pawn_Two_Square'
                print(setup_grid[new_coordinates[0]][new_coordinates[1]])
            elif current_coordinates[1] == 6 and new_coordinates[1] == 4 and player_color == "BLACK" and piece_on_current_square == 'p'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'First_Pawn_Two_Square'
            elif new_coordinates[0]- current_coordinates[0] == 0 and new_coordinates[1]- current_coordinates[1] == 1 and player_color == "WHITE" and piece_on_current_square == 'P'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'Pawn_Advance'
            elif new_coordinates[0]- current_coordinates[0] == 0 and new_coordinates[1]- current_coordinates[1] == -1 and player_color == "BLACK" and piece_on_current_square == 'p'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'Pawn_Advance'
            else:
                vector = 'Vertical'
                print('Vector is Vertical')

        elif current_coordinates[1] == new_coordinates[1] and current_coordinates[0] != new_coordinates[0]:
            vector = 'Horizontal'
        elif player_color == 'WHITE' and piece_on_current_square == 'P' and new_coordinates[1] - current_coordinates[1] == 1 and abs(current_coordinates[0] - new_coordinates[0]) == 1 and piece_on_new_square in black_material:
            vector = 'Pawn_attack'
        elif player_color == 'BLACK' and piece_on_current_square == 'p' and new_coordinates[1] -current_coordinates[1] == -1 and abs(current_coordinates[0] - new_coordinates[0]) == 1 and piece_on_new_square in white_material:
            vector = 'Pawn_attack'
        # most_recent_move = piece_on_current_square, current_coordinates, new_coordinates
        elif (player_color == 'WHITE' and piece_on_current_square == 'P' and current_coordinates[1] == 4 and
              new_coordinates[1] - current_coordinates[1] == 1 and abs(current_coordinates[0] - new_coordinates[0]) == 1
              and Util.most_recent_move[0] == 'p' and Util.most_recent_move[1][0]-new_coordinates[0] == 0
                and Util.most_recent_move[1][1] == 6 and Util.most_recent_move[2][1] == 4):
            vector = 'En_Passant'
            setup_grid[Util.most_recent_move[2][0]][Util.most_recent_move[2][1]] = ' '
        elif (player_color == 'BLACK' and piece_on_current_square == 'p' and current_coordinates[1] == 3 and
              new_coordinates[1] - current_coordinates[1] == -1 and abs(current_coordinates[0] - new_coordinates[0]) == 1
              and Util.most_recent_move[0] == 'P' and Util.most_recent_move[1][0]-new_coordinates[0] == 0
                and Util.most_recent_move[1][1] == 1 and Util.most_recent_move[2][1] == 3):
            vector = 'En_Passant'
            setup_grid[Util.most_recent_move[2][0]][Util.most_recent_move[2][1]] = ' '
        elif abs(current_coordinates[0] - new_coordinates[0]) == abs(current_coordinates[1] - new_coordinates[1]):
            vector = 'Diagonal45'


        elif abs(abs((current_coordinates[0] - new_coordinates[0])) - abs(current_coordinates[1] - new_coordinates[1])) == 1:
            if abs(current_coordinates[0] - new_coordinates[0]) <= 2 and abs(current_coordinates[1] - new_coordinates[1]) <= 2:
                vector = 'HalfDiagonal45'
            else:
                vector = 'invalid'

        else:
            vector = 'invalid'
            print('Whoa Smokey this aint Nam there are rules.Your piece cant move like that try again.')

        # Series of IF statements (taking vector as a boolean input) to determine if piece
        # made one square advance on vector or multiple (knight excluded)

        if vector == 'Vertical':
            if abs(current_coordinates[1] - new_coordinates[1]) == 1:
                distance = 'Single'
            else:
                distance = 'Multiple'
        elif vector == 'First_Pawn_Two_Square':
            distance = 'Single'
        elif vector == 'Horizontal':
            if abs(current_coordinates[0] - new_coordinates[0]) == 1:
                distance = 'Single'
            else:
                distance = 'Multiple'
        elif vector == 'Diagonal45':
            if abs(current_coordinates[0] - new_coordinates[0]) == 1 and abs(
                    current_coordinates[1] - new_coordinates[1]) == 1:
                distance = 'Single'
            else:
                distance = 'Multiple'
        elif vector == 'HalfDiagonal45':
            distance = 'Single'

        print(vector, distance)





        return vector, distance
    def check_vector_distance(vector, distance, piece_on_current_square):
        #vector, distance = calc_vector_distance_map(piece_on_current_square, current_coordinates, new_coordinates)[0], calc_vector_distance_map(piece_on_current_square, current_coordinates, new_coordinates)[1]

        legal_vector = False
        legal_distance = False
        if vector in Util.legal_move_dict[piece_on_current_square]:
            legal_vector = True
        else:
            legal_vector = False
            print('Sorry that vector is ILLEGAL for this piece')
        if distance in Util.legal_move_dict[piece_on_current_square]:
            legal_distance = True
            print('Vector, Distance is :', vector, distance)
        else:
            legal_distance = False
            print('Vector, Distance is :', vector, distance)
            print('Sorry that distance is ILLEGAL for this piece')
        return legal_vector == legal_distance == True
    def check_open_line(piece_on_current_square, current_coordinates, new_coordinates):
        Util.requested_line.clear()
        x_change = new_coordinates[0] - current_coordinates[0]
        y_change = new_coordinates[1] - current_coordinates[1]
        if x_change == 0 and y_change > 0:
            Util.requested_line = [(new_coordinates[0], (new_coordinates[1] - y)) for y in range(y_change)[1:]]
            #print('TEST X Unchanged, Y Increase')
        elif x_change == 0 and y_change < 0:  # THIS ONE WORKS
            Util.requested_line = [(new_coordinates[0], (new_coordinates[1] + y)) for y in range(abs(y_change))[:0:-1]]
            #print('TEST X Unchanged, Y Decrease')
        elif x_change > 0 and y_change == 0:
            Util.requested_line = [(new_coordinates[0] - x, new_coordinates[1]) for x in range(x_change)[1:]]
            #print('TEST Y Unchanged, X Increase')
        elif x_change < 0 and y_change == 0:
            Util.requested_line = [((new_coordinates[0] + x), new_coordinates[1]) for x in range(abs(x_change))[:0:-1]]
            #print('TEST Y Unchanged, X Decrease')
        elif x_change > 0 and y_change > 0:
            Util.requested_line = [((new_coordinates[0] - i), (new_coordinates[1] - i)) for i in range(x_change)[1:]]
            #print('Y axis increase on slope 1')
        elif x_change < 0 and y_change < 0:
            Util.requested_line = [((new_coordinates[0] + i), (new_coordinates[1] + i)) for i in
                                   range(abs(x_change))[:0:-1]]
            #print('Y Axis decrease on slope 1')
        elif x_change < 0 and y_change > 0:
            Util.requested_line = [((new_coordinates[0] + i), (new_coordinates[1] - i)) for i in range(y_change)[1:]]
            #print('Y axis decrease on slope -1')
        elif x_change > 0 and y_change < 0:
            Util.requested_line = [((new_coordinates[0] - i), (new_coordinates[1] + i)) for i in range(x_change)[1:]]
            #print('Y axis decrease on slope -1')

        #print(Util.requested_line)
        piece_map = [setup_grid[i[0]][i[1]] for i in Util.requested_line]
        #print('piece_map is ',piece_map)
        #print('empty squares on piece map =',piece_map.count(' '))

        if piece_map.count(' ') == len(piece_map) or piece_on_current_square == 'n' or piece_on_current_square == 'N':
            #print('Open line', piece_map.count(' ') == len(piece_map))
            #print('This piece is a knight and can jump', piece_on_current_square  )
            return True
        else:
            return False
    def check_enemy_piece_on_open_line(piece_on_current_square, player_color, new_coordinates, future_grid):
        enemy_piece_on_open_line = []
        if player_color == 'WHITE':
            friendly_material = Util.white_material
            enemy_material = Util.black_material
            enemy_color = 'BLACK'
        elif player_color == 'BLACK':
            friendly_material = Util.black_material
            enemy_material = Util.white_material
            enemy_color = 'WHITE'
        for angle in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            threat_angle = angle
            threat_vector = None
            check_coordinates = new_coordinates
            piece_check = ' '
            # print('Angle being checked is', angle)
            while ((7 >= check_coordinates[0] >= 0 and 7 >= check_coordinates[1] >= 0)
                    and piece_check not in friendly_material):
                if check_coordinates != new_coordinates:
                    piece_check = future_grid[check_coordinates[0]][check_coordinates[1]]

                if piece_check in enemy_material:
                    vector_distance = calc_vector_distance_map(enemy_color, piece_check, piece_on_current_square, check_coordinates, new_coordinates, future_grid)
                    if check_vector_distance(vector_distance[0], vector_distance[1], piece_check):
                        print(piece_check, 'can attack your piece.', piece_on_current_square, new_coordinates)
                        enemy_piece_on_open_line.append((check_coordinates, piece_check))
                    break
                check_coordinates = check_coordinates[0] + threat_angle[0], check_coordinates[1] + threat_angle[1]

        def check_knight_threat(player_color, new_coordinates, future_grid):
            x, y = new_coordinates[0], new_coordinates[1]
            check_coord = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            for i in check_coord:
                if 7 >= (x + i[0]) >= 0 and 7 >= (y + i[1]) >= 0:
                    if future_grid[x + i[0]][y + i[1]] == 'n' and player_color == 'WHITE':
                        enemy_piece_on_open_line.append(((x + i[0], y + i[1]),'n'))
                        print('Black Knight is threatening piece the White Piece.')
                    elif future_grid[x + i[0]][y + i[1]] == 'N' and player_color == 'BLACK':
                        enemy_piece_on_open_line.append(((x + i[0], y + i[1]), 'N'))
                        print('White Knight is threatening piece the Black Piece.')

        check_knight_threat(player_color, new_coordinates, future_grid)
        print(enemy_piece_on_open_line)
        print('len(enemy_piece_on_open_line) > 0', len(enemy_piece_on_open_line) > 0)
        return len(enemy_piece_on_open_line) > 0

    def is_king_safe(player_color, future_grid):
        turn.king = ''
        if player_color == 'WHITE':
            turn.king = 'K'
            for x in range(len(future_grid)):
                if 'K' in future_grid[x]:
                    turn.king_coordinates = x, future_grid[x].index('K')

        elif player_color == 'BLACK':
            turn.king = 'k'
            for x in range(len(future_grid)):
                if 'k' in future_grid[x]:
                    turn.king_coordinates = x, future_grid[x].index('k')


        in_check = check_enemy_piece_on_open_line(turn.king, player_color, turn.king_coordinates, future_grid)

        print('in_check', in_check)
        if in_check == True:
            print(f'You cannot make this move because your {player_color}king is in Check.')
        else:
            print(f'Your {player_color}king is safe.')
            return True


    future_grid = create_future_grid(piece_on_current_square, current_coordinates, new_coordinates)
    is_king_safe(player_color, future_grid)
    vector_distance = calc_vector_distance_map(player_color, piece_on_current_square,piece_on_new_square,current_coordinates, new_coordinates, setup_grid)
    legal_turn = False
    if (check_starting_piece(piece_on_current_square) == check_destination_square(piece_on_new_square)
            == check_vector_distance(vector_distance[0], vector_distance[1], piece_on_current_square)
            == check_open_line(piece_on_current_square, current_coordinates, new_coordinates) == is_king_safe(player_color, future_grid) == True):
        legal_turn = True
        print('This is a legal move.  ')
        if legal_turn == turn_approved == True:
            if is_king_safe(Util.opponent, future_grid):
                Util.check = False
            if not is_king_safe(Util.opponent, future_grid):
                Util.check = True
            move_piece(piece_on_current_square, current_coordinates, new_coordinates)
    else:
        print('This move is ILLEGAL.')
    return legal_turn

def check_pawn_promotion(piece_on_current_square, new_coordinates):
    promotion_options = []
    if piece_on_current_square == 'P' and new_coordinates[1] == 7:
        promotion_options = list(Util.white_material)
        promotion_options.remove('P'), promotion_options.remove('K')
        selection = 'Test'
        while selection not in promotion_options:
            selection = input(f'CONGRATULATIONS! Your pawn has promoted.  Please select piece promotion from this list: \n {promotion_options}')
        piece_on_current_square = selection
        print(f'You have promoted to {selection}')
    elif piece_on_current_square == 'p' and new_coordinates[1] == 0:
        promotion_options = list(Util.black_material)
        promotion_options.remove('p'), promotion_options.remove('k')
        selection = 'Test'
        while selection not in promotion_options:
            selection = input(
                f'CONGRATULATIONS! Your pawn has promoted.  Please select piece promotion from this list: \n {promotion_options}')
        piece_on_current_square = selection
        print(f'You have promoted to {selection}')
    else:
        pass
    return piece_on_current_square
def castle_request(turn_approved, player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates):
    def castle_kingside(player_color):
        if player_color == 'WHITE':
            setup_grid[4][0] = ' '
            setup_grid[5][0] = 'R'
            setup_grid[6][0] = 'K'
            setup_grid[7][0] = ' '
        elif player_color == 'BLACK':
            setup_grid[4][7] = ' '
            setup_grid[5][7] = 'r'
            setup_grid[6][7] = 'k'
            setup_grid[7][7] = ' '
        Util.timer_end = time.time()
        if Util.player_turn == 'WHITE':
            Util.white_clock = Util.white_clock - (Util.timer_end - Util.timer_start)
            print('White time:', (Util.timer_end - Util.timer_start))
            Util.white_clock = Util.white_clock + Util.increment
        elif Util.player_turn == 'BLACK':
            Util.black_clock = Util.black_clock - (Util.timer_end - Util.timer_start)
            print('Black time:', (Util.timer_end - Util.timer_start))
            Util.black_clock = Util.black_clock + Util.increment
        if Util.player_turn == 'WHITE':
            Util.player_turn = 'BLACK'
        elif Util.player_turn == 'BLACK':
            Util.player_turn = 'WHITE'
        Util.timer_start = 0
        Util.timer_end = 0
    def castle_queenside(player_color):
        if player_color == 'WHITE':
            setup_grid[4][0] = ' '
            setup_grid[3][0] = 'R'
            setup_grid[2][0] = 'K'
            setup_grid[1][0] = ' '
            setup_grid[0][0] = ' '
        elif player_color == 'BLACK':
            setup_grid[4][7] = ' '
            setup_grid[3][7] = 'r'
            setup_grid[2][7] = 'k'
            setup_grid[1][7] = ' '
            setup_grid[0][7] = ' '
        Util.timer_end = time.time()
        if Util.player_turn == 'WHITE':
            Util.white_clock = Util.white_clock - (Util.timer_end - Util.timer_start)
            print('White time:', (Util.timer_end - Util.timer_start))
            Util.white_clock = Util.white_clock + Util.increment
        elif Util.player_turn == 'BLACK':
            Util.black_clock = Util.black_clock - (Util.timer_end - Util.timer_start)
            print('Black time:', (Util.timer_end - Util.timer_start))
            Util.black_clock = Util.black_clock + Util.increment
        if Util.player_turn == 'WHITE':
            Util.player_turn = 'BLACK'
        elif Util.player_turn == 'BLACK':
            Util.player_turn = 'WHITE'
        Util.timer_start = 0
        Util.timer_end = 0
    if player_color == 'WHITE' and piece_on_current_square == 'K':
        if (current_coordinates == (4, 0) and new_coordinates == (6, 0) and
                setup_grid[5][0] == ' ' and setup_grid[6][0] == ' ' and Util.can_castle_dict['E1'] == True
                and Util.can_castle_dict['H1'] == True):
            castle_kingside(player_color)
            return True
        elif (current_coordinates == (4, 0) and new_coordinates == (2, 0) and
              setup_grid[3][0] == ' ' and setup_grid[2][0] == ' ' and setup_grid[1][0] == ' ' and Util.can_castle_dict[
                  'E1'] == True
              and Util.can_castle_dict['A1'] == True):
            castle_queenside(player_color)
            return True

    elif player_color == 'BLACK' and piece_on_current_square == 'k':
        if (current_coordinates == (4, 7) and new_coordinates == (6, 7) and
                setup_grid[5][7] == ' ' and setup_grid[6][7] == ' ' and Util.can_castle_dict['E8'] == True
                and Util.can_castle_dict['H8'] == True):
            castle_kingside(player_color)
            return True
        elif (current_coordinates == (4, 7) and new_coordinates == (2, 7) and
              setup_grid[3][7] == ' ' and setup_grid[2][7] == ' ' and setup_grid[1][7] == ' ' and Util.can_castle_dict[
                  'E8'] == True
              and Util.can_castle_dict['A8'] == True):
            castle_queenside(player_color)
            return True
    else:
        return False
def castle_status_update(current_coordinates):
    if current_coordinates[0] == 0 and current_coordinates[1] == 0:
        Util.can_castle_dict.update({'A1': False})
    elif current_coordinates[0] == 4 and current_coordinates[1] == 0:
        Util.can_castle_dict.update({'E1': False})
    elif current_coordinates[0] == 7 and current_coordinates[1] == 0:
        Util.can_castle_dict.update({'H1': False})
    elif current_coordinates[0] == 0 and current_coordinates[1] == 7:
        Util.can_castle_dict.update({'A8': False})
    elif current_coordinates[0] == 4 and current_coordinates[1] == 7:
        Util.can_castle_dict.update({'E8': False})
    elif current_coordinates[0] == 7 and current_coordinates[1] == 7:
        Util.can_castle_dict.update({'H8': False})
def move_piece(piece_on_current_square, current_coordinates, new_coordinates):
    piece_on_current_square = check_pawn_promotion(piece_on_current_square, new_coordinates)
    Util.most_recent_move = piece_on_current_square, current_coordinates, new_coordinates
    setup_grid[new_coordinates[0]][new_coordinates[1]] = piece_on_current_square
    setup_grid[current_coordinates[0]][current_coordinates[1]] = ' '
    Util.timer_end = time.time()
    castle_status_update(current_coordinates)

    if Util.player_turn == 'WHITE':
        Util.white_clock = Util.white_clock - (Util.timer_end-Util.timer_start)
        print('White time:', (Util.timer_end-Util.timer_start))
        Util.white_clock = Util.white_clock + Util.increment
    elif Util.player_turn == 'BLACK':
        Util.black_clock = Util.black_clock - (Util.timer_end - Util.timer_start)
        print('Black time:', (Util.timer_end - Util.timer_start))
        Util.black_clock = Util.black_clock + Util.increment
    if Util.player_turn == 'WHITE':
        Util.player_turn = 'BLACK'
        Util.opponent = 'WHITE'
    elif Util.player_turn == 'BLACK':
        Util.player_turn = 'WHITE'
        Util.opponent = 'BLACK'
    Util.timer_start = 0
    Util.timer_end = 0
def legal_moves_available(player_color): #this will be the toughest one.  Need to check literally every move a player can make and see if they will result in check.  If no (and in check) - checkmate.  If no (and not in check) -stalemate. Make directory of material and attempt to move them to every square on the board.
    def potential_moves(player_color, setup_grid):
        pass



    #attempt to move the king one square in every direction
                #attempt to capture threatening piece
                #attempt to block attack line (if it is not a knight)
    #STALEMATE  #attempt to move all pieces along their legal lines and see if there is a legal move.
    #THREEFOLD REPETITION #log the list of setup_grids and the player whose turn it is at each.  Each turn, check the list of setup grids for 2 identical in the list.

    pass
def pick_winner():
    if Util.white_clock < 0:
        Util.winner = 'BLACK'
        Util.win_type = 'Time Expiration'
    elif Util.black_clock < 0:
        Util.winner = 'WHITE'
        Util.win_type = 'Time Expiration'
    else:
        print('The game is not over.  Keep going.')