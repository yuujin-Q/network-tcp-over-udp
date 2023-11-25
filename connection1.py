from lib.connection import *

connection = Connection(Address(port=8000))

for i in range(100):
    connection.send_segment(msg=Segment(), dest=Address(port=8001))

connection.close_socket()
