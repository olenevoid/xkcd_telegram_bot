import requests
from urllib.parse import urlparse, unquote
from os import path


def save_image(url: str, filename: str, params: dict = None):

    response = requests.get(url, params=params)

    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_filename_from_url(url):
    parsed_url = urlparse(url)

    name = parsed_url.path.split('/')[-1]
    name = unquote(name)

    if not len(path.splitext(name)[1]):
        name = f'{name}.png'

    return name
