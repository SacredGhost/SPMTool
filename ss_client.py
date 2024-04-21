from watches import get_watch, Datatype
import socket
import json
import time
import traceback

def set_level():
    get_level = get_watch('Level')
    get_softlock = get_watch('Low HP TextBox / GSWF 420')
    current_level = get_level.read()
    current_softlock = get_softlock.read()
    if current_level != 99:
        get_level.write(99)
    if current_softlock != 16:
        get_softlock.write(16)

def send_data(sock, data):
    json_data = json.dumps(data)
    message = json_data + '\n'
    sock.sendall(message.encode())

get_username = get_watch("File Name")
previous_level = 1
initial_join = True

set_level()

score_required = []
xp = 0
for i in range(-1, 100):
    xp += ((i // 2) + 1) * 10000
    score_required.append(xp)

def manual_levelup(current_score):
    global previous_level
    max_hp = 10
    attack = 1
    
    level = 1
    for i in range(1, len(score_required)):
        if current_score >= score_required[i]:
            level += 1
        else:
            break

    for i in range(1, level + 1):
        if i % 2 != 0 and i != 1:
            attack += 1
        elif i != 1:
            max_hp += 5
    
    # Needs some sort of check for HP Plus and Attack Plus
    get_maxhp = get_watch("Max HP")
    get_hp = get_watch("HP")
    get_attack = get_watch("Attack")
    get_3DBar = get_watch("3D Bar")

    get_maxhp.write(max_hp)
    get_attack.write(attack)
    if previous_level != level:
        get_hp.write(max_hp)
        get_3DBar.write(10)
    previous_level = level

watch_list = {
    "HP" : {
        "addresses" : {
            "E": [0x804cea34, 0x804d02b4, 0x804d0434],
            "P": [0x80511a34, 0x80511a34],
            "J": [0x804a3d34, 0x804a5334],
            "K": [0x8054931c]
        },
    "datatype": Datatype.WORD
    },
    "Max HP" : {
        "addresses" : {
            "E": [0x804cea38, 0x804d02b8, 0x804d0438],
            "P": [0x80511a38, 0x80511a38],
            "J": [0x804a3d38, 0x804a5338],
            "K": [0x80549320]
        },
    "datatype": Datatype.WORD
    },
    "Attack" : {
        "addresses" : {
            "E": [0x804cea30, 0x804d02b0, 0x804d0430],
            "P": [0x80511a30, 0x80511a30],
            "J": [0x804a3d30, 0x804a5330],
            "K": [0x80549318]
        },
        "datatype": Datatype.WORD
    },
    "Coins" : {
        "addresses" : {
            "E": [0x804cea44, 0x804d02c4, 0x804d0444],
            "P": [0x80511a44, 0x80511a44],
            "J": [0x804a3d44, 0x804a5344],
            "K": [0x8054932c]
        },
        "datatype": Datatype.WORD
    },
    "Score" : {
        "addresses" : {
            "E": [0x804cea40, 0x804d02c0, 0x804d0440],
            "P": [0x80511a40, 0x80511a40],
            "J": [0x804a3d40, 0x804a5340],
            "K": [0x80549328]
        },
        "datatype": Datatype.WORD
    },
    "FlipFlop Pipe / GSWF 531 + GSWF 534" : { 
        # GSWF's are booleans stored on a byte with 7 other GSWF bits.
        # GSWF 531 is on Bit 5, and GSWF 534 is on Bit 2 of the below addresses
        "addresses" : {
            "E": [0x804e26d5, 0x804e3f55, 0x804e40d5],
            "P": [0x805256d5, 0x805256d5],
            "J": [0x804b79d5, 0x804b8fd5],
            "K": [0x8055d035]
        },
        "datatype": Datatype.BYTE
    },
    "Low HP TextBox / GSWF 420" : {
        "addresses" : {
        # GSWF 420 is stored on Bit 4 of the below addresses
            "E": [0x804e26cb, 0x804e3f48, 0x804e40cb],
            "P": [0x805256cb, 0x805256cb],
            "J": [0x804b79cb, 0x804b8fcb],
            "K": [0x8055d02b]
        },
        "datatype": Datatype.BYTE
    }
}

def main():
    global initial_join, watch_list
    username = get_username.read()
    previous_data = {}

    for key in watch_list:
        get_value = get_watch(key)
        value = get_value.read()
        previous_data[key] = value

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set this to localhost if you are running a local server or the server from the same machine as the client
    # Or set it to the provided IP of the person running the server
    server_ip = "localhost" 
    server_port = 5556 # Set this to the port of the server

    while True:
            try:
                # Connect to the server
                print(f'{"[" + "SharedStats" + "]":>15} connecting...')
                sock.connect((server_ip, server_port))
                break
            except socket.error as e:
                print(f'{"[" + "SharedStats" + "]":>15} Connection error: {e}')
                print('Trying again...')
                time.sleep(5)  # Wait for 5 seconds before attempting reconnection
    
    # Create Username
    print(f'{"[" + "SharedStats" + "]":>15} Connected to Server')
    sending = {
    'data': {},
    'message': [f'{"[" + username + "]":>15} has joined the channel'],
    'user': username,
    }

    send_data(sock, sending)
    print(f'{"[" + "SharedStats" + "]":>15} Waiting for updates')

    # Main Loop
    sock.settimeout(5)
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
                    get_score = get_watch("Score")
                    data = json.loads(part)

                    # Read Server / Current data
                    recived_data = {}
                    current_data = {}

                    set_level()
                    for key in watch_list:
                        if key in data['data']:
                            recived_data[key] = data['data'][key] # From Server
                            get_data = get_watch(f"{key}")
                            current_data[key] = get_data.read() # From Memory

                    # Find changes
                    changes = {}
                    for key in watch_list:
                        if key in data['data'] and initial_join:
                            changes[key] = current_data[key] - recived_data[key]
                        elif key in data['data']:
                            changes[key] = current_data[key] - previous_data[key]

                    # Send changelog
                    messages = []
                    if changes:
                        for key in changes:
                            if changes[key] != 0:
                                messages.append(f'{"[" + username + "]":>15} {key}: {changes[key]}')

                    # Send difference
                    if changes:
                        print("Sending...")
                        valid_send = True
                        if initial_join == False:
                            fix_score = get_score.read()
                            if changes['Score'] and changes['Score'] <= 0:
                                valid_send = False
                                fix_score = recived_data["Score"]
                            manual_levelup(fix_score)

                            if changes['Coins'] and changes['Coins'] <= 0:
                                valid_send = False

                            if changes['Max HP'] and changes["Max HP"] <= 0:
                                valid_send = False

                        sending = {
                            'data': changes,
                            'message': messages,
                            'user': username
                        }

                    if valid_send and initial_join == False:
                        send_data(sock, sending)

                    # Write received + change
                    for key in watch_list:
                        if key in data['data']:
                            get_data = get_watch(key)
                            if current_data[key] == previous_data[key] + changes[key] and initial_join:
                                initial_join = 2
                                continue
                            elif current_data[key] == recived_data[key] + changes[key] and initial_join == 2:
                                continue
                            else:
                                if initial_join:
                                    get_data.write(recived_data[key])
                                else:
                                    get_data.write(recived_data[key] + changes[key])

                    # Update previous data
                    if initial_join == 2:
                        for key in watch_list:
                            if key in data['data']:
                                previous_data[key] = recived_data[key]
                        initial_join = False
                    else:
                        for key in watch_list:
                            if key in data['data']:
                                previous_data[key] = recived_data[key] + changes[key]
                    manual_levelup(get_score.read())

                    # Print sent messages
                    if 'message' in data:
                        for message in data['message']:
                            print(message)

        except socket.timeout:
            # Handle timeout (no data received within the timeout period)
            print("Timeout: No data received from the server")
            continue
        # Handle Errors
        except json.JSONDecodeError:
            print(f'{"[" + "SharedStats" + "]":>15} Invalid JSON data received: {data}')
            continue

        except KeyboardInterrupt:
            # Close the socket
            print(f'{"[" + "SharedStats" + "]":>15} closing connection')
            sock.close()
        except ConnectionResetError:
            print(f'{"[" + "SharedStats" + "]":>15} The server has crashed or have been closed! Restarting client...')
            break
        except Exception as e:
            print(f'{"[" + "SharedStats" + "]":>15} Error:', traceback.print_exc(), e)
            time.sleep(.1)

if __name__ == '__main__':
    main()