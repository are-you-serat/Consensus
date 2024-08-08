import time
import requests
from bs4 import BeautifulSoup
import re
import os
from requests_doh import DNSOverHTTPSSession, add_dns_provider
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

file_lock = threading.Lock()

def parse_DOH():
    try:
        response = requests.get('https://github.com/curl/curl/wiki/DNS-over-HTTPS')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'dns-query$'))
        for link in links:
            full_url = link['href']
            with open(r'DNS\dns_servers.txt', 'a') as file:
                file.write(full_url + '\n')
        print('Data received. Testing for DOH functionality begins')
    except Exception as e:
        print(e)

def check(line):
    try:
        name = line.strip()
        add_dns_provider(name=name, address=name)
        session = DNSOverHTTPSSession(name)
        r = session.get("https://google.com/", timeout=10)
        if r.status_code == 200:
            print(name)
            with file_lock:
                with open('valid_doh_servers.txt', 'a', encoding='utf-8') as file:
                    file.write(name + '\n')
    except Exception:
        pass

def run_dns():
    parse_DOH_question = int(input('Parse DOH servers or use local servers file (1 - Parse, 0 - Use local one): '))
    if parse_DOH_question == 1:
        try:
            os.remove('DNS\dns_servers.txt')
        except FileNotFoundError:
            pass
        parse_DOH()
    time.sleep(15)

    with open('DNS/dns_servers.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check, line) for line in lines]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(e)