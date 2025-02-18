import os
import socket
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
import re
import logging
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = os.environ.get('API_KEY', '')
if not API_KEY:
    raise NotImplementedError('`API_KEY` variable is not set with the SecurityTrails API key. Please set this before running. For more reference refer to: https://securitytrails.com/app/account/credentials')

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        logging.error(f"{Fore.RED}{Style.BRIGHT}Unable to resolve the domain name {domain}: {e}{Style.RESET_ALL}")
        return None

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        logging.info(f"{Fore.GREEN}{Style.BRIGHT}Port {port} is OPEN on {target}{Style.RESET_ALL}")
    sock.close()

def scan_ports(target, ports):
    logging.info(f"{Fore.CYAN}{Style.BRIGHT}Scanning {target} for open ports...{Style.RESET_ALL}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda port: scan_port(target, port), ports)

def enumerate_subdomains(domain):
    api_url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
    headers = {
        "APIKEY": API_KEY,
        "accept": "application/json",
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        subdomains = response.json().get("subdomains", [])
        logging.info(f"{Fore.YELLOW}{Style.BRIGHT}Found {len(subdomains)} subdomains for {domain}{Style.RESET_ALL}")
        return subdomains
    except requests.RequestException as e:
        logging.error(f"{Fore.RED}{Style.BRIGHT}Unable to enumerate subdomains for {domain}: {e}{Style.RESET_ALL}")
        return []

def crawl_urls(base_url):
    urls = set()
    try:
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    urls.add(full_url)
        logging.info(f"{Fore.MAGENTA}{Style.BRIGHT}Found {len(urls)} URLs for {base_url}{Style.RESET_ALL}")
    except requests.RequestException as e:
        logging.warning(f"{Fore.YELLOW}{Style.BRIGHT}Error crawling {base_url}: {e}{Style.RESET_ALL}")
    return urls

def main():
    target_domain = input("Enter target domain or IP: ").strip()

    # Validate and clean the input domain
    pattern = re.compile(r"https?://(www\.)?")
    target_domain = pattern.sub('', target_domain).strip().split('/')[0]

    if not target_domain:
        logging.error(f"{Fore.RED}{Style.BRIGHT}Invalid domain name. Please enter a valid domain.{Style.RESET_ALL}")
        return

    # Enumerate subdomains
    subdomains = enumerate_subdomains(target_domain)
    if not subdomains:
        logging.error(f"{Fore.RED}{Style.BRIGHT}No subdomains found.{Style.RESET_ALL}")
        return

    # Crawl URLs for each subdomain
    all_urls = set()
    for subdomain in subdomains:
        base_url = f"https://{subdomain}.{target_domain}"
        logging.info(f"{Fore.BLUE}{Style.BRIGHT}Scanning subdomain: {base_url}{Style.RESET_ALL}")
        urls = crawl_urls(base_url)
        all_urls.update(urls)

    # Scan ports for each URL
    port_range = range(1, 1025)  # Scanning common ports
    for url in all_urls:
        parsed_url = urlparse(url)
        ip_address = get_ip_address(parsed_url.netloc)
        if ip_address:
            scan_ports(ip_address, port_range)

if __name__ == "__main__":
    main()
