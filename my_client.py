import random
import socket
import sys
from threading import Thread

# Making Thread-object for thread that receives messages from the server.
class clientThread(Thread):
    def __init__(self, user_key):
        Thread.__init__(self)
        self.flag = True # Theard receives messages while this flag is True
        self.user_key = user_key

    def run(self):
        sock_r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_r.connect((HOST,PORT))
        sock_r.settimeout(1)
        sock_r.send('RECV-' + user_key)
        #print("FFF", HOST, PORT, self.flag)
        while self.flag:
            try:
                message = sock_r.recv(4096)
                print message
                if not message:
                    self.flag = False
            except:
                pass
        sock_r.close()


#HOST = '127.0.0.1'
#PORT = 5555
try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print "Give me HOST and PORT in command line (after script name)."
    # Example: python my_client.py 192.168.0.68 5555
    sys.exit()
    
#HOST = '127.0.0.1'
#PORT = 5555

#Special symbols for erasing last line on the terminal window:
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

# This random number is our identifier for the server:
user_key = str(random.randint(1000000,9000000))
sock_w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock_w.connect((HOST, PORT))
    sock_w.send('SEND-' + user_key)
except:
    print("Can't connect to server (%s:%s)." % (HOST, PORT))
    sys.exit()

t_read = clientThread(user_key)
t_read.start()

try:
    while 1:
        sock_w.send(raw_input(""))
        #print(CURSOR_UP_ONE + ERASE_LINE +'\e[#M') 
except:
    sock_w.close()
    t_read.flag = False
    t_read.join()
    print("closing...")
    sys.exit()
    #sock_r.close()
