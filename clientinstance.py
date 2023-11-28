import argparse

from lib.constants import LOOPBACK_ADDR

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
