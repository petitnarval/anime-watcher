import re

from bs4 import BeautifulSoup
from pyjsparser import parse

import colors
import user_interface
import web_requests
import config
import time


def optimised_link(url):
    if "vidmoly" in url:
        return url[:19] + url[25:]
    return url


def get_anime_list():
    """Extract the list of animes from a web page"""
    pages = 23
    animes = []
    for i in range(21, pages):
        # Loading bar
        bar_begin = "*"*(i-1)
        bar_end = "."*(pages-i+1)
        print(f"\r{colors.GREEN}|{bar_begin}{colors.RESET}{bar_end}{colors.GREEN}|", end="")

        x = web_requests.get(f"https://anime-sama.fr/catalogue/index.php?page={i}")
        anime_list = get_anime_list_from_page(x)
        animes.extend(anime_list)

        time.sleep(0.1)

    print(f"\r{'*'*pages}", end="")
    print(colors.RESET)
    return animes


def get_anime_list_from_page(x):
    x = BeautifulSoup(x, "html.parser")  # Soupify the world
    x = x.find_all("div", {"id": "result_catalogue"})[0]  # Extract the list of animes
    x1 = x.find_all('div', {'class': 'anime'})
    x2 = x.find_all('div', {'class': 'anime,'})

    x = x1
    x.extend(x2)

    animes = []
    for anime in x:
        data = anime.find_all('a')[0]

        name = data.find_all('h1')[0].text.strip().lower()
        link = data["href"]

        line = (name, link)
        animes.append(line)

    return animes


def get_seasons(x, url):
    """Extract the list of seasons from a web page"""
    x = BeautifulSoup(x, "html.parser")  # SOUPIFY THE WORLD
    x = x.find_all("script", string=re.compile("panneauanime"))[1]
    return get_seasons_script(x, url)


def get_seasons_script(s, url):
    s = s.text.strip()
    seasons = []
    s = s.split("\n")
    s = s[1:]

    for line in s:
        line = line.strip()
        line = line[14:-3]
        line = line.split('", "')

        name = line[0]
        link = f"{url}/{line[1]}"

        line = (name, link)
        seasons.append(line)

    return seasons


def get_episodes(url):
    url = url + "/episodes.js"  # Build the url
    data = web_requests.get(url)
    data = parse(data)  # Parse the js
    data = data['body']  # Get the code
    data = data[:-1]  # Remove the last element (empty statement)

    # Get the list of providers
    data = list(map(
        lambda a: a["declarations"][0]["init"]["elements"],
        data
    ))

    # Extract the links
    data = list(map(  # For each provider
        lambda provider: list(map(  # For each element
            lambda link: link["value"],  # Map to the link
            provider
        )),
        data
    ))

    # Search for vidmoly
    data_filtered = list(filter(
        lambda link: "vidmoly" in link[0],
        data
    ))

    # If vidmoly is found, return it
    if config.PREFER_VIDMOLY:
        if len(data_filtered) == 1:
            return list(map(optimised_link, data_filtered[0]))

    # Else, use the provider
    if config.PROVIDER >= (len(data)):
        print(f"{colors.RED}The provider N° {config.PROVIDER} doesn't exist for this anime !{colors.RESET}")
        config.PROVIDER = user_interface.ask_for_int(
            f"Please select another provider [0 - {len(data) - 1}] :",
            max_value=len(data) - 1,
            default=0)
    return list(map(optimised_link, data[config.PROVIDER]))
