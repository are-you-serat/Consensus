import re
import time
import requests
from icmplib import ping
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

file_lock = threading.Lock()

def get_ips_file():
    responce = requests.get('https://github.com/scriptzteam/Tor-Bridges-Collector/raw/main/bridges-obfs4')
    with open('obfs4/bridges-obfs4.txt', 'w', encoding='utf-8') as file:
        file.write(responce.text)

def extract_ips():
    with open('obfs4/bridges-obfs4.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if match:
            ip_address = match.group(1)
            with open('obfs4/ips.txt', 'a', encoding='utf-8') as file:
                file.write(ip_address + '\n')

def check_valid_ip(ip):
    host = ping(ip.strip(), count=3, timeout=1)
    if host.is_alive:
        print(ip.strip())
        with file_lock:
            with open(r'obfs4/valid.txt', 'a', encoding='utf-8') as file:
                file.write(ip.strip() + '\n')

def extract_valid_from_brindes_obfs4_list():
    with open(r'obfs4/valid.txt', 'r') as ip_file:
        ips = ip_file.readlines()

    with open(r'obfs4/bridges-obfs4.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(r'output_nodes.txt', 'w', encoding='utf-8') as output_file:
        for line in lines:
            for ip in ips:
                if ip.strip() in line:
                    output_file.write(line.strip() + '\n')

def remove_useless_files():
    try:
        print('Removing useless files')
        os.remove(r'obfs4/ips.txt')
        os.remove(r'obfs4/valid.txt')
        print('Completed')
    except FileNotFoundError:
        print('No useless files were found, continue working')


def run_tor_obfs4():
    parse_tor_question = int(input('Parse TOR bridges or use local servers file (1 - Parse, 0 - Use local one): '))
    remove_useless_files()
    if parse_tor_question == 1:
        get_ips_file()
    extract_ips()

    print('Data parsed and extracted')
    time.sleep(10)

    with open('obfs4/ips.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    print('Checking...')
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_valid_ip, ip) for ip in lines]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(e)

    extract_valid_from_brindes_obfs4_list()
    remove_useless_files()
    with open('output_nodes.txt', 'r') as file:
        lines = file.readlines()
    print(f'Well. Check output_nodes.txt. {len(lines)} bridges alive.')