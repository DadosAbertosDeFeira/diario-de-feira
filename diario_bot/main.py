from dotenv import load_dotenv

from diario_bot.apis.maria_quiteria import get_gazette_by_date
from diario_bot.cli import cli_args
from diario_bot.twitter import post_gazettes

load_dotenv()
CLI_ARGS = cli_args()


def main():
    gazette_date = CLI_ARGS.data or None
    gazettes = get_gazette_by_date(gazette_date)

    set_dry_run = CLI_ARGS.dry_run or False
    post_gazettes(gazettes, dry_run=set_dry_run)


if __name__ == "__main__":
    main()
