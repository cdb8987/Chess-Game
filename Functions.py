import Util  #7:23 (pre-board configuration change)
import time
import copy

import Test_Page
rank, file, setup_grid, white_material, black_material = Util.rank, Util.file, Util.setup_grid, Util.white_material, Util.black_material

def board_set_up(setup_grid, rank, file):
    '''Board_set_up creates 8x8 grid, outlines rank/file and populates pieces.  It also requests user input to set the clock and the increment.
    Minimum time set for 5 minutes on each side.  Lowercase letters are used to populate black and upper for white.  '''
    while Util.white_clock < 300 or Util.black_clock < 300 or Util.increment < 0: #sets minimum time allowance at 5 minutes
        print('''To set up the clock you will need to enter MINUTES for each side and SECONDS for increment.\nEach side must have a minimum of 5 minutes.  If you do not want increment, please enter 0.''')
        try:
            Util.white_clock = 60 * int(input('\nPlease Select White Clock time in Minutes.'))
            Util.black_clock = 60 * int(input('\nPlease Select Black Clock time in Minutes.'))
            Util.increment = int(input('For no increment, enter 0.  Otherwise, please enter increment (in seconds).'))
        except:
                print('Please enter a whole number of minutes (minimum 5 minutes) i.e 5, 10, 15, etc.  No spaces, decimals or letters.')
                Util.white_clock = 0
                Util.black_clock = 0
        # print(Util.white_clock, Util.black_clock)
    backline = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    border = '  ________________________'

    ###NOTE!!!- WHEN referencing piece values on 'setup_grid' please know the board is
    #STORED with left being white and black being right but the display is converted to SHOW
    #White being bottom and black being top.  To avoid errors, please make sure to reference
    #diagram '1.  Storage of game state' in ReadMe.txt
    for i in range(8):
        setup_grid[i][1]='P'
    for i in range(8):
        setup_grid[i][6]='p'
    for i in range(8):
        setup_grid[i][0] = backline[i].upper()
    for i in range(8):
        setup_grid[i][7] = backline[i]
    for x in [2, 3, 4, 5]:
        for y in range(8):
            setup_grid[y][x] = ' '

    #display's board in readable format while maintaining correct X,Y coordinates in Directory
def display_board(setup_grid):
    '''This function is called every turn and shows the new configuration of the board as stored by setup_grid.  It also
    prints the board in a console friendly user display.'''
    global border
    border = '  ________________________'
    print(border)
    for x in range(0, 8)[::-1]:
        row = [(setup_grid[y][x]) for y in range(0, 8)]
        print(rank[x], ("[{0}]".format(', '.join(map(str, row)))))
    print(border)
    print(' ', ("[{0}]".format(', '.join(map(str, file)))))
def request_move(player_color):
    '''First Checks Util.Check to see if player is in check from previous move.  Prints Players remaining time. Sets variable turn_approved to false and evaluates
    a series of booleans that must all be true for turn to switch to approved. Checks to make sure both squares are valid squares on the board.  This function returns the piece values (i.e. 'p', 'K', etc) and the coordinates
     of both the starting square and the requested square.
     '''
    global current_notation, new_notation
    current_notation, new_notation = None, None

    if Util.check == True:  #Shows notification if 'check' function returns true
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
        new_notation = input(f'PLAYER {player_color}:Which square would you like to move to?')
        if new_notation in Util.coordinate_index:
            new_coordinates = Util.coordinate_index[new_notation]
            ending_square_valid = True
        if starting_square_valid == ending_square_valid == True:
            valid_squares = True
        else:
            print('One of your requested squares is not a valid square on the chessboard.  Please try again.')
    piece_on_current_square = setup_grid[current_coordinates[0]][current_coordinates[1]]
    piece_on_new_square = setup_grid[new_coordinates[0]][new_coordinates[1]]
    turn_approved = True
    return turn_approved, player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates

def turn(turn_approved, player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates):
    '''Sub-function Call order.  1. Future Grid Created (create_future_grid), 2.  Look for attacks on king on the next move (is_king_safe),
     3.  Check vector and distance and validate against piece allowable moves (calc_vector_distance_map),
     4.  Checks if all conditions are valid and if so, calls the move_piece function.'''

    vector, distance = None, None
    def create_future_grid(piece_on_current_square, current_coordinates, new_coordinates):
        '''Creates a future grid against which move legality and potential future move options (when determining check/stalemate) can be evaluated without actually updating the board until all
    conditions are met.'''
        future_grid = copy.deepcopy(setup_grid)
        future_grid[new_coordinates[0]][new_coordinates[1]] = piece_on_current_square
        future_grid[current_coordinates[0]][current_coordinates[1]] = ' '
        return future_grid
    def check_starting_piece(piece_on_current_square):
        '''Checks to make sure that the piece on the requested square currently houses a piece from the requesting player.'''
        if player_color == 'WHITE' and piece_on_current_square in Util.white_material:
            return True
        elif player_color == 'BLACK' and piece_on_current_square in Util.black_material:
            return True
        else:
            # print(f'{player_color} does not have a piece on your starting square.  Please try again.')
            return False
    def check_destination_square(piece_on_new_square):
        '''Checks to make sure the piece on destination square does not contain piece belonging to requesting player.'''
        if player_color == 'WHITE' and piece_on_new_square not in Util.white_material:
            return True
        elif player_color == 'BLACK' and piece_on_new_square not in Util.black_material:
            return True
        else:
            return False
    def calc_vector_distance_map(player_color, piece_on_current_square, piece_on_new_square, current_coordinates, new_coordinates, setup_grid):
        '''Categorizes piece movements by vector (i.e. horizontal, vertical, diagonal, special knight move).  Categorizes piece distance as either single
        or multiple.  These are returned as strings which are later cross referenced to a dictionary containing allowable piece movements for each piece.'''
        vector, distance = None, 'Single'
        #SERIES OF IF STATEMENTS TO DETERMINE PIECE VECTOR FIRST
        if current_coordinates[0] == new_coordinates[0] and current_coordinates[1] == new_coordinates[1]:
            vector = None
        elif current_coordinates[0] == new_coordinates[0] and current_coordinates[1] != new_coordinates[1]:
            if current_coordinates[1] == 1 and new_coordinates[1] == 3 and player_color == "WHITE" and piece_on_current_square == 'P' and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'First_Pawn_Two_Square'
            elif current_coordinates[1] == 6 and new_coordinates[1] == 4 and player_color == "BLACK" and piece_on_current_square == 'p'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'First_Pawn_Two_Square'
            elif new_coordinates[0]- current_coordinates[0] == 0 and new_coordinates[1]- current_coordinates[1] == 1 and player_color == "WHITE" and piece_on_current_square == 'P'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'Pawn_Advance'
            elif new_coordinates[0]- current_coordinates[0] == 0 and new_coordinates[1]- current_coordinates[1] == -1 and player_color == "BLACK" and piece_on_current_square == 'p'and setup_grid[new_coordinates[0]][new_coordinates[1]] == ' ':
                vector = 'Pawn_Advance'
            else:
                vector = 'Vertical'
        elif current_coordinates[1] == new_coordinates[1] and current_coordinates[0] != new_coordinates[0]:
            vector = 'Horizontal'
        elif player_color == 'WHITE' and piece_on_current_square == 'P' and new_coordinates[1] - current_coordinates[1] == 1 and abs(current_coordinates[0] - new_coordinates[0]) == 1 and piece_on_new_square in black_material:
            vector = 'Pawn_attack'
        elif player_color == 'BLACK' and piece_on_current_square == 'p' and new_coordinates[1] -current_coordinates[1] == -1 and abs(current_coordinates[0] - new_coordinates[0]) == 1 and piece_on_new_square in white_material:
            vector = 'Pawn_attack'
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
        return vector, distance
    def check_vector_distance(vector, distance, piece_on_current_square):
        '''Cross references vector and distance passed in from calc_vector_distance_map.  Check the pieces availble
        legal standard move types in Util.legal_move_dict.  Returns true if both are allowed.'''
        legal_vector = False
        legal_distance = False
        if vector in Util.legal_move_dict[piece_on_current_square]:
            legal_vector = True
        else:
            legal_vector = False
        if distance in Util.legal_move_dict[piece_on_current_square]:
            legal_distance = True
        else:
            legal_distance = False
        return legal_vector == legal_distance == True
    def check_open_line(piece_on_current_square, current_coordinates, new_coordinates):
        '''Checks all squares between the current square and the new square to make sure no pieces exist that are in the way.  '''
        Util.requested_line.clear()
        x_change = new_coordinates[0] - current_coordinates[0]
        y_change = new_coordinates[1] - current_coordinates[1]
        if x_change == 0 and y_change > 0:
            Util.requested_line = [(new_coordinates[0], (new_coordinates[1] - y)) for y in range(y_change)[1:]]
        elif x_change == 0 and y_change < 0:
            Util.requested_line = [(new_coordinates[0], (new_coordinates[1] + y)) for y in range(abs(y_change))[:0:-1]]
        elif x_change > 0 and y_change == 0:
            Util.requested_line = [(new_coordinates[0] - x, new_coordinates[1]) for x in range(x_change)[1:]]
        elif x_change < 0 and y_change == 0:
            Util.requested_line = [((new_coordinates[0] + x), new_coordinates[1]) for x in range(abs(x_change))[:0:-1]]
        elif x_change > 0 and y_change > 0:
            Util.requested_line = [((new_coordinates[0] - i), (new_coordinates[1] - i)) for i in range(x_change)[1:]]
        elif x_change < 0 and y_change < 0:
            Util.requested_line = [((new_coordinates[0] + i), (new_coordinates[1] + i)) for i in
                                   range(abs(x_change))[:0:-1]]
        elif x_change < 0 and y_change > 0:
            Util.requested_line = [((new_coordinates[0] + i), (new_coordinates[1] - i)) for i in range(y_change)[1:]]
        elif x_change > 0 and y_change < 0:
            Util.requested_line = [((new_coordinates[0] - i), (new_coordinates[1] + i)) for i in range(x_change)[1:]]
        piece_map = [setup_grid[i[0]][i[1]] for i in Util.requested_line]
        if piece_map.count(' ') == len(piece_map) or piece_on_current_square == 'n' or piece_on_current_square == 'N':
            return True
        else:
            return False
    def check_enemy_piece_on_open_line(piece_on_current_square, player_color, new_coordinates, future_grid):
        '''Checks to see if an enemy piece has a clear line to a given square/piece.  Primarily used for evaluating checks on the king. '''
        enemy_piece_on_open_line = []
        if player_color == 'WHITE': #determines whether white or black are the enemy pieces we need to check for
            friendly_material = Util.white_material
            enemy_material = Util.black_material
            enemy_color = 'BLACK'
        elif player_color == 'BLACK':
            friendly_material = Util.black_material
            enemy_material = Util.white_material
            enemy_color = 'WHITE'
            #The following are all linear vectors that can be iterated legally on a chessboard.
            #Knight moves are not included since knights do not need an open line of empty squares to attack.
        for angle in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            threat_angle = angle
            threat_vector = None
            check_coordinates = new_coordinates
            piece_check = ' ' #single space string indicates empty square on board
            #While loop below Iterates from starting position to the end of all possible lines. Range set 0-7 (both inluded) to only check valid coordinates on 8*8 chessboard and prevent index errors.
            while ((7 >= check_coordinates[0] >= 0 and 7 >= check_coordinates[1] >= 0)
                    and piece_check not in friendly_material):
                if check_coordinates != new_coordinates:
                    piece_check = future_grid[check_coordinates[0]][check_coordinates[1]]
                if piece_check in enemy_material: #if enemy piece on open line, check that enemy piece's allowable movement types.
                    vector_distance = calc_vector_distance_map(enemy_color, piece_check, piece_on_current_square, check_coordinates, new_coordinates, future_grid)
                    if check_vector_distance(vector_distance[0], vector_distance[1], piece_check): #if the enemy piece's vector and distance constraints allow them to move to the requested square, Add them to the list of threatening pieces (enemy_piece_on_open_line)
                        enemy_piece_on_open_line.append((check_coordinates, piece_check))
                    break
                check_coordinates = check_coordinates[0] + threat_angle[0], check_coordinates[1] + threat_angle[1]

        def check_knight_threat(player_color, new_coordinates, future_grid):
            '''Repeats above operation except without iterating since knight moves are fixed.  Checks if enemy knights exist on potential attack squares.
            If so, adds them to the threat list (enemy_piece_on_open_line).'''
            x, y = new_coordinates[0], new_coordinates[1]
            check_coord = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            for i in check_coord:
                if 7 >= (x + i[0]) >= 0 and 7 >= (y + i[1]) >= 0:
                    if future_grid[x + i[0]][y + i[1]] == 'n' and player_color == 'WHITE':
                        enemy_piece_on_open_line.append(((x + i[0], y + i[1]),'n'))
                        # print('Black Knight is threatening piece the White Piece.')
                    elif future_grid[x + i[0]][y + i[1]] == 'N' and player_color == 'BLACK':
                        enemy_piece_on_open_line.append(((x + i[0], y + i[1]), 'N'))
                        # print('White Knight is threatening piece the Black Piece.')

        check_knight_threat(player_color, new_coordinates, future_grid)
        # print(enemy_piece_on_open_line)
        # print('len(enemy_piece_on_open_line) > 0', len(enemy_piece_on_open_line) > 0)
        return len(enemy_piece_on_open_line) > 0

    def is_king_safe(player_color, future_grid):
        '''Identifies the king of the current player, the kings square and then passes that square into
        check_enemy_piece_on_open_line to see if the king will be attackable on the next move.'''
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
        if in_check == True:
            pass
        else:
            return True
    future_grid = create_future_grid(piece_on_current_square, current_coordinates, new_coordinates)
    is_king_safe(player_color, future_grid)
    vector_distance = calc_vector_distance_map(player_color, piece_on_current_square,piece_on_new_square,current_coordinates, new_coordinates, setup_grid)
    legal_turn = False
    if (check_starting_piece(piece_on_current_square) == check_destination_square(piece_on_new_square)
            == check_vector_distance(vector_distance[0], vector_distance[1], piece_on_current_square)
            == check_open_line(piece_on_current_square, current_coordinates, new_coordinates) == is_king_safe(player_color, future_grid) == True):
        legal_turn = True
        if legal_turn == turn_approved == True:
            if is_king_safe(Util.opponent, future_grid):
                Util.check = False
            if not is_king_safe(Util.opponent, future_grid):
                Util.check = True
            move_piece(piece_on_current_square, current_coordinates, new_coordinates)
    else:
        pass
        # print('This move is ILLEGAL.')
    return legal_turn

def check_pawn_promotion(piece_on_current_square, new_coordinates):
    '''Allows player to select a new piece value if one of their pawns has reached the final rank.'''
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
    '''Checks if the requested move is a castle request and then checks current board as well as move history (Util.can_castle_dict) to see if it is allowed.'''
    def castle_kingside(player_color):
        '''Castles Kingside.'''
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
        '''Castles Queenside'''
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
    '''Updates a dictionary that records whether kings and rooks have moved or not to be referenced by future castle requests.  If a given rook or king has moved, it can no longer participate in a castle move.'''
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
    '''Checks if move results in pawn promotion.  Updates Util.most_recent_move to be referenced by the En Passant Function.
    Changes the piece value of the target square and returns piece value of old square to a single space string ' '.
    Ends the players move timer once the board has been successfully updated.  Updates Castle Status.  Updates the game log.
    Subtracts used time from the players remaining clock.  Toggles Util.player_turn to or from WHITE/BLACK.'''
    piece_on_current_square = check_pawn_promotion(piece_on_current_square, new_coordinates)
    Util.most_recent_move = piece_on_current_square, current_coordinates, new_coordinates
    setup_grid[new_coordinates[0]][new_coordinates[1]] = piece_on_current_square
    setup_grid[current_coordinates[0]][current_coordinates[1]] = ' '
    Util.timer_end = time.time()
    castle_status_update(current_coordinates)


    update_game_log(Util.player_turn, current_notation, new_notation)
    if Util.player_turn == 'WHITE':
        Util.white_clock = Util.white_clock - (Util.timer_end-Util.timer_start)
        print('White time:', (Util.timer_end-Util.timer_start))
        Util.white_clock = Util.white_clock + Util.increment
    elif Util.player_turn == 'BLACK':
        Util.black_clock = Util.black_clock - (Util.timer_end - Util.timer_start)
        print('Black time:', (Util.timer_end - Util.timer_start))
        Util.black_clock = Util.black_clock + Util.increment
    Util.move_list.append((Util.player_turn, copy.deepcopy(setup_grid))) #ADDS Move after completion to move_list for three rep checker
    if Util.player_turn == 'WHITE':
        Util.player_turn = 'BLACK'
        Util.opponent = 'WHITE'
    elif Util.player_turn == 'BLACK':
        Util.player_turn = 'WHITE'
        Util.opponent = 'BLACK'
    Util.timer_start = 0
    Util.timer_end = 0


def update_game_log(player_color, current_notation, new_notation):
    '''Writes players move (i.e. E2, E4) as well as the printed board to a text file so players
    can examine a history of the game post-mortem.'''
    with open('Game_Record.txt', mode='a') as game_log:
        game_log.write(str(Util.move_counter) +'. '  + player_color[0]+ ':' + current_notation
        + ','+ new_notation+ '\n')
        Util.move_counter += 1

        game_log.write(border + '\n')
        for x in range(0, 8)[::-1]:
            row = [(setup_grid[y][x]) for y in range(0, 8)]
            game_log.write(str(rank[x]+ ("[{0}]".format(', '.join(map(str, row))))))
            game_log.write('\n')
        game_log.write(border + '\n')
        game_log.write(' '+ ("[{0}]".format(', '.join(map(str, file))))+ '\n\n')

def legal_moves_available(player_color):
    def potential_moves(player_color, setup_grid):
        remaining_material_list = []
        all_board_squares = []
        if player_color == 'WHITE': #defines whose material we are looking for
            material = Util.white_material
        elif player_color == 'BLACK':
            material = Util.black_material
        for x in range(len(setup_grid)):
            for y in range(len(setup_grid)):
                value = setup_grid[x][y]
                all_board_squares.append((x, y)) #populates all_board_squares with 64 elements each containing one of the valid coordinates
                if value in material:
                    remaining_material_list.append((value, (x, y))) #adds piece value to remaining material list
        return remaining_material_list, all_board_squares

    material_and_squares = potential_moves(player_color, Util.setup_grid)
    material, squares = material_and_squares[0], material_and_squares[1]
    def check_legal(material, squares):
        legal_moves = []
        done = False
        for a in material:
            for b in squares:
                #print('Material A is ', a, 'Squares B is' ,b)
                #print('A[0] is ',a[0], 'setup_grid[[b[0]][b[1]]] is',setup_grid[b[0]][b[1]], 'a[1] is', a[1],'b is', b)
                if turn(False, player_color, a[0], setup_grid[b[0]][b[1]], a[1], b):
                    legal_moves.append((a[0], b))
                    done = True
                    break
            if done == True:
                break
        #print(legal_moves)
        if len(legal_moves) == 0 and Util.check == True:
            Util.checkmate = True
            print(f'Player{player_color} is in CHECKMATE.  GAME OVER!')
        elif len(legal_moves) == 0 and Util.check == False:
            Util.stalemate = True
            print(f'Player {player_color} cannot make a legal move and is not in check. \n STALEMATE!')

    check_legal(material, squares)
def is_time_left():
    if Util.white_clock < 0:
        Util.winner = 'BLACK'
        Util.win_type = 'Time Expiration'
    elif Util.black_clock < 0:
        Util.winner = 'WHITE'
        Util.win_type = 'Time Expiration'
    else:
        pass
def three_move_rep_check(l):
    '''Takes the move_list as an argument'''
    recent_move = l[-1]
    if l.count(recent_move) == 3:
        return True

def clear_visual():
    for i in range(15):
        print('\n')

def front_end_display_coord(squares=None):  ##this function will create a grid of coordinates that will be passed to CSS stylesheet
    margin_left = 34
    top = 31
    coord_list = []
    for idx1, r in enumerate(reversed(list(rank))):
        length_of_square_side = 67
        t = top + idx1 * length_of_square_side
        for idx2, f in enumerate(file):
            l = margin_left + idx2 * length_of_square_side
            piece_value = setup_grid[idx2][7 - idx1]
            coord_list.append(tuple((piece_value, str(f)+str(r), l, t)))
    return coord_list