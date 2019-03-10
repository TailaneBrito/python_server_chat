# Author: Tailane Brito
# Date: 09/mar/2019
# Progra: script for Tkinter GUI chat client.
#-----------------------


from threading import Thread
import tkinter

#------receiving messages-----------------
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
    
        except OSError: # Possibly client has left the chat.
            break

def send(event=None): #event is passed by binders.
    """Handles sending of messages."""
    try:
        msg = my_msg.get()
        my_msg.set(" ") #Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        
    except:
        
        HOST = '10.0.0.8'
        PORT = 8081
        ADDR = (HOST, PORT)
        
        s = socket(AF_INET, SOCK_STREAM)
        client_socket.bind(ADDR)
        s.connect((HOST, PORT))
        s.send(msg)
        
    if msg == "{quit}":
        client_socket.close()
        top.destroy()        
    

    

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

#--creating a frame for messages-----------------
top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() # For the messages to be sent.
my_msg.set(" ")
scrollbar = tkinter.Scrollbar(messages_frame) # to navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

#--closing the frame for messagees-----------------
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
from socket import AF_INET, socket, SOCK_STREAM
HOST = '10.0.0.8'
PORT = 8081
ADDR = (HOST, PORT)
BUFSIZ = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
print (client_socket)
try:
    client_socket.bind(ADDR)   
except socket.error as e: print(str(e))
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() #Starts GUI execution.

