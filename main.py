import argparse


def main(action: str, niche: str = None):
    match action:
        case "news":
            from news import publish_news
            publish_news(target_niche=niche)
        case "digest":
            from digest import publish_digest
            publish_digest()
        case "cves":
            from cves import publish_cves
            publish_cves()
        case "models":
            from models import publish_models
            publish_models()
        case "github":
            from github_trending import publish_github_trending
            publish_github_trending()
        case "direct":
            from news import update_direct_links_data
            update_direct_links_data()
        case "discover-links-back":
            from discover_links_back import main as discover_main
            discover_main()
        case _:
            from news import publish_news
            publish_news(target_niche=niche)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish tech news")
    parser.add_argument("--action", type=str, default="news", help="Action: news, digest, cves, models, github, direct, discover-links-back")
    parser.add_argument("--niche", type=str, default=None, help="Target niche: ai, software-engineering, devtools, cloud, security")
    args = parser.parse_args()
    main(action=args.action, niche=args.niche)
