import struct
from node.serverhandler import *
from node.client import *

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


def input_board(board, turn):
    i = int(input('row      : '))
    j = int(input('column   : '))
    print('')
    while(not(is_valid_input(i,j)) or board[i][j] != ' ' ):
        print('invalid input! try again!')
        i = int(input('row      : '))
        j = int(input('column   : '))
        print()
    
    return i,j

def tictactoe(Marker: chr, handler: Host, opp_addr: Address):
    board = initiate_board()

    win = ' '
    
    turn = 'X'

    while win == ' ' and not(is_board_full(board)):
        show_board(board)
        print('its ' + turn + ' turn')

        if(turn == Marker):
            i, j = input_board(board)
            input_loc = game_input(i,j)
            handler.send_payload(input_loc.convert_to_bytes(), opp_addr)
        else:
            message = handler.await_segment()
            bytes = message.segment.payload

            i, j = struct.unpack('II', bytes)

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

class game_input:
    def __init__(self, i, j):
        self.i = i
        self.j = j
    
    def convert_to_bytes(self)->bytes:
        # segment = Segment() #TODO : seq_num ack_num
        # data = b""
        # data += struct.pack('II', self.i, self.j)
        # segment.set_payload(data)

        return struct.pack('II', self.i, self.j)

        



if __name__ == "__main__":
    print("Selamat datang di tictactoe!")
    print("Ketik 1 jika kamu ingin memulai permainan baru!")
    print("Ketik 2 jika kamu ingin join ke permain lain!")

    jawaban = int(input("Jawaban kamu: "))

    while(jawaban > 2 and jawaban < 1 ):
        print('invalid input! ulangi!')
        jawaban = int(input("Jawaban kamu: "))

    if(jawaban == 1):
        port = int(input("Pilih port hosting permainan(default): "))
        handler = ServerHandler(self_port= port)
        
        print("waiting for opponent")
        dest = handler.three_way_handshake()

        print('opponent found')
        Marker = input('Masukkan marker yang kamu mau: [X/O]')
        byte_marker = struct.pack('c', Marker)
        handler.send_payload(byte_marker)

        tictactoe(Marker, handler, dest)


    elif(jawaban == 2):
        port = int(input("Pilih port untuk koneksi: "))
        dest_ip = input("masukkan ip host: ") 
        dest_port = int(input("masukkan port host: "))
        handler = Client(dest_ip, dest_port, self_port= port)
        
        print("waiting for opponent")
        handler = ServerHandler(self_port=SERVER_BROADCAST_PORT)
        dest = handler.three_way_handshake()

        message = handler.await_segment()

        Marker = struct.unpack('c', message.segment.payload)
        print('Selamat bermain')

        tictactoe(Marker, handler, dest)
    
    handler.send_fin_segment(dest)
    handler.close_connection()

