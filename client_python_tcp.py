# Import socket module
import socket  
import time
import sys
import os

def get_valid_port():
    port = int(input('Enter port:'))
    if port > 65535:
        print("Invalid port number.")
        sys.exit()
    else:
        return port

def get_inputs_then_connect(s):
    try:
        address = input('Enter server name or IP address:')
        socket.inet_aton(address)
        port = get_valid_port()
        s.connect((address, port))
        return (address, port)
        
    except socket.error:
        print("Could not connect to server")
        sys.exit()
    

def parse_command(cmd):
    command = ''
    file_name = ''
    command_text = True

    for c in range(len(cmd)):
        if command_text:
            if cmd[c] == ">":
                command_text = False
            else:
                command = command + cmd[c]
        else:
            #remove extranous space at end of command
            if command[-1] == " ":
                command = command[:-1]
            elif cmd[c] != " ":
                file_name = cmd[c:]
                break
            else:
                pass
    return command, file_name
    
def send_user_command(s, connection):
    #get the command from the user
    cmd = input("Enter a command: ")
    cmd, file_name = parse_command(cmd)
    #establish a connection
    frame_send_message(cmd, s)

    return file_name

def frame_send_message(message, sock):
    #this breaks messages into blocks of 1024 bytes if needed
    
    framed_message = ''
    for c in range(len(message)):
        if (len(framed_message) < 1024) :
            framed_message = framed_message + message[c]

            if c == len(message) - 1:
                send_message(framed_message, sock)
        else:
            #send the framed message(can be less than 1024 bytes)
            send_message(framed_message, sock)
            #start building new framed_message
            framed_message = message[c]

def send_message(message, sock):
    #if the message has been broken up, the length with
    #be 1024 bytes
    print(message)
    print(type(message))
    sock.sendall(message.encode())


def main():
    # Create a socket object
    s = socket.socket()  
    s.settimeout(1)       
    
    # input the port and ip on which you want to connect then connect and send to server
    connection = get_inputs_then_connect(s)

    file_name = send_user_command(s, connection)

    while True:

        
        try:
            output = s.recv(1024)

        except socket.timeout:
            print("Could not fetch file.")
            sys.exit()
        if output:
            if file_name != '':
                with open(file_name,"a") as output_file:
                    
                    output_file.write(output.decode())
                    output_file.close()
            else:
                print(output.decode().rstrip())
        else:
            if(file_name != ''):
                print("File", file_name, "saved.")
            sys.exit()

    
    # close the connection
    s.close() 

if __name__ == "__main__":
    main()      
