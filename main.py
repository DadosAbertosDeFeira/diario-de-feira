from dotenv import load_dotenv

from diario.maria_quiteria import get_todays_gazette
from diario.twitter import post_todays_gazette

load_dotenv()

if __name__ == "__main__":
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)
