from dotenv import load_dotenv

from diario_bot.apis.maria_quiteria import get_todays_gazette
from diario_bot.twitter import post_todays_gazette

load_dotenv()


def main():
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)


if __name__ == "__main__":
    main()
