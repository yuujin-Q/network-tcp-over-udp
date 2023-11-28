import argparse
import struct

from lib.address import Address
from lib.constants import *
from node.client import Client


class ClientInstance:
    def __init__(self, dest__ip: str, dest__port: int, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._dest = Address(dest__ip, dest__port)
        self._addr = Address(self_ip, self_port)
        self._connection: Client = Client(dest__ip, dest__port, self_ip, self_port)
        self._server_handler: Address | None = None

    def request_connection(self):
        print('[!] Requesting connection to server')
        # handshake to broadcast port
        self._connection.three_way_handshake()

        # redirect response
        response = self._connection.await_segment()
        self._connection.send_fin_segment(self._dest)
        self._connection.close_connection()

        # get new port
        new_port = struct.unpack(f'{ENDIAN_SPECIFIER}I', response.segment.payload)[0]
        print(f'[!] Redirected to server port {new_port}')

        # create new connection
        self._connection = Client(self._dest.get_ip(), new_port, self._addr.get_ip(), self._addr.get_port())

    def run_receiver(self):
        print('[!] Running File Receiving')
        # handshake to handler
        dest = self._connection.three_way_handshake()

        # receive file
        data = self._connection.start_receiver_transfer(dest)

        # save file
        filename = input('[?] Input filename: ')
        with open(filename, "wb") as file:
            file.write(data)

    def close_connection(self):
        self._connection.close_connection()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='client host for file transfer')
    arg_parser.add_argument('src_port', type=int, help='specifies client port number')
    arg_parser.add_argument('dest_ip', type=str, help='specifies server ip')
    arg_parser.add_argument('dest_port', type=int, help='specifies server port number')
    arg_parser.add_argument('--src_ip', nargs='?', type=str, help='set client ip, defaults to localhost',
                            default=LOOPBACK_ADDR)

    arguments = arg_parser.parse_args()
    src_port: int = arguments.src_port
    src_ip: str = arguments.src_ip
    dest_ip: str = arguments.dest_ip
    dest_port: int = arguments.dest_port

    input('[?] Press ENTER to start client')
    print(f'[!] Starting client on {src_ip}:{src_port}')
    print(f'[!] Connecting to server on {dest_ip}:{dest_port}')
    client = ClientInstance(dest_ip, dest_port, src_ip, src_port)
    client.request_connection()
    client.run_receiver()
    client.close_connection()
