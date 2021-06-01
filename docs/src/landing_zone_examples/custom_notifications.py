import datetime
import os
import socket
import time

GALILEO_LZ_IPV4 = os.environ.get('GALILEO_LZ_IPV4')
GALILEO_LZ_PORT = os.environ.get('GALILEO_LZ_PORT')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((GALILEO_LZ_IPV4, int(GALILEO_LZ_PORT)))
    print("Connected!")
    for intervals in range(6):
        print("Sending message...")
        s.sendall(f"Hello! {datetime.datetime.now()}".encode())
        print("Done sending")
        time.sleep(10)
