import socket
import threading
import json
import time

# List to store client connections
socket_list = []

messages_lock = threading.Lock()
messages = []

usernames_lock = threading.Lock()
usernames = {}

stats_lock = threading.Lock()
stats = {
    'Score': 0,
    'HP': 10,
    'Max HP': 10,
    'Attack': 1,
    'Coins': 0,
    'Level': 1,
    'FlipFlop Pipe': 0,
    'Low HP Textbox': 16,
}

# File path for the stats save file
SAVE_FILE_PATH = 'stats.json'

# Locks for thread synchronization
save_file_lock = threading.Lock()

def load_stats():
    global stats
    try:
        with open(SAVE_FILE_PATH, 'r') as file:
            saved_stats = json.load(file)
            stats.update(saved_stats)
            print("Stats loaded from the save file.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Save file not found or invalid format. Using default stats.")

def save_stats():
    global stats
    with save_file_lock:
        with open(SAVE_FILE_PATH, 'w') as file:
            json.dump(stats, file)
            print('[Stats Saved]')
            print(stats)

def send_data():
    global messages
    global stats
    while True:
        time.sleep(0.1)

        with messages_lock:
            with stats_lock:
                if stats:
                    sending = {
                        'data': stats.copy(),
                        'message': messages.copy(),
                    }
                    messages.clear()

                    if socket_list:
                        # Send dictionary over a socket
                        json_data = json.dumps(sending)
                        message = json_data + '\n'

                        # Send data to all connected clients
                        for connection in socket_list:
                            try:
                                connection.sendall(message.encode())
                            except BrokenPipeError:
                                # Handle broken pipe error
                                print("Broken pipe error. Client disconnected.")
                                connection.close()
                                if connection in socket_list:
                                    socket_list.remove(connection)

def handle_client(sock, addr):
    try:
        while True:
            # Receive data from client
            data = sock.recv(4096)
            if not data:
                continue

            # Split the received data by newline character
            parts = data.decode().split('\n')

            # Process each received JSON string individually
            for part in parts:
                if not part:
                    continue
                try:
                    # Parse the JSON string into a Python object
                    data = json.loads(part)

                    if 'message' in data:
                        with messages_lock:
                            messages.extend(data['message'])

                    if 'data' in data and data['data'] and data['data']['Score'] >= 0:
                        with stats_lock:
                            # Check if the data changed is in the stats dictionary
                            for key in data['data']:
                                if key in stats:
                                    stats[key] += data['data'][key]
                except json.JSONDecodeError:
                    pass
                    # print(f"Invalid JSON data received from client {addr}. Skipping.")

    except (ConnectionResetError, ConnectionAbortedError):
        # Client disconnected
        print(f"Client {addr} disconnected.")

    finally:
        # Remove client from socket list if it still exists
        if sock in socket_list:
            sock.close()
            if sock in socket_list:
                socket_list.remove(sock)

def main():
    # Load stats from save file
    load_stats()

    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            # Bind the socket to a specific IP address and port
            sock.bind(('0.0.0.0', 8080)) # this will open the whole server up to any connections to port 8080
            break

        except Exception as e:
            print(e)
            print('Sleeping for 5 seconds')
            time.sleep(5)

    # Listen for incoming connections
    sock.listen(5)
    print("Server started. Listening for connections...")

    # Send messages to clients
    sending_thread = threading.Thread(target=send_data)
    sending_thread.start()

    # Start a thread to save stats periodically
    saving_thread = threading.Thread(target=save_stats_periodically)
    saving_thread.start()

    while True:
        # Accept a client connection
        client_socket, client_address = sock.accept()
        print(f"Client {client_address} connected.")

        # Add client to the socket list
        socket_list.append(client_socket)

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def save_stats_periodically():
    while True:
        time.sleep(10)  # Save stats every 10 seconds
        save_stats()

if __name__ == "__main__":
    main()
