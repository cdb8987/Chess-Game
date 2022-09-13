import Functions, Util, copy  #7:23 (pre-board configuration change)
import time
setup_grid = Util.setup_grid

def legal_moves_available(player_color):
    def potential_moves(player_color, setup_grid):
        remaining_material_list = []
        all_board_squares = []
        if player_color == 'WHITE':
            material = Util.white_material
        elif player_color == 'BLACK':
            material = Util.black_material
        for x in range(len(setup_grid)):
            for y in range(len(setup_grid)):
                #print(x, y)
                #print(setup_grid)
                value = setup_grid[x][y]
                all_board_squares.append((x, y))
                if value in material:
                    remaining_material_list.append((value, (x, y)))
        #print(remaining_material_list)
        #print(all_board_squares, len(all_board_squares))
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
                if Functions.turn(False, player_color, a[0], setup_grid[b[0]][b[1]], a[1], b):
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