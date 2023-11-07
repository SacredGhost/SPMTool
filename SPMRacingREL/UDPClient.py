import socket

# Define the server's IP address and port
server_host = '127.0.0.1'  # Replace with the server's IP address
server_port = 12345        # Replace with the server's port

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message to send to the server (or 'exit' to quit): ")

    if message.lower() == 'exit':
        break

    # Send the message to the server
    client_socket.sendto(message.encode('utf-8'), (server_host, server_port))

# Close the client socket
client_socket.close()
