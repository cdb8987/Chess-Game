import copy    #7:23 (pre-board configuration change)

empty_grid = [[(x, y) for y in range(0,8)] for x in range(0,8)]
setup_grid = copy.deepcopy(empty_grid)
move_list = [None]


file = ['A', 'B', 'C','D','E','F','G','H']
rank = ['1', '2', '3', '4', '5', '6', '7', '8']
square_list = [f+r for f in file for r in rank ]
most_recent_move = ['test', (0,0), (0, 0)]
can_castle_dict = {'A1': True, 'E1': True, 'H1': True, 'A8': True, 'E8': True, 'H8': True}
requested_line = []
player_turn = 'WHITE'
opponent = 'BLACK'
check = None
white_clock = 0
black_clock = 0
increment = -1

move_counter = 1

timer_start = 0
timer_end = 0

winner = None
win_type = None
checkmate = None
stalemate = None


white_material = ['P', 'R', 'N', 'B', 'Q', 'K']
black_material = ['p', 'r', 'n', 'b', 'q', 'k']

legal_move_dict = {
    'p': ['Single', 'First_Pawn_Two_Square', 'Pawn_attack', 'Pawn_Advance','En_Passant'],
    'r': ['Vertical', 'Horizontal', 'Single', 'Multiple'],
    'n': ['HalfDiagonal45', 'Single'],
    'b': ['Diagonal45', 'Single', 'Multiple'],
    'q': ['Vertical','Diagonal45', 'Horizontal', 'Single', 'Multiple'],
    'k': ['Vertical', 'Diagonal45', 'Horizontal', 'Single'],
    'P': ['Single', 'First_Pawn_Two_Square', 'Pawn_attack','Pawn_Advance', 'En_Passant'],
    'R': ['Vertical', 'Horizontal', 'Single', 'Multiple'],
    'N': ['HalfDiagonal45', 'Single'],
    'B': ['Diagonal45', 'Single', 'Multiple'],
    'Q': ['Vertical', 'Diagonal45', 'Horizontal', 'Single', 'Multiple'],
    'K': ['Vertical', 'Diagonal45', 'Horizontal', 'Single']
}

coordinate_index = {}
for row in range(len(empty_grid)):  #creates Dictionary Assigning Squares to Coordinate Tuples (i.e. A1 = (0,0) and H8 = (7, 7))
    for column in range(len(empty_grid)):
        coordinate_index[file[column] + rank[row]] = (column , row)

front_end_display_dict = {
    'K': None,
    'Q': None,
    'B': None,
    'N': None,
    'R': None,
    'P': "pictures/White_Pawn.bmp",
    'k': None,
    'q': None,
    'b': None,
    'n': None,
    'r': None,
    'p': None,
}

