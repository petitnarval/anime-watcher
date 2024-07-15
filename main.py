import parser
import web_requests

# EXTRACT THE DATA
x = web_requests.get('https://neko-sama.fr/animes-search-vostfr.json?13-07-2024')
animes = parser.get_anime_list(x)

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
x = web_requests.get(animes[choice][1])
episodes = parser.get_episode_list(x)

choice = ""
while True:
    try:
        choice = int(input(f"Select an episode [1-{len(episodes)}] "))

        if 0 <= choice <= len(episodes):
            break
        else:
            raise ValueError("Too big")
    except ValueError as e:
        print("Entree invalide:", e)

print(episodes[choice-1][1])