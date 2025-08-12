from environs import env


def main():
    env.read_env()
    tg_token = env('TG_TOKEN')


if __name__ == '__main__':
    main()
