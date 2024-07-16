from bs4 import BeautifulSoup
from pyjsparser import parse

import web_requests

PROVIDER = 0


def get_anime_list():
    """Extract the list of animes from a web page"""
    animes = []
    for i in range(1, 33):
        x = web_requests.get(f"https://anime-sama.fr/catalogue/index.php?page={i}")
        l = get_anime_list_from_page(x)
        animes.extend(l)
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

    x = BeautifulSoup(x, "html.parser")  # Soupify the world
    x = x.find_all("div", {"class": "flex flex-wrap overflow-y-hidden justify-start bg-slate-900 bg-opacity-70 rounded "
                                    "mt-2 h-auto"})[0]  # Extract the list of seasons
    x = x.find_all("script")[0].text.strip()
    return get_seasons_script(x, url)


def get_seasons_script(s, url):
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
    url = url + "/episodes.js"
    x = web_requests.get(url)
    x = parse(x)
    x = x['body']
    x = x[PROVIDER]
    x = x['declarations']
    x = x[0]
    x = x['init']
    x = x['elements']
    x = list(map(
        lambda e: e['value'],
        x
    ))
    return x
