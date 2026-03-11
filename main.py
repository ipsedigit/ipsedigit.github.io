import argparse


def main(action: str, niche: str = None):
    match action:
        case "news":
            from news import publish_news
            publish_news(target_niche=niche)
        case "devlogs":
            from devlogs import publish_devlogs
            publish_devlogs()
        case "outages":
            from outages import publish_outages
            publish_outages()
        case _:
            from news import publish_news
            publish_news(target_niche=niche)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish tech news")
    parser.add_argument("--action", type=str, default="news", help="Action: news")
    parser.add_argument("--niche", type=str, default=None, help="Target niche: ai, software-engineering, devtools, cloud, security")
    args = parser.parse_args()
    main(action=args.action, niche=args.niche)
