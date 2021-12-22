# calculatorTCP
Calculator Implemented with a Client and Server Over a TCP Connection and UDP Connection

The goal of this project was to implement a calculator that performs basic arithmetic operations using a TCP and UDP connection. The TCP program works in the following way: First, the client reads individual lines from a text that should contain a single mathematical operation. The client then sends each of these lines to the server
through a TCP socket. If the format of the equation sent by the client is correct, the server sends back the result along with the status code '200' to indicate no errors occurred. Otherwise, the server sends an error message with a different status code to indicate an error in the client's message. At each iteration, the client and the server both print the results of the operations they perform respectively.

A similar calculator program was also implemented over an unreliable connection using UDP. This version of the calculator handles cases when the message from the client is delayed or lost. The server does this by using a timer that measures how long it takes for the client's message to be received. The message is resent whenever a timeout occurs and the value of the timer is incremented. Once the timer reaches a certain value, the server determines that there was an error receiving the message and sends an error message back.
