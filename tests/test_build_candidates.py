from unittest.mock import patch
from news import _build_candidates


def _make_entry(title, source_type, score, category, subniche, link):
    return {
        'title': title,
        'source_type': source_type,
        'score': score,
        '_category': category,
        '_subniche': subniche,
        'link': link,
        'tags': ['AI', 'Machine Learning'],
        'community_score': 0,
        'source': 'Test Source',
        'content_type': 'breaking',
    }


def test_build_candidates_filters_published():
    entries = [
        _make_entry('Published article', 'news', 80, 'ai', 'llm', 'http://published.com'),
        _make_entry('New article', 'news', 80, 'ai', 'llm', 'http://new.com'),
    ]

    with patch('news.read_text_file', return_value={'http://published.com'}):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates()

    links = [c['link'] for c in candidates]
    assert 'http://published.com' not in links
    assert 'http://new.com' in links


def test_build_candidates_filters_below_min_score():
    entries = [
        _make_entry('Low score', 'news', 50, 'ai', 'llm', 'http://low.com'),
        _make_entry('High score', 'news', 80, 'ai', 'llm', 'http://high.com'),
    ]

    with patch('news.read_text_file', return_value=set()):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates(min_score=70)

    assert len(candidates) == 1
    assert candidates[0]['link'] == 'http://high.com'


def test_build_candidates_sorted_by_score_desc():
    entries = [
        _make_entry('Mid', 'news', 80, 'ai', 'llm', 'http://mid.com'),
        _make_entry('Top', 'news', 120, 'security', 'malware', 'http://top.com'),
        _make_entry('Low', 'news', 71, 'cloud', 'aws', 'http://low.com'),
    ]

    with patch('news.read_text_file', return_value=set()):
        with patch('news._scan_all_sources', return_value=entries):
            candidates = _build_candidates(min_score=70)

    assert candidates[0]['score'] == 120
    assert candidates[1]['score'] == 80
    assert candidates[2]['score'] == 71
