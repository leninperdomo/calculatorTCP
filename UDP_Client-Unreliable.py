#Import the necessary libraries to implement UDP over an unreliable connection
import socket
import sys
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#Open the file with the operations texts
with open(sys.argv[-1], 'r', encoding="utf8") as inputFile:
    #Set the value of the timer
    d = 0.1

    #Open a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #Read each line from the text file
        fileLines = inputFile.readlines()
        for line in fileLines:
            #Initialize the status code with a value of '200' to indicate that no errors have occurred
            status_code = '200'

            #Remove the /n character at the end of each line
            message = line[:-1]

            #Check whether a message has been received
            received = False
            while received == False:
                #Start the timer for awaiting the next message
                s.settimeout(d)

                #Send the current operation to the server to solve
                s.sendto(message.encode('utf-8'), (HOST, PORT))

                try:
                    #Extract the data received back from the server and split it into tokens
                    data = s.recvfrom(1024)
                    data = str(data)
                    data = data[3:-24]
                    data = data = data.replace("'", "")
                    dataSplit = data.split()
                    
                    #Print the result if there are no errors in the message received and reset the timer
                    if (dataSplit[0] == '200'):
                        print('Result is ' + dataSplit[1])
                        d = 0.1
                        received = True

                    #Print the appropiate error message if there are any errors and reset the timer
                    else:
                        print('Error ' + dataSplit[0] + ': ' + dataSplit[1])
                        d = 0.1
                        received = True

                #Handle timeout exceptions when a message is not received on time
                except socket.timeout:
                    #Increment the value of the timer by multiplying it by two
                    d = 2*d
                    #Print an error message once the timer value exceeds a value of 2 and reset the timer
                    if d > 2:
                        print('Request timed out: the server is dead')
                        status_code = '300'
                        print('Error ' + status_code + ': request_time_out')
                        received = True
                        d = 0.1
                    #While the timer value limit has not been reached, reset the timer and indicate that the message is being resent
                    else:
                        print('Request timed out: resending')
