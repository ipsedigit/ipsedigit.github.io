"""
Discover who links back to eof.news by checking each DIRECT_FEEDS site (derived from feed URL).
Run: python main.py --action discover-links-back
Output: list of { name, url } that contain a link to eof.news / ipsedigit.github.io.
Add those to LINKS_BACK in const.py and run --action direct to update the site.
"""
import re
import time
from urllib.parse import urlparse, urlunparse

import requests

from const import DIRECT_FEEDS

OUR_DOMAINS = ("eof.news", "ipsedigit.github.io")
USER_AGENT = "eof.news Backlink Discovery (https://ipsedigit.github.io/direct/)"
REQUEST_DELAY_SEC = 2
TIMEOUT = 15


def _blog_root_from_feed(feed_url: str) -> str:
    """Derive blog root URL from feed URL."""
    if not feed_url or not feed_url.startswith("http"):
        return ""
    p = urlparse(feed_url)
    path = (p.path or "/").rstrip("/")
    for suf in ["/feed", "/atom.xml", "/feed.xml", "/rss", "/feeds/posts/default"]:
        path = re.sub(re.escape(suf) + r"?$", "", path, flags=re.IGNORECASE)
    path = path.rstrip("/") or "/"
    return urlunparse((p.scheme, p.netloc, path, "", "", "")).rstrip("/")


def page_links_to_us(html: str) -> bool:
    if not html:
        return False
    lower = html.lower()
    return any(domain in lower for domain in OUR_DOMAINS)


def discover_links_back() -> list[dict]:
    found = []
    for i, feed_spec in enumerate(DIRECT_FEEDS):
        name = feed_spec.get("name", "?")
        feed_url = feed_spec.get("feed_url", "").strip()
        if not feed_url:
            continue
        url = _blog_root_from_feed(feed_url)
        if not url:
            continue
        if i > 0:
            time.sleep(REQUEST_DELAY_SEC)
        try:
            resp = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
            resp.raise_for_status()
            if page_links_to_us(resp.text):
                found.append({"name": name, "url": url})
                print(f"  ✓ {name}: {url}")
        except requests.RequestException as e:
            print(f"  ✗ {name}: {e}")
    return found


def main():
    print("Checking DIRECT_FEEDS sites for pages that link to eof.news / ipsedigit.github.io ...")
    found = discover_links_back()
    print(f"\nFound {len(found)} site(s) that link to us.")
    if found:
        print("Add them to LINKS_BACK in const.py, then run: python main.py --action direct")
    return found
