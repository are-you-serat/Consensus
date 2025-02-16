import time
import requests
import re
import os
import threading
from threading import Lock
from icmplib import ping
from concurrent.futures import ThreadPoolExecutor, as_completed

file_lock = Lock()

def remove_useless_files():
    try:
        print('Removing useless files')
        os.remove(r'vanilla\ips.txt')
        os.remove(r'vanilla\valid.txt')
        print('Completed')
    except FileNotFoundError:
        print('No useless files were found, continue working')

def parse_tor_bridges():
    response = requests.get('https://drew-phillips.com/tor-node-list.txt')
    with open(r'vanilla\tor-node-list.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

def extract_ip(bridges):
    print('Data received. Testing for bridge functionality begins. Extracting IP...')
    pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    matches = pattern.findall(bridges)
    with open(r'vanilla\ips.txt', 'w') as file:
        for match in matches:
            file.write(match + '\n')

def check_valid_ip(ip):
    host = ping(ip.strip(), count=3, timeout=1)
    if host.is_alive:
        print(ip.strip())
        with file_lock:
            with open(r'vanilla\valid.txt', 'a', encoding='utf-8') as file:
                file.write(ip.strip() + '\n')

def extract_valid_from_tor_node_list():
    with open(r'vanilla\valid.txt', 'r') as ip_file:
        ips = ip_file.readlines()

    with open(r'vanilla\tor-node-list.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(r'output_nodes.txt', 'w', encoding='utf-8') as output_file:
        for line in lines:
            for ip in ips:
                if ip.strip() in line:
                    bridge = line.split()
                    if len(bridge) == 6:
                        ip = bridge[1]
                        port = bridge[2]
                        fingerprint = bridge[4]
                        output_file.write(ip + ':' + port + '\n' + fingerprint + '\n')

def run_tor_vanilla():
    parse_tor_question = int(input('Parse TOR bridges or use local servers file (1 - Parse, 0 - Use local one): '))
    remove_useless_files()
    if parse_tor_question == 1:
        parse_tor_bridges()
    with open(r'vanilla\tor-node-list.txt', 'r', encoding='utf-8') as file:
        bridges = file.read()
    extract_ip(bridges)
    time.sleep(15)

    with open(r'vanilla\ips.txt', 'r') as file:
        lines = file.readlines()

    print('Checking...')
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_valid_ip, ip) for ip in lines]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(e)

    extract_valid_from_tor_node_list()
    remove_useless_files()
    with open('output_nodes.txt', 'r') as file:
        lines = file.readlines()
    print(f'Well. Check output_nodes.txt. {len(lines)} bridges alive.')