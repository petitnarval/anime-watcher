import subprocess

import data_parser
import user_interface
import web_requests

# PROMPT FOR PROVIDER
data_parser.PROVIDER = user_interface.ask_for_int("Select a provider (default: 0): ", default=0)

# EXTRACT THE DATA
print("Loading data...")
animes = data_parser.get_anime_list()


# FILTER THE DATA
query = input("What do you want to watch ? ").lower().strip()
animes = list(filter(lambda anime: query in anime[0], animes))


# PRINT THE AVAILABLE ANIMES
for i in range(len(animes)):
    a = animes[i]
    print(f"[{i}] {a[0]}")


# PROMPTS THE USER TO CHOSE AN ANIME
choice = ""
while True:
    try:
        choice = int(input("Select an anime: "))

        if 0 <= choice < len(animes):
            break
        else:
            raise ValueError("Too big")
    except ValueError as e:
        print("Invalid input:", e)


# FILTER THE EPISODES
url = animes[choice][1]
x = web_requests.get(url)
seasons = data_parser.get_seasons(x, url)


# ASK FOR SEASON
choice = ""
if len(seasons) == 1:
    choice = 1
else:
    choice = user_interface.ask_for_int(f"Chose a season [1-{len(seasons)}] : ",
                                        min_value=1,
                                        max_value=len(seasons))

url = seasons[choice - 1][1]
episodes = data_parser.get_episodes(url)


# ASK FOR EPISODE
choice = ""
if len(episodes) == 1:
    choice = 1
else:
    choice = user_interface.ask_for_int(f"Select an episode [1-{len(episodes)}] : ",
                                        min_value=1,
                                        max_value=len(episodes))
episode = episodes[choice - 1]

# START THE EPISODE
subprocess.call(f'mpv {episode}', shell=True)
