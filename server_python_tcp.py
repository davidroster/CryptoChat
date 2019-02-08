# first of all import the socket library
import subprocess
import socket
import sys
import os
         

def frame_send_message(message, address, sock):
    #this breaks messages into blocks of 1024 bytes if needed
    
    framed_message = ''
    for c in range(len(message)):
        if (len(framed_message) < 1024) :
            framed_message = framed_message + message[c]

            if c == len(message) - 1:
                send_message(framed_message, address, sock)
        else:
            #send the framed message(can be less than 1024 bytes)
            send_message(framed_message, address, sock)
            #start building new framed_message
            framed_message = message[c]

def send_message(message, address, sock):
    #if the message has been broken up, the length with
    #be 1024 bytes
    sock.sendall(message.encode())

def main(port):
    # next create a socket object
    s = socket.socket()         
                
    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests 
    # coming from other computers on the network
    #comSocket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    s.bind(('', port))        
    print("socket binded to %s" %(port))
    
    # put the socket into listening mode
    s.listen(5)            
    
    # a forever loop until we interrupt it or 
    # an error occurs
    while True:
    
        # Establish connection with client.
        c, addr = s.accept()     
        print('Got connection from', addr)
        #get the command from the client interface
        cmd = c.recv(1024)
        print(cmd)
        #perform the command
        output_file = open("output_server_tcp.txt", "w")

        result = subprocess.run([cmd], stdout=subprocess.PIPE)
        output_file.write(result.stdout.decode())
        output_file.close()
        #print(result.stdout.decode())

        f = open("output_server_tcp.txt", "r")
        for line in f:
            print(line)
            #frame_send_message(line, addr, c)
            c.send(line.encode())
        f.close()

        # Close the connection with the client
        c.close()

if __name__ == "__main__":
    #port = int(sys.argv[1])
    port = 30000
    main(port)