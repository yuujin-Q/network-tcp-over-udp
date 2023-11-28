import argparse
import os.path
import struct
import time
from dataclasses import dataclass

from lib.connection import Address
from lib.constants import LOOPBACK_ADDR, DEFAULT_PORT, ENDIAN_SPECIFIER
from lib.messageinfo import MessageInfo
from lib.segment import Segment
from node.serverhandler import ServerHandler


@dataclass
class Server:
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: ServerHandler = ServerHandler(self_ip, self_port)
        self._clients_server_port_map: dict[Address, int] = dict()
        self._file_payload = b''
        self._port_handler_map: dict[port, ServerHandler] = dict()

    def set_file_payload(self, payload: bytes):
        self._file_payload = payload

    def listen(self):
        # waits for client connection request
        while True:
            client_address = self._connection.listen_for_client()

            if self._clients_server_port_map.get(client_address) is None:
                self._clients_server_port_map[client_address] = -1

                continue_listen = input("[?] Listen more clients? [y/n] ")
                while continue_listen.lower() != 'y' and continue_listen.lower() != 'n':
                    time.sleep(1)
                    print('[!] Invalid input, please input [y/n]')
                    continue_listen = input("[?] Listen more clients? [y/n] ")

                if continue_listen.lower() == 'n':
                    break

    def notify_redirect(self):
        # inform client to redirect
        for client_address, port_num in self._clients_server_port_map.items():
            print(port_num)
            notification_segment = Segment()
            notification_segment.set_payload(struct.pack(f'{ENDIAN_SPECIFIER}I', port_num))
            self._connection.send_segment(MessageInfo(notification_segment, client_address))

    def init_handlers(self):
        # instantiate server handler threads
        for address, port_num in self._clients_server_port_map.items():
            if port_num == -1:
                new_handler = ServerHandler(address.get_ip())

                # record new_handler information
                self._port_handler_map[address.get_port()] = new_handler
                self._clients_server_port_map[address] = new_handler.get_address().get_port()

    def run_handlers(self):
        print('[!] Running Server Handlers')

        # TODO: threading
        # run each handler
        completed_handler_ports: list[int] = []
        for port_num, handler in self._port_handler_map.items():
            handler.run()
            completed_handler_ports.append(port_num)

        # delete handlers
        for port_num in completed_handler_ports:
            del self._port_handler_map[port_num]


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='server host for file transfer')
    arg_parser.add_argument('port', type=int, help='specifies port number')
    arg_parser.add_argument('filename', type=str, help='specifies filename')
    arg_parser.add_argument('--ip', type=str, nargs=1, help='set server ip, defaults to localhost')

    arguments = arg_parser.parse_args()

    ip: str
    port: int = arguments.port
    filename: str = arguments.filename
    if arguments.ip is None:
        ip = LOOPBACK_ADDR
    else:
        ip = arguments.ip

    # read file, checks current working dir
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)
    if not os.path.exists(filepath):
        print(f"[!] File {filename} does not exist in {cwd}")
        print("[!] Stopping Server")
        exit(-1)

    # reads file as binary
    with open(filepath, "rb") as file_binaries:
        data = file_binaries.read()

    input('[?] Press ENTER to start server')
    print(f'[!] Starting server on {ip}:{port}')
    time.sleep(2)
    server_parent = Server(ip, port)
    server_parent.set_file_payload(data)
    server_parent.listen()
    server_parent.init_handlers()
    server_parent.run_handlers()
    server_parent.notify_redirect()
