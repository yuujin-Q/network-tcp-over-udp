from lib.connection import *

connection = Connection(Address(port=8001))

for i in range(100):
    received = connection.listen_segment()

    if received is not None:
        print(received)
        print(received.payload)
        print()

    else:
        print("No packet received")

connection.close_socket()
