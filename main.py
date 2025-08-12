from environs import env
from image_helpers import IMAGE_FOLDER_NAME, save_image, get_filename_from_url
from os import makedirs, path
import requests
from typing import TypeAlias


ImageUrl: TypeAlias = str
Commentary: TypeAlias = str


def fetch_xkcd_post(post_id: int) -> tuple[ImageUrl, Commentary]:
    image_url = f'https://xkcd.com/{post_id}/info.0.json'

    response = requests.get(image_url)
    response.raise_for_status()

    xkcd_post = response.json()

    return (xkcd_post.get('img'), xkcd_post.get('alt'))




def main():
    env.read_env()
    tg_token = env('TG_TOKEN')


if __name__ == '__main__':
    main()
