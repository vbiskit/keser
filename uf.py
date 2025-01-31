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
    print("""\033[38;2;0;255;255m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣄⣠⣀⡀⣀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⢠⣠⣼⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⢠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣟⣾⣿⣽⣿⣿⣅⠈⠉⠻⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⢀⡶⠒⢉⡀⢠⣤⣶⣶⣿⣷⣆⣀⡀⠀⢲⣖⠒⠀⠀⠀⠀⠀⠀⠀
⢀⣤⣾⣶⣦⣤⣤⣶⣿⣿⣿⣿⣿⣿⣽⡿⠻⣷⣀⠀⢻⣿⣿⣿⡿⠟⠀⠀⠀⠀⠀⠀⣤⣶⣶⣤⣀⣀⣬⣷⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣦⣼⣀⠀
⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠓⣿⣿⠟⠁⠘⣿⡟⠁⠀⠘⠛⠁⠀⠀⢠⣾⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⠙⠁
⠀⠸⠟⠋⠀⠈⠙⣿⣿⣿⣿⣿⣿⣷⣦⡄⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣼⣆⢘⣿⣯⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⠉⢱⡿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⠦⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡗⠀⠈⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣉⣿⡿⢿⢷⣾⣾⣿⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⠿⠿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣾⣿⣿⣷⣦⣶⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣤⡖⠛⠶⠤⡀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠙⣿⣿⠿⢻⣿⣿⡿⠋⢩⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠧⣤⣦⣤⣄⡀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠘⣧⠀⠈⣹⡻⠇⢀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣤⣀⡀⠀⠀⠀⠀⠀⠀⠈⢽⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⣴⣿⣷⢲⣦⣤⡀⢀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣷⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠂⠛⣆⣤⡜⣟⠋⠙⠂⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠉⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣾⣿⣿⣿⣿⣆⠀⠰⠄⠀⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⠿⠿⣿⣿⣿⠇⠀⠀⢀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡇⠀⠀⢀⣼⠗⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠃⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
\033[0m""")  
    sys.stdout.flush()
    for _ in range(1):
        time.sleep(0.6)
        sys.stdout.write(Fore.LIGHTWHITE_EX "@biskit V 0.1")
        sys.stdout.flush()
    print("\n")

def check_username_on_website(url, username):
    try:
        response = requests.get(url.format(username))  
        if response.status_code == 429:
            print(f"\033[38;2;255;165;0m[+] Error Status Code 429 🟠  {url.format(username)} \033[38;2;0;255;255m[+] Can't Check If Link Is Found \033[0m")
        elif response.status_code == 404:
            print(f"\033[38;2;255;0;0m[+] Not Found {url.format(username)}\033[0m")
        elif response.status_code == 200:
            if username.lower() in response.text.lower():
                print(f"\033[38;2;0;255;0m[+] Found {url.format(username)}\033[0m")
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
    "Twitch": "https://www.twitch.com/{}",
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
    "minecraft":"https://namemc.com/search?q={} ",
    "airbit":"https://airbit.com/{}",
    "freesound":"https://freesound.org/people/{}",
    "7Cups": "https://www.7cups.com/@{}",
    "8tracks": "https://8tracks.com/{}",
    "9GAG": "https://www.9gag.com/u/{}",
    "About.me": "https://about.me/{}",
    "Academia.edu": "https://independent.academia.edu/{}",
    "Air Pilot Life": "https://airlinepilot.life/u/{}",
    "Airbit": "https://airbit.com/{}",
    "AllMyLinks": "https://allmylinks.com/{}",
    "Anilist": "https://anilist.co/user/{}",
    "Apple Developer": "https://developer.apple.com/forums/profile/{}",
    "Apple Discussions": "https://discussions.apple.com/profile/{}",
    "Archive of Our Own": "https://archiveofourown.org/users/{}",
    "Atcoder": "https://atcoder.jp/users/{}",
    "Audiojungle": "https://audiojungle.net/user/{}",
    "Bandcamp": "https://www.bandcamp.com/{}",
    "Behance": "https://www.behance.net/{}",
    "BiggerPockets": "https://www.biggerpockets.com/users/{}",
    "Blogger": "https://tyrell.blogspot.com",
    "BoardGameGeek": "https://boardgamegeek.com/user/{}",
    "Bookcrossing": "https://www.bookcrossing.com/mybookshelf/{}",
    "BuyMeACoffee": "https://buymeacoff.ee/{}",
    "BuzzFeed": "https://buzzfeed.com/{}",
    "CGTrader": "https://www.cgtrader.com/{}",
    "Carbonmade": "https://{}.carbonmade.com",
    "Championat": "https://www.championat.com/user/{}",
    "Clapper": "https://clapperapp.com/{}",
    "Clubhouse": "https://www.clubhouse.com/@{}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "Codeforces": "https://codeforces.com/profile/{}",
    "Codewars": "https://www.codewars.com/users/{}",
    "ColourLovers": "https://www.colourlovers.com/lover/{}",
    "Crowdin": "https://crowdin.com/profile/{}",
    "Cults3D": "https://cults3d.com/en/users/{}/creations",
    "DMOJ": "https://dmoj.ca/user/tyrell",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "Dealabs": "https://www.dealabs.com/profile/{}",
    "DeviantART": "https://{}.deviantart.com",
    "Disqus": "https://disqus.com/{}",
    "Docker Hub": "https://hub.docker.com/u/{}/",
    "Duolingo": "https://www.duolingo.com/profile/{}",
    "EyeEm": "https://www.eyeem.com/u/{}",
    "Fanpop": "https://www.fanpop.com/fans/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Flightradar24": "https://my.flightradar24.com/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "Freelancer": "https://www.freelancer.com/u/{}",
    "Freesound": "https://freesound.org/people/{}",
    "GaiaOnline": "https://www.gaiaonline.com/profiles/{}",
    "Gamespot": "https://www.gamespot.com/profile/{}",
    "Genius (Artists)": "https://genius.com/artists/{}",
    "Genius (Users)": "https://genius.com/{}",
}

def search_username(username, threads=10):
    
    print(f"\033[38;2;0;255;0m[+] Searching {username} \033[0m\n")

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
    username = input("\033[38;2;0;255;255m[+] Enter Persons Name \033[0m")  
    threads = int(input("\033[38;2;0;255;255m[+] Enter Number of Threads (10-100) \033[0m"))
    search_username(username, threads)
