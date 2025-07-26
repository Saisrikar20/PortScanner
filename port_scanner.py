import socket
import threading
from colorama import Fore, Style, init

init(autoreset=True)

target = '192.168.29.1'
lock = threading.Lock()

def scan(port):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.settimeout(0.5)
        result = sckt.connect_ex((target, port))

        with lock:
            if result == 0:
                print(f"{Fore.GREEN}[OPEN     ] Port {port}")
            elif result == 111:
                print(f"{Fore.RED}[CLOSED   ] Port {port}")
            else:
                print(f"{Fore.YELLOW}[FILTERED ] Port {port}")
        sckt.close()

    except socket.timeout:
        with lock:
            print(f"{Fore.YELLOW}[FILTERED ] Port {port} (timeout)")
    except Exception as e:
        with lock:
            print(f"{Fore.MAGENTA}[ERROR    ] Port {port} — {e}")

for port in range(1, 100):
    thread = threading.Thread(target=scan, args=(port,))
    thread.start()
