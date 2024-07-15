import data_parser
import web_requests
import subprocess
import sys

if len(sys.argv) >= 2:
    data_parser.PROVIDER = int(sys.argv[1])
# EXTRACT THE DATA
animes = data_parser.get_anime_list()

# FILTER THE DATA

query = input("What do you want to watch ? ").lower()


def filter_animes(x):
    return query in x[0]


animes = list(filter(filter_animes, animes))

# Print the available animes
for i in range(len(animes)):
    a = animes[i]
    print(f"[{i}] {a[0]}: {a[1]}")

choice = ""
while True:
    try:
        choice = int(input("Select an anime: "))

        if 0 <= choice < len(animes):
            break
        else:
            raise ValueError("Too big")
    except ValueError as e:
        print("Entree invalide:", e)

# FILTER THE EPISODES
url = animes[choice][1]
x = web_requests.get(url)
seasons = data_parser.get_seasons(x,url)


# ASK FOR CHOICE SEASON
choice = ""
if len(seasons) == 1:
    choice = 1
else:
    while True:
        try:
            choice = int(input(f"Select a season [1-{len(seasons)}] "))

            if 0 <= choice <= len(seasons):
                break
            else:
                raise ValueError("Too big")
        except ValueError as e:
            print("Entree invalide:", e)

url = seasons[choice-1][1]
episodes = data_parser.get_episodes(url)


# ASK FOR CHOICE EPISODES
choice = ""
if len(episodes) == 1:
    choice = 1
else:
    while True:
        try:
            choice = int(input(f"Select an episode [1-{len(episodes)}] "))

            if 0 <= choice <= len(episodes):
                break
            else:
                raise ValueError("Too big")
        except ValueError as e:
            print("Entree invalide:", e)
episode = episodes[choice-1]


subprocess.call(f'mpv {episode}', shell=True)