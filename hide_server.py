import socket
import threading
import time
import json
import random

TIME_DELAY = 0.06

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super(ClientHandler, self).__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server

        self.username = 'Guest' + str(random.randint(1000,9999))
        self.pixl_model = 200
        self.x = 0
        self.y = 0
        self.z = 0
        self.current_map = ''
        self.score = 0

    def run(self):
        print(f"Client {self.client_address} connected.")

        while True:
            try:
                # Receive data from the client
                data = self.client_socket.recv(1024)
                if not data:
                    break # Blank = Connection closed

                # Split the received data by newline (\n) to handle multiple JSON messages at once
                messages = data.decode("utf-8").split("\n")
                for message in messages:
                    if not message:
                        continue
                    # Parse the JSON data
                    try:
                        data = json.loads(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {self.client_address}: {e}")
                        continue

                    # Handle the JSON data here
                    # print(f"Received from {self.username}: {data}")

                    if 'username' in data:
                        self.username = data['username']

                    if 'x' in data:
                        self.x = data['x']

                    if 'y' in data:
                        self.y = data['y']

                    if 'z' in data:
                        self.z = data['z']

                    if 'current_map' in data:
                        self.current_map = data['current_map']

            except Exception as e:
                print(f"Error while receiving data from {self.client_address}: {e}")
                break

        # Close the client socket when the loop breaks
        self.client_socket.close()
        print(f"Client {self.client_address} disconnected.")

        # Remove the disconnected client from the connections dictionary
        del self.server.connections[self.client_address]

class Server(threading.Thread):
    def __init__(self, host, port):
        super(Server, self).__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self.connections = {}

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                client_handler = ClientHandler(client_socket, client_address, self)
                client_handler.start()

                # Store the client handler in the dictionary for future reference
                self.connections[client_address] = client_handler

            except Exception as e:
                print(f"Error accepting connection: {e}")

    def stop(self):
        self.server_socket.close()

class Game(threading.Thread):
    def __init__(self, server):
        super(Game, self).__init__()
        self.server = server

    def run(self):
        # Add your main game logic here
        while True:
            # Access the connections dictionary in the Server class from the Game class
            all_connections = self.server.connections

            # Game logic to be executed periodically
            time.sleep(TIME_DELAY)

if __name__ == "__main__":
    # Set your desired host and port for the server
    HOST = '0.0.0.0'
    PORT = 8080

    server = Server(HOST, PORT)
    server.start()

    game_thread = Game(server) # Server is passed to give Game access to Server data
    game_thread.start()

    try:
        while True:
            if server.connections:
                all_clients_data = []
                for connection in server.connections:
                    client_info = server.connections[connection]
                    client_data = {
                        'username': client_info.username,
                        'pixl_model': client_info.pixl_model,
                        'x': client_info.x,
                        'y': client_info.y,
                        'z': client_info.z,
                        'current_map': client_info.current_map,
                        'score': client_info.score,
                    }
                    all_clients_data.append(client_data)

                json_data = json.dumps(all_clients_data)
                json_data += '\n'

                for connection in server.connections:
                    sock = server.connections[connection].client_socket
                    sock.send(json_data.encode())

                time.sleep(TIME_DELAY)
    except KeyboardInterrupt:
        server.stop()
