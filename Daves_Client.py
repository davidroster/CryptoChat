#!/usr/bin/env python3
"""Script for clients on Dave's secret chat"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter #Python's basic GUI Library

#Handles receiving of messages
#Infinite loop so we can receive messages at any time
#Try block if client leaving causes an error
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #msg_list is a Tkinter feature for displaying the list of messages on the screen.
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

#event is passed by binders.
#Handles sending of messages
    #Get's message from message box in GUI
    #Clears message box
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

#This function is called when user exist GUI
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 2048
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

if __name__ == "__main__":
        main()