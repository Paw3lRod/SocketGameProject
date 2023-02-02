import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 10000)
print(f"Starting up on {server_address}")
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print("Waiting for a connection")
    connection, client_address = sock.accept()
    print(f"Connection from {client_address}")

    # Receive data in small chunks and retransmit it
    data = connection.recv(16)
    print(f"Received {data.decode()!r}")
    if data:
        print("Sending data back to the client")
        connection.sendall(data)
    else:
        print("No data from client")
        break

    # Clean up the connection
    connection.close()
