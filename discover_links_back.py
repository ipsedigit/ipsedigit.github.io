"""
Discover who links back to eof.news by checking each DIRECT_LINKS site's homepage.
Run: python main.py --action discover-links-back
Output: list of { name, url } that contain a link to eof.news / ipsedigit.github.io.
Add those to LINKS_BACK in const.py and run --action direct to update the site.
"""
import time

import requests

from const import DIRECT_LINKS

# Strings that indicate a link to us (case-insensitive)
OUR_DOMAINS = ("eof.news", "ipsedigit.github.io")
USER_AGENT = "eof.news Backlink Discovery (https://ipsedigit.github.io/direct/)"
REQUEST_DELAY_SEC = 2
TIMEOUT = 15


def page_links_to_us(html: str) -> bool:
    """True if HTML contains an href or plain text pointing to our site."""
    if not html:
        return False
    lower = html.lower()
    return any(domain in lower for domain in OUR_DOMAINS)


def discover_links_back() -> list[dict]:
    """
    Fetch each DIRECT_LINKS URL and return entries whose page links to us.
    Rate-limited and polite (single request per site).
    """
    found = []
    for i, entry in enumerate(DIRECT_LINKS):
        name = entry.get("name", "?")
        url = entry.get("url", "").strip()
        if not url:
            continue
        if i > 0:
            time.sleep(REQUEST_DELAY_SEC)
        try:
            resp = requests.get(
                url,
                timeout=TIMEOUT,
                headers={"User-Agent": USER_AGENT},
                allow_redirects=True,
            )
            resp.raise_for_status()
            if page_links_to_us(resp.text):
                found.append({"name": name, "url": url})
                print(f"  ✓ {name}: {url}")
        except requests.RequestException as e:
            print(f"  ✗ {name}: {e}")
    return found


def main():
    print("Checking DIRECT_LINKS for pages that link to eof.news / ipsedigit.github.io ...")
    found = discover_links_back()
    print(f"\nFound {len(found)} site(s) that link to us.")
    if found:
        print("Add them to LINKS_BACK in const.py, then run: python main.py --action direct")
    return found
