import socket
import time
import json
from watches import *

# Hook Python to Dolphin
dme.hook()

username = get_watch("File Name")
max_hp = get_watch("Max HP")
hp = get_watch("HP")
points = get_watch("Score")
coins = get_watch("Coins")
sequence = get_watch("SequencePosition")
username = get_watch("File Name")
player_x = get_watch("Mario_X")
player_y = get_watch("Mario_Y")
player_z = get_watch("Mario_Z")
current_map = get_watch("CurrentMap")
item1 = get_watch("Item Slot 1")
item2 = get_watch("Item Slot 2")
item3 = get_watch("Item Slot 3")
item4 = get_watch("Item Slot 4")
item5 = get_watch("Item Slot 5")
item6 = get_watch("Item Slot 6")
item7 = get_watch("Item Slot 7")
item8 = get_watch("Item Slot 8")
item9 = get_watch("Item Slot 9")
item10 = get_watch("Item Slot 10")

# Define the server's IP address and port
server_host = '127.0.0.1'  # Replace with the server's IP address
server_port = 12345        # Replace with the server's port

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    time.sleep(.01)
    data = {
        "max_hp": max_hp.read(), 
        "hp": hp.read(),
        "points": points.read(),
        "coins": coins.read(),
        "sequence": sequence.read(),
        "player_x": player_x.read(),
        "player_y": player_y.read(),
        "player_z": player_z.read(),
        "current_map": current_map.read(),
        "item1": item1.read(),
        "item2": item2.read(),
        "item3": item3.read(),
        "item4": item4.read(),
        "item5": item5.read(),
        "item6": item6.read(),
        "item7": item7.read(),
        "item8": item8.read(),
        "item9": item9.read(),
        "item10": item10.read(),
    }
    message = {
        "username": username.read(),
        "data": data
    }

    message = json.dumps(message)
    # Send the message to the server
    client_socket.sendto(message.encode('utf-8'), (server_host, server_port))
    print("data sent")

# Close the client socket
client_socket.close()
