import argparse


def main(action: str, niche: str = None):
    match action:
        case "news":
            from news import publish_news
            publish_news(target_niche=niche)
        case "cves":
            from cves import publish_cves
            publish_cves()
        case "github":
            from github_trending import publish_github_trending
            publish_github_trending()
        case "outages":
            from outages import publish_outages
            publish_outages()
        case "devs":
            from news import update_devs_articles_data
            update_devs_articles_data()
        case _:
            from news import publish_news
            publish_news(target_niche=niche)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish tech news")
    parser.add_argument("--action", type=str, default="news", help="Action: news, cves, github, devs, outages")
    parser.add_argument("--niche", type=str, default=None, help="Target niche: ai, software-engineering, devtools, cloud, security")
    args = parser.parse_args()
    main(action=args.action, niche=args.niche)
