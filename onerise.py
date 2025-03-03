#!/usr/bin/env python3
# coded by vbiskit 

import aiohttp
import re
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import os
from colorama import Fore
from urllib.parse import urlparse, parse_qs
import sys
import argparse
import asyncio
import io

def fetch_metadata():
    url = "https://raw.githubusercontent.com/vbiskit/oneRise/refs/heads/main/metadata.json"
    return requests.get(url).json()

metadata = fetch_metadata()

user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    # ... (other user agents remain the same)
]

def rgb(r, g, b, text):
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

def blue_green(text):
    gradient_colors = [
        (0, 180, 255),  
        (0, 220, 220),  
        (0, 255, 180),  
        (0, 255, 120),  
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def blue2(text):
    gradient_colors = [
        (0, 0, 255),       
        (0, 102, 255),     
        (0, 191, 255),     
        (30, 144, 255),    
        (70, 130, 180),    
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def vibrant_yellow_green(text):
    gradient_colors = [
        (255, 255, 0),   
        (220, 255, 0),   
        (180, 255, 0),   
        (120, 255, 0),  
        (60, 255, 0),    
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def get_random_user_agent():
    return random.choice(user_agents)

async def check_username_on_website(session, site, username):
    url = site["uri_check"].replace("{account}", username)
    headers = {"User-Agent": get_random_user_agent()}

    try:
        async with session.get(url, headers=headers, timeout=19.6) as response:
            raw_bytes = await response.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("latin-1")

            if response.status == site["e_code"] and site["e_string"] in text:
                print(f"\033[38;2;255;255;255m[\033[38;2;0;191;255m{site['name']}\033[38;2;255;255;255m] \033[38;2;255;255;255m[\033[38;2;0;255;0m{site['cat']}\033[38;2;255;255;255m] {Fore.LIGHTBLACK_EX}{url}")
                return (site["name"], url, site["cat"])

            if "m_code" in site and "m_string" in site:
                if response.status == site["m_code"] and site["m_string"] in text:
                    return None

            return None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None

async def check_username_with_retries(session, site, username, max_retries=1):
    for attempt in range(max_retries):
        result = await check_username_on_website(session, site, username)
        if result is not None:
            return result
        await asyncio.sleep(0.03)  
    return None

def print_banner():
    logo = r"""                                                                    
    ______    _____  ___    _______   _______    __      ________  _______  
   /    " \  (\"   \|"  \  /"     "| /"      \  |" \    /"       )/"     "| 
  // ____  \ |.\\   \    |(: ______)|:        | ||  |  (:   \___/(: ______) 
 /  /    ) :)|: \.   \\  | \/    |  |_____/   ) |:  |   \___  \   \/    |   
(: (____/ // |.  \    \. | // ___)_  //      /  |.  |    __/  \\  // ___)_  
 \        /  |    \    \ |(:      "||:  __   \  /\  |\  /" \   :)(:      "| 
  \"_____/    \___|\____\) \_______)|__|  \___)(__\_|_)(_______/  \_______)  
  """
    print(f"{logo}\n")
    print(" coded by biskit V 7.2\n")
    print(" -h to see Usage and Arguments\n")
    print(" \033[38;2;255;255;255m[\033[38;5;214mWRN\033[38;2;255;255;255m]\033[38;2;255;255;255m This is Private\033[38;2;255;255;255m\n")

def setup_argparse():
    class CustomHelpFormatter(argparse.HelpFormatter):
        def format_help(self):
            help_text = """
Arguments:
  -sf  Save the output to a file
  -bf brute-force usernames from a .txt file
  -all Search With Duckduckgo And Userlinks
  -bd brute-force usernames with duckduckgo
  -bsn brute-force similar names (e.g., vbiskit -> biskit, biskit069)
  -bf name,name2
  -bd name,name2
  -bsn search similar names of that user
Usage:
  - python3 onerise <example> -sf example.txt
  - python3 onerise <example> for just links
  - python3 onerise -bf usernames.txt
  - python3 onerise <example> -all
  - python3 onerise -bd example.txt
  - python3 onerise example -all -sf some.txt
  - python3 onerise -bf name,name2
  - python3 onerise -bd name,name2
  - python3 onerise -bsn <user>
"""
            return help_text

    parser = argparse.ArgumentParser(
        description="Search for usernames on various websites and DuckDuckGo.",
        formatter_class=CustomHelpFormatter,  
        add_help=False  
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message and exit."
    )

    parser.add_argument("username", nargs="?", type=str, help="The username to search for.")
    parser.add_argument("-bf", "--brute-force", type=str, help="Enable brute-force username variations from a .txt file.")
    parser.add_argument("-bd", "--brute-force-duckduckgo", type=str, help="Brute-force usernames from a .txt file and search DuckDuckGo.")
    parser.add_argument("-bsn", "--brute-force-similar-names", type=str, help="Brute-force similar names (e.g., vbiskit -> biskit, biskit069).")
    parser.add_argument("-sf", "--save-file", type=str, help="Save the results to a file.")
    parser.add_argument("-all", "--search-all", action="store_true", help="Search additional sites like DuckDuckGo.")

    return parser


def generate_similar_names(username):
    variations = set()
    variations.add(username)  

    parts = []
    if " " in username:  
        parts = username.split(" ")
    else:  
        parts = [username]

    if len(parts) > 1:
        variations.add("".join(parts))  
        variations.add("".join(reversed(parts)))  
        variations.add("_".join(parts))  
        variations.add(".".join(parts))  
        variations.add("-".join(parts))  

    common_prefixes = ['x', 'xx', 'the', 'real', 'official', 'im', 'its', 'mr', 'ms', 'dr', 'pro']
    for prefix in common_prefixes:
        variations.add(f"{prefix}{username}")  
        variations.add(f"{prefix}_{username}")  
        variations.add(f"{prefix}{''.join(parts)}")  

    common_suffixes = ['123', '69', '007', '01', '2023', 'x', 'xx', 'lol', 'uwu', 'qt']
    for suffix in common_suffixes:
        variations.add(f"{username}{suffix}")  
        variations.add(f"{''.join(parts)}{suffix}")  
        variations.add(f"{username}_{suffix}")  

    for _ in range(5):  
        random_num = random.randint(1, 999)
        variations.add(f"{username}{random_num}")  
        variations.add(f"{''.join(parts)}{random_num}")  

    reversed_username = username[::-1]  
    variations.add(reversed_username)  

    variations.add(username.lower())
    variations.add(username.upper())

    mixed_case = "".join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(username)])
    variations.add(mixed_case)  

    return list(variations)

def process_bf_argument(bf_arg):
    if os.path.isfile(bf_arg):  
        with open(bf_arg, "r") as f:
            usernames = [line.strip() for line in f if line.strip()]
    else:  
        usernames = bf_arg.split(",")

    return usernames
    
async def search_username(username, save_file=None, search_all=False, print_summary=True):
    start_time = time.time()
    found = []
    unique_sites = set()
    duckduckgo_results = [] 

    if save_file:
        output_capture = io.StringIO()
        sys.stdout = output_capture 

    async with aiohttp.ClientSession() as session:
        tasks = [check_username_with_retries(session, site, username) for site in metadata["sites"]]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result and result[0] not in unique_sites:
                unique_sites.add(result[0])
                found.append(result)

        if search_all:
            duckduckgo_results = scrape_duckduckgo_links(username)  
            print(f"\n\033[38;2;255;255;255m[\033[93mDuckduckgo\033[38;2;255;255;255m]", flush=True)  
            for link in duckduckgo_results:
                highlighted_link = highlight_url(link)
                print(f"\033[97m{highlighted_link}\033[0m", flush=True)

    elapsed_time = time.time() - start_time

    if not found and not duckduckgo_results:
        print(f"\033[38;2;255;255;255m[\033[38;2;255;0;0mERR\033[38;2;255;255;255m] Name doesn't exist \033[38;5;11m{username}\n")
    elif print_summary:
        print(f"\n\033[38;2;255;255;255m[\033[93mINF\033[38;2;255;255;255m] [\033[93mSites\033[38;2;255;255;255m] \033[38;2;255;255;255m: {len(found)}")  
        print(f"[{Fore.LIGHTWHITE_EX}*\033[38;2;255;255;255m] [\033[93mTime Taken\033[38;2;255;255;255m] \033[38;2;255;255;255m{elapsed_time:.2f} seconds\n")

    if save_file:
        sys.stdout = sys.__stdout__  
        captured_output = output_capture.getvalue()  

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}+{Fore.LIGHTGREEN_EX}] Results saved to {save_file}")
        except Exception as e:
            print(f"\033[38;2;255;255;255m[\033[38;5;196mERR\033[38;2;255;255;255m] Failed to save results to {save_file}: {str(e)}")
    
    return len(found), duckduckgo_results, elapsed_time

def scrape_duckduckgo_links(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": get_random_user_agent()}

    try:  
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a_tag in soup.find_all("a", class_="result__a", href=True):
            href = a_tag.get("href")
            if "duckduckgo.com/l/?" in href:
                parsed_url = urlparse(href)
                real_url = parse_qs(parsed_url.query).get("uddg", [None])[0]
                if real_url:
                    links.add(real_url)
            elif "duckduckgo.com" not in href:
                links.add(href)

        return list(links)

    except requests.exceptions.RequestException as e:
        print(f"\033[91mError with DuckDuckGo request: {e}\033[0m")
        return []

def highlight_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    highlighted_url = f"{Fore.LIGHTBLACK_EX}{parsed_url.scheme}://\033[38;5;10m{domain}{Fore.LIGHTBLACK_EX}{path}"

    return highlighted_url

def read_usernames_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
        return usernames
    except Exception as e:
        print(f"\033[91mError reading file {file_path}: {e}\033[0m")
        return []

def process_brute_force_duckduckgo(usernames_input, save_file=None, max_retries=1):
    if os.path.isfile(usernames_input):
        usernames = read_usernames_from_file(usernames_input)
    else:
        usernames = usernames_input.split(',')

    total_links_found = 0
    username_results = {}
    start_time = time.time()

    if save_file:
        output_capture = io.StringIO()
        sys.stdout = output_capture  

    for username in usernames:
        retry_count = 0
        success = False
        username_links = 0

        print(f"\n\033[38;2;255;255;255m[\033[93mINF\033[38;2;255;255;255m] Checking {username} with DuckDuckGo", flush=True)

        while retry_count < max_retries and not success:
            duckduckgo_results = scrape_duckduckgo_links(username)

            if not duckduckgo_results:
                if retry_count == 0:
                    print(f"[\033[38;2;255;255;255m\033[38;5;196mERR\033[38;2;255;255;255m]\033[38;5;196m No results found for \033[38;2;255;255;255m{username}", flush=True)
                    print(f"\033[38;2;255;255;255m[{blue2('INFO')}\033[38;2;255;255;255m] Retrying {username}...", flush=True)

                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.91)
                else:
                    break
            else:
                for link in duckduckgo_results:
                    highlighted_link = highlight_url(link)
                    print(highlighted_link, flush=True)
                    username_links += 1
                    total_links_found += 1
                success = True

        username_results[username] = username_links
        time.sleep(6.5)

    elapsed_time = time.time() - start_time

    print(f"\n\033[38;2;255;255;255m[\033[93mSUMMARY\033[38;2;255;255;255m]")
    for username, link_count in username_results.items():
        print(f"\033[38;2;255;255;255m{username}: {link_count} links")
    
    if save_file:
        sys.stdout = sys.__stdout__  
        captured_output = output_capture.getvalue()  

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}+{Fore.LIGHTGREEN_EX}] Results saved to {save_file}")
        except Exception as e:
            print(f"[{blue2('ERR')}] Failed to save results to {save_file}: {str(e)}")

def main():
    print_banner()  
    parser = setup_argparse()
    args = parser.parse_args()

    if hasattr(args, 'help') and args.help:
        print(parser.format_help())  
        sys.exit(0)

    if not any([args.username, args.brute_force, args.brute_force_duckduckgo, args.brute_force_similar_names]):
        sys.exit(0)

    if args.username:
        print(f"\n\033[38;2;255;255;255m[\033[93mINF\033[38;2;255;255;255m] Emulating websites for {args.username}")
        asyncio.run(search_username(args.username, save_file=args.save_file, search_all=args.search_all))

    elif args.brute_force:
        usernames = process_bf_argument(args.brute_force)
        username_results = {}
        total_sites = 0
        overall_start_time = time.time()
        for username in usernames:
            print(f"\n\033[38;2;255;255;255m[\033[93mINF\033[38;2;255;255;255m] Emulating websites for {username}")
            sites_found, duckduckgo_links, _ = asyncio.run(search_username(username, save_file=args.save_file, search_all=args.search_all, print_summary=False))
            username_results[username] = sites_found
            total_sites += sites_found
        
        overall_elapsed_time = time.time() - overall_start_time
        
        print(f"\n\033[38;2;255;255;255m[\033[93mSUMMARY\033[38;2;255;255;255m]")
        for username, count in username_results.items():
            print(f"\033[38;2;255;255;255m{username} : {count} sites")

    elif args.brute_force_duckduckgo:
        process_brute_force_duckduckgo(args.brute_force_duckduckgo, save_file=args.save_file)

    elif args.brute_force_similar_names:
        similar_names = generate_similar_names(args.brute_force_similar_names)
        username_results = {}
        total_sites = 0
        overall_start_time = time.time()
        for name in similar_names:
            print(f"\n\033[38;2;255;255;255m[\033[93mINF\033[38;2;255;255;255m] Emulating websites for {name}")
            sites_found, duckduckgo_links, _ = asyncio.run(search_username(name, save_file=args.save_file, search_all=args.search_all, print_summary=False))
            username_results[name] = sites_found
            total_sites += sites_found
        
        overall_elapsed_time = time.time() - overall_start_time
        for name, count in username_results.items():
            if count > 0:  
                print(f"")

if __name__ == "__main__":
    main()
