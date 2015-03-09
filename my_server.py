import socket
import select
import sys


def broadcast(list_of_sockets, message):
    for sock in list_of_sockets:
        try:
            sock.send(message)
        except:
            pass


try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print "Give me HOST and PORT in command line (after script name)."
    # Example: python my_server.py 192.168.0.68 5555
    sys.exit()


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind((HOST, PORT))
serversock.listen(15)
serversock.setblocking(1)

readlist = [serversock]
writelist = []
print "Chat-server was started."


while 1:
    try:
        s_read, s_write, s_err = select.select(readlist, [], [])
    except socket.error as error:
        print("Error number:", error.errno)
        serversock.close()
        sys.exit()
    
    for sock in s_read:
        if sock == serversock:
            newsock, address = serversock.accept()
            newsock.setblocking(1)
            recv_msg = newsock.recv(1024)
            if recv_msg[:4] == 'SEND':
                readlist.append(newsock)
                message = "Client %s:%s is online." % address
                broadcast(writelist, message)
                print(message)
            else:
                writelist.append(newsock)
                newsock.send("you're connected to the server")
        else:
            try:
                recv_msg = sock.recv(1024)
                if recv_msg == "":
                    (remoute_host, remoute_port) = sock.getpeername()
                    message = "Client %s:%s closed the connection" %(remoute_host, 
                                                                     remoute_port)
                    print message
                    broadcast(writelist, message)
                    sock.close()
                    readlist.remove(sock)
                else:
                    (remoute_host, remoute_port) = sock.getpeername()
                    message = "Client %s:%s : %s" %(str(remoute_host),
                                                    str(remoute_port),
                                                    str(recv_msg))
                    print message
                    broadcast(writelist, message)
                    

            except:
                pass
