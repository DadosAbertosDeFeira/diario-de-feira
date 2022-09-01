import os
from logging import WARNING

import sentry_sdk
from dotenv import load_dotenv
from loguru import logger
from sentry_sdk.integrations.logging import EventHandler, LoggingIntegration

from diario_bot.apis.maria_quiteria import get_gazette_by_date
from diario_bot.cli import cli_args
from diario_bot.twitter import post_gazettes

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[LoggingIntegration(level=None, event_level=None)],
)
logger.add(EventHandler(level=WARNING))

load_dotenv()
CLI_ARGS = cli_args()


def main():
    gazette_date = CLI_ARGS.data or None
    gazettes = get_gazette_by_date(gazette_date)

    set_dry_run = CLI_ARGS.dry_run or False
    post_gazettes(gazettes, dry_run=set_dry_run)


if __name__ == "__main__":
    main()
