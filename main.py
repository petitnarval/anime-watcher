import subprocess

from thefuzz import fuzz

import colors
import config
import data_parser
import user_interface
import web_requests


def start_episode(episode):
    print(f"Loading Episode...")
    subprocess.call(f'mpv {episode}', shell=True)


options = "a"
choice = {
    "anime": None,
    "season": None,
    "episode": None,
}

# EXTRACT THE DATA
print("Loading data...")
animes_list = data_parser.get_anime_list()

while True:

    if len(options) >= 1:
        option = options[0]
        options = options[1:]
    else:
        option = None

    # ASK FOR PROVIDER
    if option == "p":
        config.PREFER_VIDMOLY = False
        data_parser.PROVIDER = user_interface.ask_for_int("Select a provider (default: 0): ", default=0)

    # ASK FOR ANIME
    elif option == "a":
        animes = []
        while len(animes) == 0:
            # FILTER THE DATA
            query = input("What do you want to watch ? ").lower().strip()
            animes = list(filter(
                lambda anime: fuzz.partial_ratio(anime[0], query) >= 80,
                animes_list))

        # PRINT THE AVAILABLE ANIMES
        for i in range(len(animes)):
            a = animes[i]
            print(f"{colors.MAGENTA}[{i}]{colors.RESET} {a[0]}")

        # PROMPTS THE USER TO CHOSE AN ANIME
        if len(animes) == 1:
            choice["anime"] = 0
        else:
            choice["anime"] = user_interface.ask_for_int(message="Choose a anime: ", max_value=len(animes) - 1)

        options = "s"

    # ASK FOR SEASON
    elif option == "s":

        # FILTER THE EPISODES
        url = animes[choice["anime"]][1]
        x = web_requests.get(url)
        seasons = data_parser.get_seasons(x, url)

        # ASK FOR SEASON
        if len(seasons) == 1:
            choice["season"] = 0
        else:
            choice["season"] = user_interface.ask_for_int(
                f"Chose a season {colors.YELLOW}[1-{len(seasons)}]{colors.RESET} : ",
                min_value=1,
                max_value=len(seasons)) - 1

        options = "e"

    # ASK FOR EPISODE
    elif option == "e":
        url = seasons[choice["season"]][1]
        episodes = data_parser.get_episodes(url)

        # ASK FOR EPISODE
        if len(episodes) == 1:
            choice["episode"] = 0
        else:
            choice["episode"] = user_interface.ask_for_int(
                f"Select an episode {colors.BLUE}[1-{len(episodes)}]{colors.RESET} : ",
                min_value=1,
                max_value=len(episodes)) - 1

        episode = episodes[choice["episode"]]
        start_episode(episode)

    elif option == "n":
        choice["episode"] += 1
        # CHANGE SEASON IF TRY TO GO NEXT AT THE LAST EPISODE
        if choice["episode"] == len(episodes):
            choice["season"] += 1
            choice["episode"] = 0

        if choice["season"] == len(seasons):
            print("There is nothing else to watch !")
            options = "a"
            continue

        url = seasons[choice["season"]][1]
        episodes = data_parser.get_episodes(url)
        episode = episodes[choice["episode"]]
        start_episode(episode)

    # QUIT
    elif option == "q":
        break

    elif option is None:

        # ASK FOR NEW ACTIONS
        print(
            "Possible actions:\n"
            f"{colors.BLUE}[p]{colors.RESET} change provider\n"
            f"{colors.BLUE}[a]{colors.RESET} change anime\n"
            f"{colors.BLUE}[s]{colors.RESET} change season\n"
            f"{colors.BLUE}[e]{colors.RESET} change episode\n"
            f"{colors.CYAN}[n]{colors.RESET} next episode\n"
            f"{colors.BLUE}[q]{colors.RESET} quit\n"
        )

        options = user_interface.ask_for_character("What do you want to do ? ", "pasenq")
