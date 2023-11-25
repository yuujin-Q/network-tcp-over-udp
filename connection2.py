from lib.connection import *

connection = Connection(Address(port=8001))

for i in range(100):
    connection.listen_segment()

connection.close_socket()
