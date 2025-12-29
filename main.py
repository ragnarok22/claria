from config import Config
from bot import ClarIABot


def main():
    config = Config()
    bot = ClarIABot(config)
    bot.run()


if __name__ == "__main__":
    main()
