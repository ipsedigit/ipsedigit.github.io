import argparse

from news import publish_news


def main(action: str):
    match action:
        case "news":
            publish_news()
        case _:
            publish_news()


# Using the special variable
# __name__
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish tech news")
    parser.add_argument("--action", type=str, default="news", help="Action: news")
    args = parser.parse_args()
    main(action=args.action)
