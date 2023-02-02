import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the address and port of the server
server_address = ('localhost', 10000)
print(f"Connecting to {server_address}")
sock.connect(server_address)

try:
    # Send data
    message = b"This is a message"
    print(f"Sending {message}")
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(f"Received {data.decode()!r}")
finally:
    # Clean up the socket
    print("Closing the socket")
    sock.close()
