import requests
from bs4 import BeautifulSoup
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import os
from colorama import Fore

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.70",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
]

def get_random_user_agent():
    return random.choice(user_agents)

def scrape_duckduckgo_links(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": get_random_user_agent()
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a_tag in soup.find_all("a", class_="result__a", href=True):
            href = a_tag.get("href")
            if href:
                links.append(href)

        return links

    except requests.exceptions.RequestException as e:
        print(f"Error with DuckDuckGo request: {e}")
        return []

def loading_screen():
    sys.stdout.write("\033c")  
    print("""\033[38;2;255;69;0m
                        _____           __         
  __  __________  _____/ __(_)___  ____/ /__  _____
 / / / / ___/ _ \/ ___/ /_/ / __ \/ __  / _ \/ ___/
/ /_/ (__  )  __/ /  / __/ / / / / /_/ /  __/ /    
\__,_/____/\___/_/  /_/ /_/_/ /_/\__,_/\___/_/ 
\033[0m""")  
    sys.stdout.flush()
    for _ in range(1):
        time.sleep(0.6)
        sys.stdout.write(Fore.LIGHTWHITE_EX+"@biskit V 0.1")
        sys.stdout.flush()
    print("\n")

def check_username_on_website(url, username):
    try:
        response = requests.get(url.format(username))  
        if response.status_code == 429:
            print(f"\033[38;2;255;165;0m429 Too many requests on Server 🟠 {url.format(username)} (Found Link ✅\033[0m")
        elif response.status_code == 404:
            print(f"\033[38;2;255;0;0m404 Not Found ❌ {url.format(username)}\033[0m")
        elif response.status_code == 200:
            if username.lower() in response.text.lower():
                print(f"\033[38;2;0;255;0mFound Link ✅ {url.format(username)}\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"Error checking {url.format(username)}: {e}")

websites = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Duolingo": "https://www.duolingo.com/{}",
    "Chess": "https://www.chess.com/member/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "AU LinkedIn": "https://au.linkedin.com/in/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Smule": "https://www.smule.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "21buttons": "https://www.21buttons.com/buttoner/{}",
    "public": "https://public.com/@{}",
    "gtainside": "https://www.gtainside.com/user/{}",
    "bodybuilder": "http://bodyspace.bodybuilding.com/{}",
    "aboutme": "https://about.me/{}",
    "35photo": "https://35photo.pro/@{}",
    "7dach": "https://7dach.ru/profile/{}",
    "anoup": "https://anonup.com/@{}",
    "bugcrowd": "https://bugcrowd.com/{}",
    "cytoid": "https://cytoid.io/profile/{}",
    "coroflot": "https://www.coroflot.com/{}",
    "adobeforms": "https://community.adobe.com/t5/forums/searchpage/tab/user?q={} ",
    "pinterest": "https://au.pinterest.com/{}",
    "patreon": "https://www.patreon.com/search?q={} ",
    "pastebin": "https://pastebin.com/u/{}",
    "periscope": "https://www.periscope.tv/{}",
    "linktree": "https://linktr.ee/{}",
    "mastodon": "https://mastodon.social/api/v2/search?q={}&type=accounts",
    "knowyourmeme": "https://knowyourmeme.com/users/{}",
    "archive": "https://archive.org/search?query={} ",
    "imgur": "https://imgur.com/user/{}/about",
    "huggingface": "https://huggingface.co/{}",
    "hudsonrock": "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={} ",
    "hackerrank": "https://www.hackerrank.com/profile/{}",
    "hackaday": "https://hackaday.io/{}",
    "XboxGamerTag": "https://www.xboxgamertag.com/search/{}",
    "younow": "https://www.younow.com/{}",
    "wordpress": "https://wordpress.org/support/users/{}",
    "vimeo": "https://vimeo.com/{}",
    "tiktok": "https://www.tiktok.com/@{}",
    "tinder": "https://tinder.com/@{}",
    "trello": "https://trello.com/u/{}/activity",
    "streamlabs": "https://streamlabs.com/{}",
    "roblox": "https://www.roblox.com/{}",
    "discorgs": "https://api.discogs.com/users/{}",
    "flipboard": "https://flipboard.com/@{}",
    "scratch": "https://scratch.mit.edu/users/{}",
    "audiojungle": "https://audiojungle.net/user/{}",
    "hoobe":"https://hoo.be/{}",
    "devinart": "https://www.deviantart.com/{}",
    "rblxtrade":"https://rblx.trade/p/{}",
    "kick":"https://kick.com/{}",
    "rumble":"https://rumble.com/user/{}",
    "steam":"https://steamcommunity.com/id/{}",
    "Shopify":"https://{}.myshopify.com",
    "steamgifts":"https://www.steamgifts.com/user/{}",
    "venmo":"https://account.venmo.com/u/{}",
    "tryhackme":"https://tryhackme.com/r/p/{}",
    "telegram":"https://t.me/{}",
    "allmylinks":"https://allmylinks.com/{}",
    "bandlab":"https://www.bandlab.com/{}",
    "clubhouse":"https://www.clubhouse.com/@{}",
    "buzzfeed":"https://www.buzzfeed.com/{}",
    "minecraft":"https://namemc.com/search?q={}",
}

def search_username(username, threads=10):
    print(f"\033[38;2;255;69;0mSearching Username '{username}' with {threads} threads...\033[0m\n")

    found = set()  

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for website, url in websites.items():
            futures.append(executor.submit(check_username_on_website, url, username))
        
        for future in as_completed(futures):
            future.result()

    duckduckgo_results = scrape_duckduckgo_links(username)

    if found or duckduckgo_results:
        print("\033[38;2;255;69;0mFound the username on the following websites:\033[0m")
        for result in found:
            print(f"\033[38;2;0;255;0m{result}\033[0m")  

        if duckduckgo_results:
            print("\n\033[38;2;0;255;0mFound the username in DuckDuckGo search results:\033[0m")
            for duckduckgo_result in duckduckgo_results:
                print(f"\033[38;2;0;255;0m{duckduckgo_result}\033[0m") 
    else:
        print(f"\n\033[38;2;255;69;0mNo exact matches for '{username}' were found on the listed websites or DuckDuckGo.\033[0m")

if __name__ == "__main__":
    loading_screen()
    username = input("\033[38;2;255;69;0mEnter Username \033[0m")  
    threads = int(input("\033[38;2;255;69;0mEnter number of threads (10-100) \033[0m"))
    search_username(username, threads)
