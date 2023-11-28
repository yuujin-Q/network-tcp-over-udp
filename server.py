import argparse
import os.path
import struct
import threading
import time
from dataclasses import dataclass
from threading import Thread

from lib.connection import Address
from lib.constants import LOOPBACK_ADDR, DEFAULT_PORT, ENDIAN_SPECIFIER
from node.serverhandler import ServerHandler


@dataclass
class Server:
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: ServerHandler = ServerHandler(self_ip, self_port)
        # get allocated address from socket initialization
        self._ip, self._port = self._connection.get_address().get_address_data()
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

                # init handler
                new_handler = ServerHandler(self._ip)
                new_handler.set_file_payload(self._file_payload)

                # record new_handler information
                self._port_handler_map[client_address.get_port()] = new_handler
                self._clients_server_port_map[client_address] = new_handler.get_address().get_port()

                # inform client to redirect
                port_num = self._clients_server_port_map[client_address]
                print(f'[!] Created handler at port {port_num}')
                self._connection.send_payload(struct.pack(f'{ENDIAN_SPECIFIER}I', port_num), client_address)

                continue_listen = input("[?] Listen more clients? [y/n] ")
                while continue_listen.lower() != 'y' and continue_listen.lower() != 'n':
                    time.sleep(1)
                    print('[!] Invalid input, please input [y/n]')
                    continue_listen = input("[?] Listen more clients? [y/n] ")

                if continue_listen.lower() == 'n':
                    break

    def run_handlers(self, is_threading: bool = False):
        print('[!] Running Server Handlers')

        if is_threading is False:
            # run each handler
            completed_handler_ports: list[int] = []
            for port_num, handler in self._port_handler_map.items():
                handler.run()
                completed_handler_ports.append(port_num)

            # delete handlers
            for port_num in completed_handler_ports:
                del self._port_handler_map[port_num]
        else:
            # threading
            threads: list[Thread] = []
            for port_num, handler in self._port_handler_map.items():
                handler_thread = Thread(target=handler.run, name=port_num)
                threads.append(handler_thread)
                handler_thread.start()

            while threading.active_count() > 1:
                for t in threads:
                    t.join()
                    del self._port_handler_map[int(t.name)]


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='server host for file transfer')
    arg_parser.add_argument('port', type=int, help='specifies port number')
    arg_parser.add_argument('filename', type=str, help='specifies filename')
    arg_parser.add_argument('--ip', type=str, help='set server ip, defaults to localhost', default=LOOPBACK_ADDR)

    arguments = arg_parser.parse_args()

    ip: str = arguments.ip
    port: int = arguments.port
    filename: str = arguments.filename

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

    parallel = input('[?] Enable Parallel File Transfer? [y/n]')
    while parallel.lower() != 'y' and parallel.lower() != 'n':
        time.sleep(1)
        print('[!] Invalid input, please input [y/n]')
        parallel = input('[?] Enable Parallel File Transfer? [y/n]')

    server_parent.run_handlers(parallel.lower() == 'y')
