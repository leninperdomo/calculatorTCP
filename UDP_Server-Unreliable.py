#Import the necessary libraries to implement UDP over an unreliable connection
import socket
import sys
import random

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#Seed a random value to check whether or not to drop a packet
p = sys.argv[1]
p = float(p)
rand = random.seed(sys.argv[2])

#Check if the absolute value of a number string is a digit
def is_number(s):
    sCopy = str(abs(float(s)))
    return sCopy.replace('.','',1).isdigit()

#Start a new socket connection
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #Bind the socket using the appropiate host and port numbers
    s.bind((HOST, PORT))

    #Receive data from the client while there is data to be received
    while True:
        try:
            data, addr = s.recvfrom(1024)
        
            #Drop the packet depending on the value of a randomly generated seed
            if random.random() <= p:
                print(str(data)[2:-1] + ' -> dropped')
                continue

            #Split the message string receieved into tokens
            messageString = str(data)
            messageString = messageString[2:-1]
            messageContents = messageString.split()

            #Check whether the operation received is valid
            isValid = True

            #Store the result after performing the operation
            result = -1
            resultStr = str(result)

            #Initialize the status code witha value of '200' to indicate that no errors have occurred
            status_code = '200'

            #Print an appropiate error message if the operators are invalid
            if messageContents[0] != '+' and messageContents[0] != '-' and messageContents[0] != '*' and messageContents[0] != '/':
                strToSend = '620 ' + resultStr
                s.sendto(strToSend.encode(), addr)
                isValid = False
                status_code = '620'

            #Print an appropiate error message if the operands are invalid
            if (not messageContents[1].isnumeric() or not messageContents[2].isnumeric()):
                strToSend = '630 ' + resultStr
                s.sendto(strToSend.encode(), addr)
                isValid = False
                status_code = '630'

            #Handle the edge case for division by zero
            elif (messageContents[0] == '/' and messageContents[2] == '0'):
                strToSend = '630 ' + resultStr
                s.sendto(strToSend.encode(), addr)
                isValid = False
                status_code = '630'

            #Calculate the result of the operation received if it is valid
            if (isValid):
                result = 0
                if (messageContents[0] == '+'):
                    result = float(messageContents[1]) + float(messageContents[2])
                if (messageContents[0] == '-'):
                    result = float(messageContents[1]) - float(messageContents[2])
                if (messageContents[0] == '*'):
                    result = float(messageContents[1]) * float(messageContents[2])
                if (messageContents[0] == '/'):
                    result = float(messageContents[1]) / float(messageContents[2])

                #Remove any decimal points from the result
                resultStr = str(result)
                if (resultStr.endswith('.0')):
                    resultStr = resultStr[:-2]

                #Send the message with the result back to the client
                strToSend = '200 ' + resultStr
                s.sendto(strToSend.encode(), addr)

            #Print the message string along with its respective status code and result value
            print(messageString + ' -> ' + status_code + ' ' + resultStr)

        #Stop the program by pressing ctrl+C
        except KeyboardInterrupt:
            exit(0)
