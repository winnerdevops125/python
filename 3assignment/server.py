import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Dictionary to store account balances
accounts = {}

# Loop forever
while True:
    # Wait for a connection
    print('Waiting for a connection...')
    connection, client_address = sock.accept()

    try:
        print('Connection from', client_address)

        # Receive and process client requests
        while True:
            data = connection.recv(1024)
            if not data:
                break

            message = data.decode('utf-8').strip().split()
            command = message[0]

            if command == 'CREATE_ACCOUNT':
                account_name = message[1]
                initial_balance = int(message[2]) * 100  # Convert dollars to cents
                if account_name in accounts:
                    response = '1 Account already exists'
                else:
                    accounts[account_name] = initial_balance
                    response = '0 Account created'

            elif command == 'DEPOSIT':
                account_name = message[1]
                amount = int(message[2]) * 100  # Convert dollars to cents
                if account_name in accounts:
                    accounts[account_name] += amount
                    response = '0 Deposit successful'
                else:
                    response = '2 Account does not exist'

            elif command == 'WITHDRAW':
                account_name = message[1]
                amount = int(message[2]) * 100  # Convert dollars to cents
                if account_name in accounts:
                    if accounts[account_name] >= amount:
                        accounts[account_name] -= amount
                        response = '0 Withdrawal successful'
                    else:
                        response = '3 Insufficient funds'
                else:
                    response = '2 Account does not exist'

            elif command == 'CHECK_BALANCE':
                account_name = message[1]
                if account_name in accounts:
                    balance = accounts[account_name]
                    response = '0 Balance: ${:.2f}'.format(balance / 100)  # Convert cents to dollars for display
                else:
                    response = '2 Account does not exist'

            else:
                response = '4 Unknown command'

            # Send response to client
            connection.sendall(response.encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()
