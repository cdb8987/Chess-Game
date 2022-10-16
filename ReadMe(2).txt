Table of Contents:
0. Game Flow/Data Flow Overview
1. Storage of the game state
2. Updating of game state
3. Player Rules and Piece rules
4. Function Descriptions
5. Front-End-Display (Future Development)
6. User Accounts and Profiles (Future Development)

0.  GAME FLOW/DATA FLOW OVERVIEW:
-Libaries and modules are imported and variables/functions from modules are redeclared on the main page.
-board_set_up function is called which requests chess clock data from user (time, increment).  Then it populates
an 8x8 grid (in the form of a list of 8 lists with 8 elements each) with their starting piece values.  Lowercase represents
black pieces and uppercase represents white pieces.
-while loop created to contain turns and is only broken when a future turn returns either checkmate or stalemate
-clear_visual is called which prints a chunk of empty lines so that game play on terminal display is clean
-display_board is called with the setup_grid(which is the game state) as its argument.  This prints a border around the
top and bottom of the board as well as printing the letters and numbers on the sides of the board.  Then the board is printed
by creating new lists (called 'row') of the "i"th element of all the lists in the setup_grid.  This is done to rotate the displayed board 90 degrees
for more intuitive viewing.
-front_end_display_coord is called which takes each element of the setup_grid and returns a tuple
containing(piece value, chess notation, left and top margin value for where the piece value should be displayed on
the chessboard image on the front end.
-request_move is called which takes a parameter player_turn(which is flipped back and forth each time move_piece is called).
This verifies the "check" value is false(which is controlled by the turn function).  It prints the clock time remaining for the player and starts
the timer for the turn.  It creates a while loop to continually request input from the player until both their starting and ending squares
are valid on the board.  Then it returns the beginning and ending coordinates and piece values and approves the turn.
-a boolean is set to evaluate if the request_move is a castle_request.  If so, a separate function route is executed because
castle_request will be invalid by the piece operating rules in "turn".
-turn is called.  It creates a hypothetical future game state called "future_grid" which exists as a "test area".  This allows moves to be checked
without updating the game state (setup_grid) until all conditions are evaluated to be valid for the turn. Using is_king_safe, it checks to see if
the opposing player can attack the king on next move.  calc_vector_distance_map is called and checks the difference in coordinates between the future_grid and setup_grid
and returns the vector, distance of the requested move (both are qualitative values which will be checked against a dictionary.)
Functions 1. piece_on_current_square, 2. check_destination_square, 3. check_vector_distance, 4. check_open_line, 5. is_king_safe are all called to verify the player 1. has a piece on their starting
square, 2. the player does not have a piece on the ending square, 3. the vector(i.e. type of piece movement) and distance of the requested move are included in the pieces capabilities, 4. there are
no pieces blocking the route between the starting and ending square, and 5. the king will not be in check on the move afterwards.  If all are valid, move_piece is called
which checks for pawn promotions, updates the most_recent_move variable (stored so that en passant can be checked), updates the setup_grid with the requested move, stops the turn timer, updates the
"castle_status" placeholder, updates the game log, deletes the time spend on the turn from the player's clock and switches player_turn to the other player.
-dispay_board is called to show the new game state
-is_time_left is called which check if either player has run out of time
-legal_moves_available is called to check if the next player has any legal moves.  If not and they are in check, checkmate is declared and game is over.
If no legal moves and they are not in check, stalemate is declared and game is over.


1.  STORAGE OF THE GAME STATE: This grid was originally stored as a left to right game.
To improve playability, it was refactored to display pieces differently than
how the "setup_grid" variable suggests (see FIG 1.A).  Because many dependent functions had already been
built, the setup_grid variable was left alone.  Setup grid is stored in typical (x,y) grid format.
It is stored as a list of 8 lists each containing 8 elements (see FIG 1.B).  The position in the first list is intended
as the x-coordinate and the position in the sub-list is considered the y-coordinate.  Dependent functions
find which piece is on a square by querying setup_grid using the combined list indices.
Ex:
setup_grid[0][0] = A1 = 'R'
setup_grid[7][0] = H1 = 'R'
setup_grid[0][7] = A8 = 'r'
setup_grid[7][7] = H8 = 'r'

FIG 1.A - (CONSOLE DISPLAY)
  ________________________
8 [r, n, b, q, k, b, n, r]
7 [p, p, p, p, p, p, p, p]
6 [ ,  ,  ,  ,  ,  ,  ,  ]
5 [ ,  ,  ,  ,  ,  ,  ,  ]
4 [ ,  ,  ,  ,  ,  ,  ,  ]
3 [ ,  ,  ,  ,  ,  ,  ,  ]
2 [P, P, P, P, P, P, P, P]
1 [R, N, B, Q, K, B, N, R]
  ________________________
  [A, B, C, D, E, F, G, H]

FIG 1.B  (setup_grid coordinate )

A1                                   A8
['R', 'P', ' ', ' ', ' ', ' ', 'p', 'r']
['N', 'P', ' ', ' ', ' ', ' ', 'p', 'n']
['B', 'P', ' ', ' ', ' ', ' ', 'p', 'b']
['Q', 'P', ' ', ' ', ' ', ' ', 'p', 'q']
['K', 'P', ' ', ' ', ' ', ' ', 'p', 'k']
['B', 'P', ' ', ' ', ' ', ' ', 'p', 'b']
['N', 'P', ' ', ' ', ' ', ' ', 'p', 'n']
['R', 'P', ' ', ' ', ' ', ' ', 'p', 'r']
H1                                   H8

2.  Updating the game state.  The game state (setup_grid) is referenced by nearly every function but is altered by only 4 functions.
board_set_up, move_piece, calc_vector_distance_map>>"en passant"(this deletes the enemy pawn that is not actually replaced by
the player's piece), and castle_request (which moves pieces in a way that circumvents turn.move_piece).  future_grid is used as way to
evaluate whether a move is legal or not without actually changing the baseline game state.

3. Player Rules and Piece rules.  Player rules:  White makes the first move and then White and Black alternate until either
time expiration, checkmate or stalemate.  I have not included the 3 move repetition






FRONT END CSS - Front end display will create a grid of coordinates for the css stylesheet.  Left and top
margins will be fixed and then each coordinate will iterate across and down by the pixel length of each square.
This grid will be assigned images which will correspond to the piece values shown on the setup_grid.
    -As a reminder, on the setup_grid : (A1 = (0,0), H1 = (7,0), A8 = (0,7), H8 = (7,7).
    A8 (0,7) >>>> H1(7,0)











Remaining Bugs:  Sometimes if you select a square that you don't have a piece on AND to move to a square inhabited by enemy, a keyerror is thrown.
Make and Functions that have a ton of sub functions a class.  (Mostly the turn function)