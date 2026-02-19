import os
import re

SITE_URL = "https://eof.news"

CATEGORY_HASHTAGS = {
    'ai': '#AI #MachineLearning',
    'security': '#CyberSecurity #InfoSec',
}


def _post_slug(file_name):
    """Extract slug from post file path."""
    base = os.path.basename(file_name)
    # Remove date prefix and .md extension
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', base)
    slug = slug.replace('.md', '')
    return slug


def post_tweet(news, category, file_name):
    """Post a tweet about a newly published article using Twitter API v2."""
    import tweepy

    api_key = os.environ.get("TWITTER_API_KEY", "")
    api_secret = os.environ.get("TWITTER_API_SECRET", "")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN", "")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET", "")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("   ⚠️ Twitter credentials not set — skipping tweet")
        return

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

    title = news.get("title", "")[:80]
    preview = news.get("preview", "")
    desc_snippet = preview[:100] + "..." if len(preview) > 100 else preview

    slug = _post_slug(file_name)
    post_url = f"{SITE_URL}/{slug}"

    category_tags = CATEGORY_HASHTAGS.get(category, '#Tech')
    emoji = "🤖" if category == 'ai' else "🔐"

    tweet = (
        f"{title} {emoji}\n\n"
        f"{desc_snippet}\n\n"
        f"{post_url}\n\n"
        f"{category_tags} #Tech"
    )

    # Twitter limit is 280 chars; trim description if needed
    if len(tweet) > 280:
        overflow = len(tweet) - 280
        trimmed = desc_snippet[:max(0, len(desc_snippet) - overflow - 3)] + "..."
        tweet = (
            f"{title} {emoji}\n\n"
            f"{trimmed}\n\n"
            f"{post_url}\n\n"
            f"{category_tags} #Tech"
        )

    response = client.create_tweet(text=tweet)
    print(f"   🐦 Tweeted: {response.data['id']}")
