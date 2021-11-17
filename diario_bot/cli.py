import argparse


def cli_args():
    parser = argparse.ArgumentParser(description="get gazette by date")
    parser.add_argument(
        "--data",
        metavar="YYYY-MM-DD",
        help="Data do diário no formato YYYY-MM-DD",
        type=str,
    )
    parser.add_argument(
        "--dry-run",
        help="Roda o bot sem tweetar, apenas mostrando os logs",
        action="store_true",
    )
    args = parser.parse_args()

    return args
