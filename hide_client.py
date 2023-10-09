import socket
import threading
import json
import time
import dolphin_memory_engine as dme
from hide_pixl import *
from hide_teleport import *

TIME_DELAY = .06

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.pixls = [Pixl(0), Pixl(1), Pixl(2), Pixl(3)]
        self.server_data = []
        self.pixl_model = 200

        # Data to send
        self.username = ""
        self.map_name = ''
        self.x = 1
        self.y = 1
        self.z = 1
        self.current_map = 'empty'
        self.score = 0

    def connect(self):
        try:
            # Establish username and connection to server.
            self.username = input('Username: ')

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.connected = True

        except ConnectionRefusedError:
            print(f"Error: The server at {self.host}:{self.port} refused the connection. (likely server down)")
        except socket.timeout:
            print(f"Error: Connection to the server at {self.host}:{self.port} timed out.")
        except OSError as e:
            print(f"Error: OS-related issue occurred - {e}")
        except Exception as e:
            print(f"Error: connecting to the server - {e}")

        try:
            # Once connected Start threads
            if self.connected:
                send_thread = threading.Thread(target=self.send_data)
                recv_thread = threading.Thread(target=self.receive_data)
                update_thread = threading.Thread(target=self.update_memory)

                send_thread.start()
                recv_thread.start()
                update_thread.start()

                send_thread.join()
                recv_thread.join()
                update_thread.join()

        except Exception as e:
            print(f"Error in one of the main threads: {e}")

    def send_data(self):
        while self.connected:
            try:
                # Prepare the data as a dictionary
                data = {
                    "username": self.username,
                    "x": self.x,
                    "y": self.y,
                    "z": self.z,
                    "current_map": self.current_map,
                }
                json_data = json.dumps(data) # convert to JSON

                if self.connected:
                    # Add a newline character at the end of the JSON data as a delimiter
                    json_data += '\n'

                    self.client_socket.send(json_data.encode())
                    time.sleep(TIME_DELAY)

            except Exception as e:
                print(f"Error sending data: {e}")
                self.connected = False

    def receive_data(self):
        # Receive data from the server and update the client.self
        while True:
            try:

                # Receive data from the server
                data = self.client_socket.recv(1024)
                if not data: # Blank = Connection closed
                    break 

                # Split the received data by newline (\n) delimiter
                messages = data.decode("utf-8").split("\n")
                for message in messages:
                    if not message:
                        continue
                    # Parse the JSON data
                    try:
                        data = json.loads(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from server: {e}")
                        continue
                    # Handle the JSON data here
                    # print(f"Receiving data from server.")

                    self.server_data = data

                    if 'score' in data[0]:
                        self.score = int(data[0]['score'])

            except socket.error:
                print("Connection to the server lost.")
                self.connected = False
                break

            except Exception as e:
                print(f"Error receiving data from the server: {e}")
                self.connected = False
                break

        # Close the client socket when the connection is lost
        if self.client_socket:
            self.client_socket.close()

    def update_memory(self):
        # Connect to Dolphin
        dme.hook()

        # Wait if Dolphin isn't hooked
        if not dme.is_hooked():
            print('Not Hooked, waiting for connection to Dolphin')
            while not dme.is_hooked():
                time.sleep(0.01)
                dme.hook()
            print('Hooked')
        else:
            print('Hooked')

        # Find Memory Addresses
        x_address = get_watch('Coordinate X')
        y_address = get_watch('Coordinate Y')
        z_address = get_watch('Coordinate Z')
        current_map_address = get_watch('Map to Save')
        score_address = get_watch('Score')
        sequence_position = get_watch('Sequence Position')

        self.update_pixls()
        sequence_position.write(420)

        while self.connected:
            # Read Game Memory
            self.x = x_address.read()
            self.y = y_address.read()
            self.z = z_address.read()
            self.current_map = MemoryWatch.read(current_map_address)

            # Update Game Memory
            score_address.write(self.score)

            self.update_pixls()

            # Find all users on the same map sort by closest
            user_list = []
            same_map = []
            closest_players = []

            for user in self.server_data:
                user_list.append(user)
                if user['current_map'] == self.current_map and user['username'] != self.username:
                    same_map.append(user)
            
            for user in same_map:
                distance_x = abs(self.x - user['x'])
                distance_y = abs(self.y - user['y'])
                distance = distance_x + distance_y
                closest_players.append((user, distance))
            
            closest_players = sorted(closest_players, key=lambda x: x[1])
            for i, player in enumerate(closest_players):
                closest_players[i] = player[0]

            players = ''
            for player in user_list:
                players += player['username'] + ' '
            print(f'Players connected: {players}', end='\r', flush=True)
            
            # Move pixls
            self.update_pixls()
            for i, pixl in enumerate(self.pixls):
                pixl.isActive.write(True)
                pixl.state.write(PixlState.STAY)
                try:
                    pixl.setPosition(closest_players[i]['x'], closest_players[i]['y'], closest_players[i]['z'])
                except IndexError:
                    pixl.setPosition(0, -1000, 0)
                    
            time.sleep(TIME_DELAY)

    def update_pixls(self):
        delete_pixls = []
        for i in range(5,12):
            delete_pixls.append(get_watch(f'Pixl slot {i}'))

        for pixl in delete_pixls:
            pixl.write(0x0000000)

        activate_pixls = []
        for i in range(1,5):
            activate_pixls.append(get_watch(f'Pixl slot {i}'))

        for pixl in activate_pixls:
            pixl.write(0x0010200)

if __name__ == "__main__":
    host = "34.125.119.174"  
    port = 8080 

    client = Client(host, port)
    client.connect()