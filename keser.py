#!/usr/bin/env python3
# Coded by vbiskit

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
import socket
from aiohttp import TCPConnector
from stats.stats import stats
import signal

def rgb(r, g, b, text):
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

def pink(text):
    colors = [
        (255, 20, 147),
        (173, 216, 230),
    ]

    colors_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(colors) - 1))
        r, g, b = colors[color_index]
        colors_text += rgb(r, g, b, char)

    return colors_text

def purple(text):
    gradient_colors = [
        (128, 0, 128),
        (160, 0, 110),
        (190, 0, 90),
        (220, 0, 60),
        (255, 0, 0),
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def yellow(text):
    gradient_output = ""
    start_color = (255, 255, 0)
    end_color = (0, 255, 0)

    for i, char in enumerate(text):
        ratio = i / len(text)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        gradient_output += f"\033[38;2;{r};{g};{b}m{char}"

    return gradient_output + "\033[0m"

def fetch_metadata():
    url = "https://raw.githubusercontent.com/vbiskit/keser/refs/heads/main/search.json"
    return requests.get(url).json()

metadata = fetch_metadata()

user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
    "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
    "Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)"
]

def get_random_user_agent():
    return random.choice(user_agents)

async def check_username_on_website(session, site, username, timeout=26.8):
    url = site["uri_check"].replace("{account}", username)
    headers = {"User-Agent": get_random_user_agent()}

    try:
        async with session.get(url, headers=headers, timeout=timeout) as response:
            raw_bytes = await response.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("latin-1")

            if response.status == site["e_code"] and site["e_string"] in text:
                print(f"\033[38;2;255;255;255m[\033[38;2;0;191;255m{site['name']}\033[38;2;255;255;255m] \033[38;2;255;255;255m[\033[38;2;0;255;0m{site['cat']}\033[38;2;255;255;255m] \033[90m{url} ")
                return (site["name"], url, site["cat"])

            if "m_code" in site and "m_string" in site:
                if response.status == site["m_code"] and site["m_string"] in text:
                    return None

            return None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None

async def check_username_with_retries(session, site, username, timeout=26.8, max_retries=1):
    for attempt in range(max_retries):
        result = await check_username_on_website(session, site, username, timeout)
        if result is not None:
            return result
        await asyncio.sleep(0.03)
    return None

async def check_top_site(session, site, username, timeout=13.6):
    url = site["uri_check"].replace("{account}", username)
    headers = {"User-Agent": get_random_user_agent()}

    try:
        async with session.get(url, headers=headers, timeout=timeout) as response:
            raw_bytes = await response.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("latin-1")

            if response.status == site["e_code"] and site["e_string"] in text:
                print(f"\033[38;2;255;255;255m[\033[38;2;0;191;255m{site['name']}\033[38;2;255;255;255m] \033[38;2;255;255;255m[\033[38;2;0;255;0m{site['cat']}\033[38;2;255;255;255m] \033[90m{url}")
                return (site["name"], url, site["cat"])

            if "m_code" in site and "m_string" in site:
                if response.status == site["m_code"] and site["m_string"] in text:
                    return None

            return None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None

async def check_top_site_with_retries(session, site, username, timeout=13.6, max_retries=3):
    for attempt in range(max_retries):
        result = await check_top_site(session, site, username, timeout)
        if result is not None:
            return result
        await asyncio.sleep(0.03)
    return None

def print_banner(show_newline=True):
    keser = r"""
 .-. .-..----. .----..----..----.
 | |/ / | {_  { {__  | {_  | {}  }
 | |\ \ | {__ .-._} }| {__ | .-. \
 `-' `-'`----'`----' `----'`-' `-'"""
    print(pink(keser))
    print(purple(' By BisKit | Version 1.0.3'))
    print(purple(' ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'))
    print(pink(' :  keser --help                      :'))
    print(pink(' :  https://github.com/vbiskit/keser  :'))
    print(purple(' ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~' f'{"" if not show_newline else "\n"}'))

def setup_argparse():
    class CustomHelpFormatter(argparse.HelpFormatter):
        def format_help(self):
            help_text = """\033[38;2;255;255;255m
Arguments:
  -sf  Save the output to a file
  -all Search With Duckduckgo And Userlinks
  -top this shows the top sites for social media gaming tiktok instagram fortnite etc. 
  --timeout is for very fast searches, use <13.6> Recommend (For Fast Internets Only) don't use timeout if you have slow wifi the default is enough to catch tiktok all the sites.
Usage:
   keser <example> -sf example.txt
   keser <example> for just links
   keser <example> -all
   keser example -all -sf some.txt
   keser <example> -top
   keser <example> --timeout 5"""

            return help_text

    parser = argparse.ArgumentParser(
        formatter_class=CustomHelpFormatter,
        add_help=False
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true"
    )

    parser.add_argument("username", nargs="?", type=str)
    parser.add_argument("-sf", "--save-file", type=str)
    parser.add_argument("-all", "--search-all", action="store_true")
    parser.add_argument("-top", "--top-sites", action="store_true")
    parser.add_argument("--timeout", type=float, default=26.8)

    return parser

def process_bf_argument(bf_arg):
    if os.path.isfile(bf_arg):
        try:
            with open(bf_arg, "r") as f:
                usernames = [line.strip() for line in f if line.strip()]
        except PermissionError:
            print(f"\033[91mError: Permission denied when trying to read the file {bf_arg}.\033[0m")
            return []
        except FileNotFoundError:
            print(f"\033[91mError: The file {bf_arg} does not exist.\033[0m")
            return []
        except Exception as e:
            print(f"\033[91mError reading the file {bf_arg}: {e}\033[0m")
            return []
    else:
        usernames = bf_arg.split(",")

    return usernames

TOP_SOCIAL_SITES = [
    "instagram", "twitter", "tiktok", "snapchat", "hudsonrock",
    "linkedin", "pinterest", "reddit", "tumblr", "youtube user", "Imginn", "kik",
    "twitch", "discord", "telegram", "whatsapp", "vimeo", "gta", "github", "Instagram_archives",
    "flickr", "deviantart", "vsco", "hoo.be", "onlysearch", "paypal", "linktree", "streamlabs"
]

TOP_GAMING_SITES = [
    "steam", "Apex Legends",
    "chess.com", "Minecraft List", "Roblox", "fortnite tracker", "MCName"
]

async def search_username(username, save_file=None, search_all=False, print_summary=True, top_sites=False, timeout=26.8):
    start_time = time.time()
    found = []
    unique_sites = set()
    duckduckgo_results = []

    if save_file:
        output_capture = io.StringIO()
        sys.stdout = output_capture

    connector = TCPConnector(
        ssl=False,
        ttl_dns_cache=300,
        use_dns_cache=True,
        limit=100,
        force_close=True,
        family=socket.AF_INET,
        resolver=aiohttp.AsyncResolver(nameservers=['1.1.1.1', '1.0.0.1'])
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        sites_to_check = metadata["sites"]
        if top_sites:
            sites_to_check = [
                site for site in metadata["sites"]
                if site["name"].lower() in TOP_SOCIAL_SITES or site["name"].lower() in TOP_GAMING_SITES
            ]
        with stats(len(sites_to_check)) as stats_checking:
            if top_sites:
                tasks = [check_top_site_with_retries(session, site, username, timeout) for site in sites_to_check]
            else:
                tasks = [check_username_with_retries(session, site, username, timeout) for site in sites_to_check]

            for task in asyncio.as_completed(tasks):
                result = await task
                if result and result[0] not in unique_sites:
                    unique_sites.add(result[0])
                    found.append(result)
                    stats_checking.update(1, 1)
                else:
                    stats_checking.update(1, 0)

        if search_all:
            print(f"\n\033[38;2;255;255;255m[\033[38;2;0;255;0mDuckduckgo\033[38;2;255;255;255m]", flush=True)
            duckduckgo_results = scrape_duckduckgo_links(username)
            for link in duckduckgo_results:
                highlighted_link = highlight_url(link)
                print(f"\033[97m{highlighted_link}\033[0m", flush=True)

    elapsed_time = time.time() - start_time

    if not found and not duckduckgo_results:
        print(f"\033[38;2;255;255;255m[\033[38;2;255;0;0mERR\033[38;2;255;255;255m] Name doesn't exist \033[38;5;11m{username}")
    elif print_summary:
        print(f"\n\033[93mSites\033[38;2;255;255;255m: {len(found)} from '{username}' - Search time: {elapsed_time:.2f} seconds")

    if save_file:
        sys.stdout = sys.__stdout__
        captured_output = output_capture.getvalue()

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTBLUE_EX}[{Fore.LIGHTGREEN_EX}*{Fore.LIGHTBLUE_EX}] Results saved to {save_file}")
        except Exception as e:
            print(f"\033[38;2;255;255;255m[\033[38;5;196mERR\033[38;2;255;255;255m] Failed to save results to {save_file}: {str(e)}")

    return len(found), duckduckgo_results, elapsed_time

def highlight_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    highlighted_url = f"\033[90m{parsed_url.scheme}://\033[38;5;39m{domain}\033[90m{path}"
    return highlighted_url

def scrape_duckduckgo_links(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": get_random_user_agent()}

    try:
        response = requests.get(url, headers=headers, timeout=10)
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

def read_usernames_from_file(file_path):
    if not os.path.isfile(file_path):
        print(f"\033[91mError: The file {file_path} does not exist.\033[0m")
        return []

    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
        return usernames
    except PermissionError:
        print(f"\033[91mError: Permission denied when trying to read the file {file_path}.\033[0m")
        return []
    except Exception as e:
        print(f"\033[91mError reading the file {file_path}: {e}\033[0m")
        return []

def process_brute_force_duckduckgo(usernames_input, save_file=None, max_retries=2):
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

    with stats(len(usernames)) as stats_checking:
        for username in usernames:
            retry_count = 0
            success = False
            username_links = 0
            while retry_count < max_retries and not success:
                duckduckgo_results = scrape_duckduckgo_links(username)

                if not duckduckgo_results:
                    if retry_count == 0:
                        print(f"[\033[38;2;255;255;255m\033[38;5;196mERR\033[38;2;255;255;255m]\033[38;5;196m No results found for \033[38;2;255;255;255m{username} Retrying failed user\n", flush=True)

                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.96)
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
            stats_checking.update(1, username_links)
            time.sleep(4.3)

    elapsed_time = time.time() - start_time
    print()
    for username, link_count in username_results.items():
     print(f"\033[93mSites\033[38;2;255;255;255m: {link_count} from '{username}' - Search time: {elapsed_time:.2f} seconds")

    if save_file:
        sys.stdout = sys.__stdout__
        captured_output = output_capture.getvalue()

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTBLUE_EX}[{Fore.LIGHTGREEN_EX}*{Fore.LIGHTBLUE_EX}] Results saved to {save_file}")
        except Exception as e:
           print(f"[\033[38;2;255;255;255m\033[38;5;196mERR\033[38;2;255;255;255m] Failed to save results to {save_file}: {str(e)}")

def signal_handler(signum, frame):
    print("\n\033[91m[!] \033[0mkeser is interrupted.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = setup_argparse()
    args = parser.parse_args()

    if hasattr(args, 'help') and args.help:
        print_banner(show_newline=False)
        print(parser.format_help())
        sys.exit(0)

    if not args.username:
        print_banner(show_newline=False)
        print(parser.format_help())
        sys.exit(0)

    print_banner(show_newline=True)
    if args.top_sites:
        asyncio.run(search_username(args.username, save_file=args.save_file, search_all=args.search_all, top_sites=args.top_sites, timeout=args.timeout))
    else:
        asyncio.run(search_username(args.username, save_file=args.save_file, search_all=args.search_all, top_sites=args.top_sites, timeout=args.timeout))

if __name__ == "__main__":
    main()
