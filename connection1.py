from lib.connection import *

connection = Connection(Address(port=8000))

for i in range(100):
    segment = Segment(seq_num=1, ack_num=2)
    segment.payload = bytes('mypayload', 'utf-8')
    print(segment)
    print(segment.payload)
    connection.send_segment(msg=segment, dest=Address(port=8001))

connection.close_socket()
