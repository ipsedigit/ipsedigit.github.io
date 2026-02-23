import argparse


def main(action: str):
    match action:
        case "news":
            from news import publish_news
            publish_news()
        case "digest":
            from digest import publish_digest
            publish_digest()
        case "trends":
            from trends import publish_trends
            publish_trends()
        case "cves":
            from cves import publish_cves
            publish_cves()
        case "models":
            from models import publish_models
            publish_models()
        case "github":
            from github_trending import publish_github_trending
            publish_github_trending()
        case _:
            from news import publish_news
            publish_news()


# Using the special variable
# __name__
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish tech news")
    parser.add_argument("--action", type=str, default="news", help="Action: news, digest, trends, cves, models, github")
    args = parser.parse_args()
    main(action=args.action)
