#Import the socket library to perform socket operations
import socket
#Import the sys library to read command line arguments
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#Open th file with the operations
with open(sys.argv[-1], 'r', encoding="utf8") as inputFile:
    #Open a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #Read each line from the file
        fileLines = inputFile.readlines()
        for line in fileLines:

            #Connect to the appropiate host and port numbers
            s.connect((HOST, PORT))
            #Remove the /n character at the end of every line
            message = line[:-1]
            
            #Send all the characters in each line to the server
            s.sendall(message.encode('utf-8'))

            #Receive the result sent back by the server
            data = s.recv(1024)
            data = str(data)
            data = data[2:-1]

            #Split the message receieved into tokens
            dataSplit = data.split()

            #Check that no errors occurred and print the result
            if (dataSplit[0] == '200'):
                print('Result is ' + dataSplit[1])
            #If an error occurred, print the appropiate error message
            else:
                print('Error ' + dataSplit[0] + ': ' + dataSplit[1])
