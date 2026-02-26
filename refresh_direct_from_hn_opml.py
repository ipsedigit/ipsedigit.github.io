"""
Build the Direct reference list from the reliable HN personal-blogs OPML.
One resource per developer: their blog homepage (single URL).
Source: https://github.com/outcoldman/hackernews-personal-blogs (list.opml)

Run: python refresh_direct_from_hn_opml.py
Output: Python list of {"name", "url", "description"} to paste into DIRECT_REFERENCE_LIST in const.py.
"""
import re
import xml.etree.ElementTree as ET
import urllib.request
from urllib.parse import urlparse, urlunparse

OPML_URL = "https://raw.githubusercontent.com/outcoldman/hackernews-personal-blogs/master/list.opml"
DESCRIPTION = "Personal blog (HN)."


def blog_root_from_feed(feed_url: str) -> str:
    """Derive blog root URL from feed URL. Returns single resource (homepage)."""
    if not feed_url or not feed_url.startswith("http"):
        return ""
    p = urlparse(feed_url)
    path = (p.path or "/").rstrip("/")
    # Strip common feed path suffixes (order matters: longer first)
    suffixes = [
        r"/feeds/posts/default$",
        r"/feeds/all\.atom\.xml$",
        r"/blog/feed/atom/?$",
        r"/blog/feed/?$",
        r"/feed\.xml$",
        r"/feed\.rss$",
        r"/feed\.atom$",
        r"/feed/?$",
        r"/atom\.xml$",
        r"/atom/?$",
        r"/rss\.xml$",
        r"/index\.rss$",
        r"/index\.xml$",
        r"/news\.rss$",
        r"/posts\.xml$",
        r"/posts\.rss$",
        r"/articles\.rss$",
        r"/blog\.xml$",
        r"/rss/?$",
    ]
    for suf in suffixes:
        path = re.sub(suf, "", path, flags=re.IGNORECASE)
    path = path.rstrip("/") or "/"
    # Drop /author, /data (feed-only path segments at end)
    path = re.sub(r"/author$", "", path, flags=re.IGNORECASE)
    path = path.rstrip("/") or "/"
    out = urlunparse((p.scheme, p.netloc, path or "/", "", "", ""))
    out = out.rstrip("/").rstrip(".")
    return out


def main():
    req = urllib.request.Request(OPML_URL, headers={"User-Agent": "eof.news"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read().decode("utf-8")
    root = ET.fromstring(data)
    outlines = root.findall(".//outline")
    entries = []
    seen_urls = set()
    for o in outlines:
        title = (o.get("title") or "").strip()
        if not title or title == "HN Personal Blogs":
            continue
        feed = (o.get("xmlUrl") or o.get("htmlUrl") or "").strip()
        if not feed:
            continue
        url = blog_root_from_feed(feed)
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        entries.append({
            "name": title,
            "url": url,
            "description": DESCRIPTION,
        })
    # Limit for const.py (single source, one resource per dev)
    max_entries = 120
    entries = entries[:max_entries]
    # Print as Python list for const.py
    print("# Paste into DIRECT_REFERENCE_LIST in const.py (source: HN personal blogs OPML)")
    print("DIRECT_REFERENCE_LIST = [")
    for e in entries:
        # Safe for Python literal (escape single quotes in name)
        name = e["name"].replace("\\", "\\\\").replace("'", "\\'")
        print(f"    {{'name': '{name}', 'url': '{e['url']}', 'description': '{e['description']}'}},")
    print("]")
    print(f"# Total: {len(entries)} developers, one resource each")


if __name__ == "__main__":
    main()
