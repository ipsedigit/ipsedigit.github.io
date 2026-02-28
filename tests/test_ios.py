import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ios import _fetch_rss_articles, _generate_page


def test_generate_page_contains_permalink():
    page = _generate_page([])
    assert "permalink: /ios/" in page


def test_generate_page_contains_liquid_loop():
    page = _generate_page([])
    assert "{% for article in articles %}" in page
    assert "site.data.ios.articles" in page


def test_generate_page_references_excerpt_and_source():
    page = _generate_page([])
    assert "article.excerpt" in page
    assert "article.source" in page
