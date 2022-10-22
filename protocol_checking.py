import requests


def protocol_checking(url):
    if '://' not in url:
        url = "http://" + url
    r = requests.get(url)
    if 'https' in r.url:
        return 0
    return 1
