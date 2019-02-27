#!/usr/bin/env python3
#David Roster
#February 8th, 2019
#CS 176B Project

"""Server Python File for multithreaded secret chat app"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#Made global variables for easier retrieval
#Name of clients and IP Address of clients
Clients_bookkeeping = {}
addresses_bookkeeping = {}

#Input - Takes in no arguements
#Output - Waits for incoming connections, stores client info, starts thread 
def accept_incoming_connections(SERVER, BUFSIZ):
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the secret chat! Type a nickname and press Enter xD", "utf8"))
        addresses_bookkeeping[client] = client_address
        Thread(target=handle_client, args=(client,BUFSIZ,)).start()
        print("Server Log: New incoming client IP Address is...", addresses_bookkeeping[client])

#Input - Takes client socket as argument.
#Output - New client chooses a nickname and added to chatroom, otherwise deleted client 
def handle_client(client, BUFSIZ):
    Clients_Desired_Name = client.recv(BUFSIZ).decode("utf8")
    Introduction = 'Whats up %s! To leave chat, type  {quit}' % Clients_Desired_Name
    print("Server Log: The new client name is %s.", Clients_Desired_Name)
    client.send(bytes(Introduction, "utf8"))
    server_message = "%s is a new secret member!" % Clients_Desired_Name
    broadcast(bytes(server_message, "utf8"))
    Clients_bookkeeping[client] = Clients_Desired_Name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, Clients_Desired_Name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del Clients_bookkeeping[client]
            broadcast(bytes("%s has left Dave's Secret Chat." % Clients_Desired_Name, "utf8"))
            break

#client_name is for name identification.
#Broadcasts a message to all the clients.
def broadcast(msg, client_name=""):
    for member in Clients_bookkeeping:
        member.send(bytes(client_name, "utf8")+msg)

def main():
        #Makes host avilable on any laptop that runs server code
        #set port number for convenience, and so restricted ports aren't chosen
        #Initial security is clients must know port number to connect
        HOST = ''
        PORT = 33000
        BUFSIZ = 2048
        ADDR = (HOST, PORT)

        #Sets up Server Socket
        SERVER = socket(AF_INET, SOCK_STREAM)
        SERVER.bind(ADDR)

        #Starts my secret server and listens for incoming connections
        while True:
                SERVER.listen(5)
                print("Waiting for connection...")
                ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER,BUFSIZ,))
                ACCEPT_THREAD.start()
                ACCEPT_THREAD.join()
                SERVER.close()

#Starts server and listens for incoming connections
if __name__ == "__main__":
        main()