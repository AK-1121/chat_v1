import socket
import select
import sys

HOST = '127.0.0.1'
PORT = 5555


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind((HOST, PORT))
serversock.listen(15)
serversock.setblocking(1)

readlist = [serversock]
#print("dir(serversock):", dir(serversock), "\n", serversock.fileno)

while 1:
    try:
        s_read, s_write, s_err = select.select(readlist, [], [])
    except socket.error as error:
        print("Error number:", error.errno)
        serversock.close()
        sys.exit()
    
    #print("s_read:", s_read, "\ns_write:", s_write, "\ns_err:", s_err)
    #print("AAA - readlist:", readlist)
    for sock in s_read:
        if sock == serversock:
            newsock, address = serversock.accept()
            newsock.setblocking(1)
            readlist.append(newsock)
            newsock.send("you're connected to the select server")
            message = "Client %s : %s is online." % address
            print(message)
            #broadcast(serversock, readlist, message)
            #print("BBB - readlist:", readlist)
        else:
            try:
                recv_msg = sock.recv(1024)
            
                if recv_msg == "":
                    #print("DDD")
                    (remoute_host, remoute_port) = sock.getpeername()
                    print "Client %s:%s closed the connection" %(remoute_host, 
                                                                remoute_port)
                    sock.close()
                    readlist.remove(sock)
                else:
                    #print("FFF")
                    (remoute_host, remoute_port) = sock.getpeername()
                    print "Client %s : %s sent: %s" %(str(remoute_host),
                                                    str(remoute_port),
                                                    str(recv_msg))
            except:
                print("Client %s : %s is offline." % sock.getpeername())
                sock.close()
                readlist.remove(sock)
                

