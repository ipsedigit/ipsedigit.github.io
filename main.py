import argparse

from news import publish_news
from quotes import publish_quote


def main(action: str):
    match action:
        case "news":
            publish_news()
        case "quotations":
            publish_quote()
        case _:
            publish_quote()


# Using the special variable
# __name__
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Let's do something")
    parser.add_argument("--action", type=str, help=f"""
    Choose an action: \n
    - quotations\n 
    - news
""")
    args = parser.parse_args()
    main(action=args.action)
