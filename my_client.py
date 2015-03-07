import socket
import sys

HOST = '127.0.0.1'
PORT = 5555

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock1.connect((HOST, PORT))
except:
    print("Can't connect to server (%s:%s)." % (HOST, PORT))
    sys.exit()


try:
    while 1:
        sock1.send(raw_input("Send:"))
except:
    print("closing...")
    sock1.close()
