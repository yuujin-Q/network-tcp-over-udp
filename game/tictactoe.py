import struct
from node.serverhandler import *
from node.client import *

DEFAULT_IP_TICTACTOE = '0.0.0.0'
DEFAULT_PORT_TICTACTOE = 6969


def show_board(matrix):
    print(flush=True)
    for i in range(3):
        for j in range(3):
            print(matrix[i][j], end=" ")
            if j < 2:
                print('|', end=' ')
        if i < 2:
            print('\n----------')
    print('\n')


matrix = [['O', 'O', 'X'],
          ['X', 'O', 'X'],
          ['O', 'X', 'O']]


def initiate_board():
    matrix = [[' ' for _ in range(3)] for _ in range(3)]
    return matrix


def winner(matrix):
    # check row
    for i in range(3):
        if matrix[i][0] == matrix[i][1] == matrix[i][2]:
            return matrix[i][0]

    # check columns
    for i in range(3):
        if matrix[0][i] == matrix[1][i] == matrix[2][i]:
            return matrix[0][i]

    # check diagonal
    if matrix[0][0] == matrix[1][1] == matrix[2][2]:
        return matrix[0][0]

    if matrix[0][2] == matrix[1][1] == matrix[2][0]:
        return matrix[0][2]

    return ' '


def is_board_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True


def is_valid_input(i, j):
    return (0 <= i < 3) and (0 <= j < 3)


def input_board(board, turn):
    while True:
        try:
            i = int(input('row      : '))
            j = int(input('column   : '))
            break
        except: # BARE EXCEPT PALA BAPAK KAU
            print('')
    print('invalid input! try again!')
    while not (is_valid_input(i, j)) or board[i][j] != ' ':
        print('invalid input! try again!')
        i = int(input('row      : '))
        j = int(input('column   : '))
        print()

    return i, j


def tictactoe(marker: chr, handler: Host, opp_addr: Address):
    board = initiate_board()

    win = ' '

    turn = 'X'

    while win == ' ' and not (is_board_full(board)):
        show_board(board)
        print('its ' + turn + ' turn')

        if turn == marker:
            i, j = input_board(board, turn)
            input_loc = game_input(i, j)
            handler.send_payload(input_loc.convert_to_bytes(), opp_addr)
        else:
            message = handler.await_segment()
            bytes = message.segment.payload

            i, j = struct.unpack('II', bytes)

        board[i][j] = turn

        win = winner(board)

        if turn == 'X':
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

    def convert_to_bytes(self) -> bytes:
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

    while 2 < jawaban < 1:
        print('invalid input! ulangi!')
        jawaban = int(input("Jawaban kamu: "))

    self_ip = input("Masukkan IP address anda (kosongkan untuk default): ")
    if len(self_ip) == 0:
        self_ip = DEFAULT_IP_TICTACTOE
    while True:
        try:
            self_port = input("Pilih port hosting permainan (kosongkan untuk default): ")
            if len(self_port) == 0:
                self_port = DEFAULT_PORT_TICTACTOE
            else:
                self_port = int(self_port)
            break
        except:
            print("input port angka pls :(((((((((")

    print(f'IP: {self_ip}\nPort: {self_port}')

    if jawaban == 1:
        handler = ServerHandler(self_ip, self_port)

        print("waiting for opponent")
        dest = handler.three_way_handshake()

        print('opponent found')
        while True:
            marker = input('Masukkan marker yang kamu mau [X/O]: ')[0]
            if marker == 'X':
                oppo_marker = 'O'
                break
            if marker == 'O':
                oppo_marker = 'X'
                break
        byte_marker = struct.pack('c', str.encode(oppo_marker, encoding='utf-8'))
        handler.send_payload(byte_marker, dest)

        tictactoe(marker, handler, dest)

    elif jawaban == 2:
        dest_ip = input("masukkan ip host: ")
        dest_port = int(input("masukkan port host: "))
        handler = Client(dest_ip, dest_port, self_ip=self_ip, self_port=self_port)

        print("waiting for opponent")
        dest = handler.three_way_handshake()

        message = handler.await_segment()

        marker_bytes = struct.unpack('c', message.segment.payload)[0]
        marker = str(marker_bytes, encoding='utf-8')
        print(f"Marker kamu: {marker}")
        print('Selamat bermain')

        tictactoe(marker, handler, dest)

    handler.send_fin_segment(dest)
    handler.close_connection()
