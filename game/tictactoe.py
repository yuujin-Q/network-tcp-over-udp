def show_board(matrix):
    for i in range(3):
        for j in range(3):
            print(matrix[i][j], end= " ")
            if(j < 2):
                print('|', end=' ')
        if(i<2):
            print('\n----------')
    print('\n')

matrix = [['O', 'O', 'X'],
          ['X', 'O', 'X'],
          ['O', 'X', 'O']]

def initiate_board():
    matrix = [[' ' for i in range(3)] for j in range(3)]
    return matrix

def winner(matrix):
    # check row
    for i in range (3):
        if(matrix[i][0] == matrix[i][1] == matrix[i][2]):
            return matrix[i][0]
    
    #check columns 
    for i in range (3):
        if(matrix[0][i] == matrix[1][i] == matrix[2][i]):
            return matrix[0][i]
    
    #check diagonal
    if(matrix[0][0] == matrix[1][1] == matrix[2][2]):
        return matrix[0][0]
    
    if(matrix[0][2] == matrix[1][1] == matrix[2][0]):
        return matrix[0][2]

    return ' '

def is_board_full(board):
    for i in range(3):
        for j in range(3):
            if(board[i][j] == " "):
                return False
    return True

def is_valid_input(i,j):
    return (i>=0 and i<3) and (j>=0 and j<3) 


def input_board(board):
    i = int(input('row      : '))
    j = int(input('column   : '))
    print('')
    while(not(is_valid_input(i,j)) or board[i][j] != ' ' ):
        print('invalid input! try again!')
        i = int(input('row      : '))
        j = int(input('column   : '))
        print()
    
    return i,j

def tictactoe():
    board = initiate_board()

    win = ' '
    
    turn = 'X'

    while win == ' ' and not(is_board_full(board)):
        show_board(board)
        print('its ' + turn + ' turn')
        i, j = input_board(board)
        board[i][j] = turn

        win = winner(board)

        if(turn == 'X'):
            turn = 'O'
        else:
            turn = 'X'
    
    show_board(board)
    
    if win != ' ':
        print('Congratulations ' + win + ' is the winner')
    else:
        print('tie')



tictactoe()