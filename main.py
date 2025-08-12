from environs import env
from image_helpers import IMAGE_FOLDER_NAME, save_image, get_filename_from_url
from os import makedirs, path
import requests
from typing import TypeAlias
from random import randint
from telegram import Bot


ImageUrl: TypeAlias = str
Commentary: TypeAlias = str


def send_telegram_post(
        tg_bot_token: str | int,
        tg_channel_id: str | int,
        image_path: str,
        caption: str
):
    bot = Bot(tg_bot_token)

    with open(image_path, 'rb') as image:
        bot.send_photo(tg_channel_id, image, caption=caption)


def fetch_last_xkcd_post_id():
    url = 'https://xkcd.com/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    xkcd_post = response.json()

    return xkcd_post.get('num')


def fetch_xkcd_post(post_id: int) -> tuple[ImageUrl, Commentary]:
    url = f'https://xkcd.com/{post_id}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    xkcd_post = response.json()

    return (xkcd_post.get('img'), xkcd_post.get('alt'))


def main():
    env.read_env()
    tg_token = env('TG_TOKEN')
    tg_channel_id = env('TG_CHANNEL_ID')
    makedirs(IMAGE_FOLDER_NAME, exist_ok=True)
    
    last_post_id = fetch_last_xkcd_post_id()
    random_post_id = randint(1, last_post_id)
    url, comment = fetch_xkcd_post(random_post_id)
    filepath = path.join(IMAGE_FOLDER_NAME, get_filename_from_url(url))
    save_image(url, filepath)
    send_telegram_post(tg_token, tg_channel_id, filepath, comment)


if __name__ == '__main__':
    main()
