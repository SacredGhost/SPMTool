import dolphin_memory_engine as dme
import socket
import json
import time
from memory import *

def send_data(sock, data):
    # Send dictionary over a socket.
    json_data = json.dumps(data)
    message = json_data + '\n'
    sock.sendall(message.encode())

def read_data(data):
    # Find memory inside Dolphin returns value
    type = type_key[data_type[data]]
    address = data_address[data]
    if type == 'type_byte':
        return dme.read_byte(address)
    if type == 'type_halfword':
        return dme.read_word(address)
    if type == 'type_word':
        return dme.read_word(address)
    if type == 'type_float':
        return dme.read_float(address)
    if type == 'type_double':
        return dme.read_double(address)
    if type == 'type_string':
        return dme.read_string(address)
    if type == 'type_byteArray':
        return dme.read_byteArray(address)
    if type == 'type_num':
        return dme.read_num(address)
    
def write_data(data, value):
    # Find memory inside Dolphin writes value
    type = type_key[data_type[data]]
    address = data_address[data]
    if type == 'type_byte':
        dme.write_byte(address, value)
    if type == 'type_halfword':
        dme.write_word(address, value)
    if type == 'type_word':
        dme.write_word(address, value)
    if type == 'type_float':
        dme.write_float(address, value)
    if type == 'type_double':
        dme.write_double(address, value)
    if type == 'type_string':
        dme.write_string(address, value)
    if type == 'type_byteArray':
        dme.write_byteArray(address, value)
    if type == 'type_num':
        dme.write_num(address, value)

def main():
    username = input('Username: ')
    # Stats shared between clients / server
    watch_list = ['HP', 'Max HP', 'Attack', 'Coins', 'Score', 'Level', 'FlipFlop Pipe', 'Low HP Textbox']

    # Connect to Dolphin
    dme.hook()

    # Wait if Dolphin isn't hooked
    if not dme.is_hooked():
        print('Not Hooked, waiting for connection to Dolphin')
        while not dme.is_hooked():
            time.sleep(0.01)
            dme.hook()
        print(f'{"[" + "Console" + "]":>15} Hooked')
    else:
        print(f'{"[" + "Console" + "]":>15} Hooked')

    # Read games data
    previous_data = {}

    for key in watch_list:
        value = read_data(key)
        previous_data[key] = value

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get the server's IP address and port
    server_ip = '' # Input the server's external IP address
    server_port = 8080 # use any port that you've opened to the public 

    while True:
        try:
            # Connect to the server
            print(f'{"[" + "Console" + "]":>15} connecting...')
            sock.connect((server_ip, server_port))
            break
        except socket.error as e:
            print(f'{"[" + "Console" + "]":>15} Connection error: {e}')
            print('Trying again...')
            time.sleep(5)  # Wait for 5 seconds before attempting reconnection

    # Create Username
    print(f'{"[" + "Console" + "]":>15} Connected to Server')
    sending = {
    'data': {},
    'message': [f'{"[" + username + "]":>15} has joined the channel'],
    'user': username,
    }

    send_data(sock, sending)
    print(f'{"[" + "Console" + "]":>15} Waiting for updates')

    # Main loop
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                continue

            # Check for delimiters / Create a TCP queue
            decoded_data = data.decode('utf-8')
            parts = [part.strip() for part in decoded_data.split('\n')]
            for part in parts:
                if part:
                    data = json.loads(part)

                    # Read Server / Current data
                    received_data = {}
                    current_data = {}
                    for key in watch_list:
                        if key in data['data']:
                            received_data[key] = data['data'][key]  # From Server
                            current_data[key] = read_data(key)      # From Memory

                    # Find changes
                    changes = {} 
                    for key in watch_list:
                        if key in data['data']:
                            changes[key] = current_data[key] - previous_data[key] 

                    # Send changelog
                    messages = []
                    if changes:
                        for key in changes:
                            if changes[key] != 0:
                                messages.append(f'{"[" + username + "]":>15} {key}: {changes[key]}')

                    # Send difference
                    valid_send = True
                    if changes:

                        # don't send data if the data doesn't meet the requirements.
                        if changes['Level'] and changes['Level'] > abs(1):
                            valid_send = False

                        if changes['Score'] and changes['Score'] <= 0:
                            valid_send = False

                        if changes['Max HP'] and changes['Max HP'] <= 0:
                            valid_send = False

                        if changes['Max HP'] and changes['Max HP'] > 5:
                            valid_send = False

                        if changes['Attack'] and changes['Attack'] <= 0:
                            valid_send = False

                        if changes['Attack'] and changes['Attack'] > 1:
                            valid_send = False

                        sending = {
                            'data': changes,
                            'message': messages,
                            'user': username,
                            }

                    if valid_send:
                        send_data(sock, sending)

                    # Write received + change
                    for key in watch_list:
                        if key in data['data']:
                            if current_data[key] == received_data[key] + changes[key]:
                                continue
                            else:
                                write_data(key, received_data[key] + changes[key])
                
                    # Update previous data
                    for key in watch_list:
                        if key in data['data']:
                            previous_data[key] = received_data[key] + changes[key]
                    
                    # Print sent messages
                    if 'message' in data:
                        for message in data['message']:
                            print(message)

        # Handle Errors
        except json.JSONDecodeError:
            print(f'{"[" + "Console" + "]":>15} Invalid JSON data received:')
            continue

        except KeyboardInterrupt:
            # Close the socket
            print(f'{"[" + "Console" + "]":>15} closing connection')
            sock.close()

        except Exception as e:
            print(f'{"[" + "Console" + "]":>15} Error:', e)
            time.sleep(.1)

if __name__ == '__main__':
    main()