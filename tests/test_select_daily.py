from unittest.mock import patch
from news import select_daily_posts


def _make(title, score, niche, subniche, ctype, source_type='news', link=None):
    return {
        'title': title,
        'score': score,
        '_category': niche,
        '_subniche': subniche,
        'content_type': ctype,
        'source_type': source_type,
        'source': 'Test',
        'link': link or f'http://example.com/{title.replace(" ", "-").lower()}',
        'tags': ['tag1'],
        'community_score': 0,
    }


def _empty_state():
    return {
        'subniches': [],
        'niche_counts': {},
        'type_counts': {'breaking': 0, 'deep': 0, 'community': 0},
        'total': 0,
    }


def test_pass1_selects_one_per_niche():
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('AI second', 90, 'ai', 'ai-research', 'deep'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'deep'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'community'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    niches = [s['_category'] for s in selected]
    assert 'ai' in niches
    assert 'security' in niches
    assert 'cloud' in niches
    assert 'devtools' in niches
    assert 'software-engineering' in niches


def test_pass1_skips_niche_at_max():
    state = _empty_state()
    state['niche_counts'] = {'ai': 3}
    state['subniches'] = ['ai:llm', 'ai:ai-research', 'ai:mlops']
    state['total'] = 3

    candidates = [
        _make('AI extra', 100, 'ai', 'ai-infrastructure', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=state):
            selected = select_daily_posts()

    niches = [s['_category'] for s in selected]
    assert 'ai' not in niches
    assert 'security' in niches


def test_pass2_fills_open_slots():
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'deep'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'community'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'deep'),
        _make('AI bonus', 92, 'ai', 'ai-research', 'deep'),
        _make('Sec bonus', 88, 'security', 'appsec', 'deep'),
        _make('Creator post', 78, 'cloud', 'kubernetes', 'community', source_type='creator'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    assert len(selected) >= 5
    assert len(selected) <= 12


def test_pass2_respects_type_cap():
    candidates = [
        _make('AI top', 100, 'ai', 'llm', 'breaking'),
        _make('Sec top', 95, 'security', 'malware', 'breaking'),
        _make('Cloud top', 80, 'cloud', 'aws', 'breaking'),
        _make('DevTools top', 85, 'devtools', 'frameworks', 'breaking'),
        _make('SE top', 82, 'software-engineering', 'architecture', 'breaking'),
        _make('Extra1', 90, 'ai', 'ai-research', 'breaking'),
        _make('Extra2', 88, 'security', 'appsec', 'breaking'),
        _make('Deep1', 75, 'cloud', 'kubernetes', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    deep_selected = [s for s in selected if s['content_type'] == 'deep']
    assert len(deep_selected) >= 1


def test_no_duplicate_subniches():
    candidates = [
        _make('AI first', 100, 'ai', 'llm', 'breaking'),
        _make('AI same sub', 90, 'ai', 'llm', 'deep'),
        _make('AI diff sub', 85, 'ai', 'ai-research', 'deep'),
    ]

    with patch('news._build_candidates', return_value=candidates):
        with patch('news.get_daily_state', return_value=_empty_state()):
            selected = select_daily_posts()

    ai_posts = [s for s in selected if s['_category'] == 'ai']
    subniches = [s['_subniche'] for s in ai_posts]
    assert len(subniches) == len(set(subniches)), "Duplicate sub-niches selected"


def test_daily_target_reached_returns_empty():
    state = _empty_state()
    state['total'] = 12

    with patch('news._build_candidates', return_value=[]):
        with patch('news.get_daily_state', return_value=state):
            selected = select_daily_posts()

    assert selected == []
