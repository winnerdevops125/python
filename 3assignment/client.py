import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 10000)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Loop forever
while True:
    # Prompt the user for input
    command = input('Enter a command: ')

    # Send command to server
    sock.sendall(command.encode('utf-8'))

    # Receive response from server
    data = sock.recv(1024).decode('utf-8')
    print('Response: ', data)
