from environs import env
from image_helpers import IMAGE_FOLDER_NAME, save_image, get_filename_from_url
from os import makedirs, path
import requests
from typing import TypeAlias


ImageUrl: TypeAlias = str
Commentary: TypeAlias = str


def fetch_xkcd_post(post_id: int) -> tuple[ImageUrl, Commentary]:
    url = f'https://xkcd.com/{post_id}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    xkcd_post = response.json()

    return (xkcd_post.get('img'), xkcd_post.get('alt'))


def download_xkcd_image(url: str):
    filepath = path.join(IMAGE_FOLDER_NAME, get_filename_from_url(url))
    save_image(url, filepath)


def main():
    env.read_env()
    tg_token = env('TG_TOKEN')
    makedirs(IMAGE_FOLDER_NAME, exist_ok=True)
    url, comment = fetch_xkcd_post(666)
    print('comment', comment)
    download_xkcd_image(url)


if __name__ == '__main__':
    main()
