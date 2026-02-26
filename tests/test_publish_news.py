from unittest.mock import patch
from news import publish_news


def _make_selected(title, score, niche, subniche, ctype, source_type='news'):
    return {
        'title': title,
        'score': score,
        '_category': niche,
        '_subniche': subniche,
        'content_type': ctype,
        'source_type': source_type,
        'source': 'Test Source',
        'link': f'http://example.com/{title.replace(" ", "-").lower()}',
        'tags': ['AI'],
        'community_score': 0,
        'preview': 'A test preview description for the article.',
        'why_picked': 'test pick',
    }


def test_publish_news_calls_create_post_for_each_selected():
    entries = [
        _make_selected('Article 1', 100, 'ai', 'llm', 'breaking'),
        _make_selected('Article 2', 90, 'security', 'malware', 'deep'),
    ]

    with patch('news.select_daily_posts', return_value=entries):
        with patch('news.fetch_preview', side_effect=lambda e: e):
            with patch('news.create_post') as mock_create:
                with patch('news.track_published'):
                    with patch('news.track_daily_subniche'):
                        with patch('news.generate_tag_pages'):
                            publish_news()

    assert mock_create.call_count == 2


def test_publish_news_skips_entries_without_preview():
    entries = [
        _make_selected('No preview', 100, 'ai', 'llm', 'breaking'),
        _make_selected('Has preview', 90, 'security', 'malware', 'deep'),
    ]

    def fake_preview(e):
        if 'No preview' in e['title']:
            return None
        return e

    with patch('news.select_daily_posts', return_value=entries):
        with patch('news.fetch_preview', side_effect=fake_preview):
            with patch('news.create_post') as mock_create:
                with patch('news.track_published'):
                    with patch('news.track_daily_subniche'):
                        with patch('news.generate_tag_pages'):
                            publish_news()

    assert mock_create.call_count == 1
