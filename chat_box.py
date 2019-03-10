# Author: Tailane Brito
# Date: 09/mar/2019
# Progra: chat_box_SERVER
#-----------------------
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread




#-----------------------
def accept_incoming_connections():
    """Sets up handlig for incoming clients."""
    while True:
        client, client_address = s.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave!" +
                          "Now type your name and press enter!",
                          "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#-----------------------
def handle_client(client): #Takes client socket as argument.
    """Handles a single client connection."""
    name= client.recv(BUFSIZ).decode("utf8")
    
    welcome = 'Welcome %s! if you ever want to quit, type {quit} to exit.' % name

    client.send(bytes(welcome, "utf8"))

    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))

    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg,name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "uft8"))
            break

#-----------------------
def broadcast(msg, prefix=""): #prefix is for name identification
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

    

"""using TC (telephonic) sockets over UDP (post-mail) sockets"""
# setting up constants
#--------CONNECTIONS---------------
#import socket s = socket.socket(socket.AF_INET, socket.sock_STREAM)

clients = {}
adresses = {}

HOST = ''
PORT = 8081
BUFSIZ = 1024
ADDR = (HOST, PORT)

s = socket(AF_INET, SOCK_STREAM)

s.bind(ADDR)

#-----------------------
if __name__ == "__main__":
    s.listen(9000) #LISTENS FOR  connections at max.
    print("Waiting for connection...")

    while True:
        c, addr = s.accept()
        print('Got connection from ', addr)
        c.send(b'Thank you for connecthing')
        c.close()

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() #starts the infinite loop.
    ACCEPT_THREAD.join()
    s.close()
        


