import socket
import time


# Create a TCP/IP socket
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print ('connecting to {} port {}'.format (*server_address))
sock.connect(server_address)

try:
    # Send data
    message = b'00010sinitservi'
    print ('sending {!r}'.format (message))
    sock.sendall (message)
    while True:
    # Look for the response
        print ("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv (5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len (data)
            print('received {!r}'.format(data))
            print ("Processing ...")
            print ("Send answer (if needed)")
finally:
        print ('closing socket')
        sock.close()