from bs4 import BeautifulSoup
import json


def get_anime_list(x):
    """Extract the list of animes from a web page"""
    x = json.loads(x)
    animes = []

    for anime in x:
        name = anime["title"]
        link = anime['url']
        line = (name, link)
        animes.append(line)

    return animes


def get_episode_list(x):
    """Extract the list of animes from a web page"""
    x = BeautifulSoup(x, "html.parser")  # Soupify the world
    x = x.find_all("div", {"class": "episodes"})[0]  # Extract the list of animes
    x = x.find_all('a')
    episodes = []
    for i in range(len(x)-1, -1, -1):
        episode = x[i]

        name = len(x) - i
        link = episode["href"]

        line = (name, link)
        episodes.append(line)

    return episodes


# :• \xa0\xa0jujutsu kaisen 2 – 01 vostfr