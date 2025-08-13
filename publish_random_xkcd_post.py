from environs import env
from image_helpers import save_image, get_filename_from_url
from os import remove, path
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from random import randint
from telegram import Bot
from telegram.error import TelegramError


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


def fetch_xkcd_post(post_id: int) -> tuple[str, str]:
    url = f'https://xkcd.com/{post_id}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    xkcd_post = response.json()

    return (xkcd_post.get('img'), xkcd_post.get('alt'))


def main():
    env.read_env()
    tg_token = env('TG_TOKEN')
    tg_channel_id = env('TG_CHANNEL_ID')

    try:
        last_post_id = fetch_last_xkcd_post_id()
        random_post_id = randint(1, last_post_id)
        url, comment = fetch_xkcd_post(random_post_id)
    
    except (HTTPError, Timeout, ConnectionError):
        print("Произошла ошибка при поиске последнего поста")
        return

    try:    
        filename = get_filename_from_url(url)
        save_image(url, filename)
        send_telegram_post(tg_token, tg_channel_id, filename, comment)

    except (HTTPError, Timeout, ConnectionError):
        print("Произошла ошибка при скачивании изображения")

    except TelegramError:
        print("Произошла ошибка при отправке в Telegram")

    except Exception:
        print("Произошла неизвестная ошибка")

    finally:
        if filename and path.exists(filename):
            remove(filename)


if __name__ == '__main__':
    main()
