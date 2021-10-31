import argparse


def cli_args():
    parser = argparse.ArgumentParser(description="get gazette by date")
    parser.add_argument(
        "--data", "--d", metavar="YYYY-MM-DD", help="gazette date", type=str
    )
    parser.add_argument(
        "--dry-run", help="run without posting tweets", action="store_true"
    )
    args = parser.parse_args()

    return args
