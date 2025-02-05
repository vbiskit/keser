mport requests
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
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
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
def check_username_on_website(url, username):
    try:
        response = requests.get(url.format(username))  
        if response.status_code == 429:
            print(f"\033[38;2;255;255;255m[\033[38;2;255;0;255m~\033[38;2;255;255;255m]\033[38;2;255;0;255m To Many Request (429) {url.format(username)} \033[38;2;255;255;255mCan't Check If Link Is Found \033[0m")
            return None
        elif response.status_code == 404:
            print(f"\033[38;2;255;255;255m[\033[38;2;255;0;0m-\033[38;2;255;255;255m]\033[\033[38;2;255;0;0m Not Found\033[38;2;255;255;255m {url.format(username)}\033[0m")
            return None
        elif response.status_code == 410:
            print(f"\033[38;2;255;255;255m[\033[38;2;255;255;0m!\033[38;2;255;255;255m]\033[38;2;255;255;0m Name Doesn't Exist\033[38;2;255;255;255m {url.format(username)}\033[0m")  
            return None
        elif response.status_code == 200:
            if username.lower() in response.text.lower():
                print(f"\033[38;2;255;255;255m[\033[38;2;0;255;0m+\033[38;2;255;255;255m]\033[38;2;0;255;0m Found\033[38;2;255;255;255m {url.format(username)}\033[0m")
                return url.format(username)  
    except requests.exceptions.RequestException as e:
        print(f"Error checking {url.format(username)}: {e}")
        return None
    return None  

websites = {
"GitHub": "https://github.com/{}",
    "Twitter": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Duolingo": "https://www.duolingo.com/profile/{}",
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
    "kick":"https://www.kick.com/{}",
    "steam":"https://steamcommunity.com/id/{}/",
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
    "8tracks": "https://8tracks.com/{}",
    "9GAG": "https://www.9gag.com/u/{}",
    "Academia.edu": "https://independent.academia.edu/{}",
    "Air Pilot Life": "https://airlinepilot.life/u/{}",
    "AllMyLinks": "https://allmylinks.com/{}",
    "Anilist": "https://anilist.co/user/{}",
    "Apple Developer": "https://developer.apple.com/forums/profile/{}",
    "Apple Discussions": "https://discussions.apple.com/profile/{}",
    "Archive of Our Own": "https://archiveofourown.org/users/{}",
    "Atcoder": "https://atcoder.jp/users/{}",
    "Behance": "https://www.behance.net/{}",
    "BiggerPockets": "https://www.biggerpockets.com/users/{}",
    "Blogger": "https://tyrell.blogspot.com",
    "BoardGameGeek": "https://boardgamegeek.com/user/{}",
    "Bookcrossing": "https://www.bookcrossing.com/mybookshelf/{}",
    "BuyMeACoffee": "https://buymeacoff.ee/{}",
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
    "Disqus": "https://disqus.com/{}",
    "Docker Hub": "https://hub.docker.com/u/{}/",
    "EyeEm": "https://www.eyeem.com/u/{}",
    "Fanpop": "https://www.fanpop.com/fans/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Flightradar24": "https://my.flightradar24.com/{}",
    "Freelancer": "https://www.freelancer.com/u/{}",
    "GaiaOnline": "https://www.gaiaonline.com/profiles/{}",
    "Gamespot": "https://www.gamespot.com/profile/{}",
    "Genius (Artists)": "https://genius.com/artists/{}",
    "Genius (Users)": "https://genius.com/{}",
    "Fortnite": "https://fortnitetracker.com/profile/all/{}",
    "dribble" : "https://dribbble.com/{}",
    "wordpress users ": "https://profiles.wordpress.org/{}",
    "linktree": "https://linktr.ee/{}",
    "osu":"https://osu.ppy.sh/users/{}",
    "medium":"https://medium.com/@{}",
    "Fadom":"https://community.fandom.com/wiki/User:{}",
    "cashapp":"https://cash.app/${}",
    "slideshare":"https://www.slideshare.net/{}",
    "airpilot": "https://airlinepilot.life/u/{}",
    "airbit": "https://airbit.com/{}",
    "airliners": "https://www.airliners.net/user/{}/profile/photos",
    "anilist": "https://anilist.co/user/{}/",
    "asciinema": "https://asciinema.org/~{}",
    "atcoder": "https://atcoder.jp/users/{}",
    "bandcamp": "https://www.bandcamp.com/{}",
    "behance": "https://www.behance.net/{}",
    "bezuzyteczna": "https://bezuzyteczna.pl/uzytkownicy/{}",
    "bitbucket": "https://bitbucket.org/{}/",
    "boardgamegeek": "https://boardgamegeek.com/user/{}",
    "bookcrossing": "https://www.bookcrossing.com/mybookshelf/{}/",
    "bravecommunity": "https://community.brave.com/u/{}/",
    "carbonmade": "https://{}.carbonmade.com",
    "chaos": "https://chaos.social/@{}",
    "clapper": "https://clapperapp.com/{}",
    "clozemaster": "https://www.clozemaster.com/players/{}",
    "codeforces": "https://codeforces.com/profile/{}",
    "codersrank": "https://profile.codersrank.io/user/{}/",
    "coderwall": "https://coderwall.com/{}",
    "crevado": "https://{}.crevado.com",
    "crowdin": "https://crowdin.com/profile/{}",
    "cults3d": "https://cults3d.com/en/users/{}/creations",
    "cyberdefenders": "https://cyberdefenders.org/p/{}",
    "devcommunity": "https://dev.to/{}",
    "dmoj": "https://dmoj.ca/user/{}",
    "dealabs": "https://www.dealabs.com/profile/{}",
    "discuss_elastic": "https://discuss.elastic.co/u/{}",
    "disqus": "https://disqus.com/{}",
    "eintracht": "https://community.eintracht.de/fans/{}",
    "empretienda": "https://{}.empretienda.com.ar",
    "exophase": "https://www.exophase.com/user/{}",
    "fanpop": "https://www.fanpop.com/fans/{}",
    "fosstodon": "https://fosstodon.org/@{}",
    "gnomevcs": "https://gitlab.gnome.org/{}",
    "gaiaonline": "https://www.gaiaonline.com/profiles/{}",
    "gamespot": "https://www.gamespot.com/profile/{}/",
    "geeksforgeeks": "https://auth.geeksforgeeks.org/user/{}",
    "giantbomb": "https://www.giantbomb.com/profile/{}/",
    "grailed": "https://www.grailed.com/{}",
    "hackthebox": "https://forum.hackthebox.com/u/{}",
    "hackernews": "https://news.ycombinator.com/user?id={}",
    "hackerone": "https://hackerone.com/{}",
    "hashnode": "https://hashnode.com/@{}",
    "holopin": "https://holopin.io/@{}",
    "ifttt": "https://www.ifttt.com/p/{}",
    "imgur": "https://imgur.com/user/{}",
    "issuu": "https://issuu.com/{}",
    "itch": "https://{}.itch.io/",
    "itemfix": "https://www.itemfix.com/c/{}",
    "joplin": "https://discourse.joplinapp.org/u/{}/",
    "kaskus": "https://www.kaskus.co.id/@{}",
    "keybase": "https://keybase.io/{}",
    "kongregate": "https://www.kongregate.com/accounts/{}",
    "launchpad": "https://launchpad.net/~{}",
    "lesswrong": "https://www.lesswrong.com/users/@{}",
    "lichess": "https://lichess.org/@/{}/",
    "listed": "https://listed.to/@{}",
    "livejournal": "https://{}.livejournal.com",
    "mmorpg": "https://forums.mmorpg.com/profile/{}",
    "memrise": "https://www.memrise.com/user/{}/",
    "mixcloud": "https://www.mixcloud.com/{}/",
    "monkeytype": "https://monkeytype.com/profile/{}",
    "myanimelist": "https://myanimelist.net/profile/{}",
    "mydramalist": "https://www.mydramalist.com/profile/{}",
    "myspace": "https://myspace.com/{}",
    "nicommunity": "https://community.native-instruments.com/profile/{}",
    "nationstates": "https://nationstates.net/nation={}",
    "naver": "https://blog.naver.com/{}",
    "nintendolife": "https://www.nintendolife.com/users/{}",
    "nitrotype": "https://www.nitrotype.com/racer/{}",
    "openstreetmap": "https://www.openstreetmap.org/user/{}",
    "packagist": "https://packagist.org/packages/{}/",
}
def search_username(username, threads=500):
    print(f"\033[38;2;0;255;0m[\033[38;2;255;255;0m*\033[38;2;0;255;0m]\033[38;2;0;255;0m Checking username {username} on: \033[0m\n")

    found = set()  

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for website, url in websites.items():
            futures.append(executor.submit(check_username_on_website, url, username))
        
        for future in as_completed(futures):
            result = future.result()
            if result:  
                found.add(result)

    duckduckgo_results = scrape_duckduckgo_links(username)

    found_count = len(found)  
    duckduckgo_count = len(duckduckgo_results)
    total_found_links = found_count + duckduckgo_count

    if found or duckduckgo_results:
        if found:
            print(f"\033[38;2;0;255;0m[\033[38;2;255;255;0m*\033[38;2;0;255;0m]\033[38;2;0;255;0m Found Username Links:\033[0m")
            for result in found:
                print(f"\033[38;2;255;255;255mLinks: {result}\033[0m")  

        if duckduckgo_results:
            print(f"\n\033[38;2;0;255;0m[\033[38;2;255;255;0m*\033[38;2;0;255;0m]\033[38;2;0;255;0m Duckduckgo Found {duckduckgo_count} Links\033[0m")
            for duckduckgo_result in duckduckgo_results:
                print(f"\033[38;2;255;255;255m{duckduckgo_result}\033[0m")

        print(f"\n\033[38;2;0;255;0m[\033[38;2;255;255;0m*\033[38;2;0;255;0m]\033[38;2;255;255;255m Website Found: {found_count}\033[0m")

    else:
        print(f"\n\033[38;2;255;69;0mNo exact matches for '{username}' were found on the listed websites or DuckDuckGo.\033[0m")

if __name__ == "__main__":
    sys.stdout.write("\033c")
    print("""\033[38;2;0;0;255m                                
 ███▄    █ ▓█████ ▒██   ██▒ █    ██   ██████ 
 ██ ▀█   █ ▓█   ▀ ▒▒ █ █ ▒░ ██  ▓██▒▒██    ▒ 
▓██  ▀█ ██▒▒███   ░░  █   ░▓██  ▒██░░ ▓██▄   
▓██▒  ▐▌██▒▒▓█  ▄  ░ █ █ ▒ ▓▓█  ░██░  ▒   ██▒
▒██░   ▓██░░▒████▒▒██▒ ▒██▒▒▒█████▓ ▒██████▒▒
░ ▒░   ▒ ▒ ░░ ▒░ ░▒▒ ░ ░▓ ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░ ░ ░  ░░░   ░▒ ░░░▒░ ░ ░ ░ ░▒  ░ ░
   ░   ░ ░    ░    ░    ░   ░░░ ░ ░ ░  ░  ░  
         ░    ░  ░ ░    ░     ░           ░                                                                                                                                                                        
\033[0m""")  
    sys.stdout.flush()
    for _ in range(1):
        time.sleep(0.6)
        sys.stdout.write("\033[38;2;0;255;255m@biskit")
        sys.stdout.flush()
    print("\n")
    username = input("\033[38;2;0;0;255m[\033[38;2;255;255;255m*\033[38;2;0;0;255m]\033[\033[38;2;255;255;255m Enter Person's Name \033[0m")  
    threads = int(input("\033[38;2;0;0;255m[\033[38;2;255;255;255m*\033[38;2;0;0;255m]\033[\033[38;2;255;255;255m Enter Number of Threads (1-500) \033[0m"))
    search_username(username, threads)
