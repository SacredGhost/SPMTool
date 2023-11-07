import socket

# Define the IP address and port to bind the server to
host = '0.0.0.0'  # Listen on all available network interfaces
port = 12345     # Choose a port (you can change this)

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
server_socket.bind((host, port))

print(f"UDP server listening on {host}:{port}")

while True:
    # Receive data and address from a client
    data, address = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes (adjust as needed)
    
    # Display the received data and client's address
    print(f"Received data from {address}: {data.decode('utf-8')}")

# Close the server socket (this won't be reached in this example)
server_socket.close()
