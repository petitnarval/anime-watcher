import requests


def get(url):
    x = requests.get(url)
    x = x.text
    x = x.lower()
    return x
