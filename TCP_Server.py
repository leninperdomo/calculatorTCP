#Import the socket library to perform socket operations
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#Check if the absolute value of the input s is an integer after removing the decimal point
def is_number(s):
    sCopy = str(abs(float(s)))
    return sCopy.replace('.','',1).isdigit()

#Open a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Bind the socket using the given host and port numbers
    s.bind((HOST, PORT))
    try:
        while True:
            #Listen for and accept new connections
            s.listen()
            conn, addr = s.accept()

            #Check the data received
            with conn:
                #Read from the socket and extract the message string contents
                data = conn.recv(1024)
                if not data:
                    break
                messageString = str(data)
                messageString = messageString[2:-1]
                messageContents = messageString.split()

                #Check that the operator is valid and print the appropiate error message if not
                isValid = True
                if messageContents[0] != '+' and messageContents[0] != '-' and messageContents[0] != '*' and messageContents[0] != '/':
                    conn.send(b'620 Invalid_OC')
                    print(messageString + ' -> 620 -1')
                    isValid = False
                
                #Check that operands are valid numbers
                if (not messageContents[1].isnumeric() or not messageContents[2].isnumeric()):
                    conn.send(b'630 Invalid_Operand')
                    print(messageString + ' -> 630 -1')
                    isValid = False

                #Check for division by zero edge cases
                elif (messageContents[0] == '/' and messageContents[2] == '0'):
                    conn.send(b'630 Invalid_Operand')
                    print(messageString + ' -> 630 -1')
                    isValid = False

                #Calculate the result if the operation received is valid
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

                    #Remove any decimal points
                    resultStr = str(result)
                    if resultStr.endswith('.0'):
                        resultStr = resultStr[:-2]

                    #Send the result back
                    strToSend = '200 ' + resultStr
                    conn.send(strToSend.encode())

                #Send all the data back
                conn.sendall(data)

                #Print the operation received and its solution if it is valid
                if (isValid):
                    print(messageString + ' -> 200 ' + resultStr)

    #Stop the program by pressing ctrl+C
    except KeyboardInterrupt:
        s.close()
