#!/usr/bin/env python3
"""Script for clients on Dave's secret chat"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter #Python's basic GUI Library
#from Crypto.PublicKey import RSA This is having issues



#Handles receiving of messages
#Infinite loop so we can receive messages at any time
#Try block if client leaving causes an error
def receive():
    while True:
        try:
            msg = client_container.recv(Buffer_size).decode("utf8")
            #messages_list_box is a Tkinter feature for displaying the list of messages on the screen.
            messages_list_box.insert(tkinter.END, msg)
        except OSError:
            break

#event is passed by binders.
#Handles sending of messages
    #Get's message from message box in GUI
    #Clears message box
Individual_Client_Messages = []
def store_individual_client_messages():
    #Stores all indiv. messages in list
    #msg = individual_message.get()
    #Individual_Client_Messages.append(msg)
    client_name = Individual_Client_Messages[0]
    with open('client_file.txt', 'w') as f:
        for item in Individual_Client_Messages:
            f.write(client_name + " : %s\n" % item)
            print("In the for loop")
        print("on the edge of the for loop")
        f.close()
        print("after the close statements")
    print("on edge of function")
    return None


def send(event=None):
    msg = individual_message.get()
    Individual_Client_Messages.append(msg)
    individual_message.set("")
    client_container.send(bytes(msg, "utf8")) #previous working line
    if msg == "{quit}":
        client_container.close()
        main_tinker.quit()

    store_individual_client_messages()

#This function is called when user exist GUI
def on_closing(event=None):
    individual_message.set("{quit}")
    send()


'''----Now comes the Client Setup part----'''
#IP Address can be any value, making this program available to a wider audience
#Chosen port number that only official members have access too
print("Welcome to Dave's Secret Chat App\n")
IP = input('Enter IP: ')
PORT_Number = input('Enter port_Number: ')
if not PORT_Number:
    PORT_Number = 33000
else:
    PORT_Number = int(PORT_Number)

Buffer_size = 2048
Address = (IP, PORT_Number)

#Setting up Sockets for Clients
#Using TCP because more secure
client_container = socket(AF_INET, SOCK_STREAM)
client_container.connect(Address)


'''----Setting up GUI with members that are constantly updated----'''
#By making global variables for Tinker GUI, functions are called on their own everytime a new client connects to server
#Tinker allows for all communication to happen on GUI rather than terminal - a much cleaner look
main_tinker = tkinter.Tk()
main_tinker.title("Dave's Secret Chat")

#Waits for message to be typed in input box
#Initial type is nickname, the rest are texts
messages_box = tkinter.Frame(main_tinker)
individual_message = tkinter.StringVar()  # For the messages to be sent.
individual_message.set("Type a message...")
tinker_scrollbar = tkinter.Scrollbar(messages_box)  # To navigate through past messages.

#Messages_list_box will contain the messages.
#we then pack that onto our existing GUI
'''messages_list_box = tkinter.Listbox(messages_box, height=15, width=50, yscrollcommand=tinker_scrollbar.set)'''
messages_list_box = tkinter.Listbox(messages_box, height=35, width=75, yscrollcommand=tinker_scrollbar.set)
tinker_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_list_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_list_box.pack()
messages_box.pack()

#Text box where we type messages
#Every return signals new message which is handled by "individual_message.get()"
#Then message is broadcasted to rest of party
input_box = tkinter.Entry(main_tinker, textvariable=individual_message)
input_box.bind("<Return>", send)
input_box.pack()
send_button = tkinter.Button(main_tinker, text="Send", command=send)
send_button.pack()

#Calls my on_closing function when the GUI application is exited out
#Just a simple cleanup procedure
main_tinker.protocol("WM_DELETE_WINDOW", on_closing)

# Starts Tinker GUI with multithreading
#mainloop() is just Tkinter's event loop monitoring functionality
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()