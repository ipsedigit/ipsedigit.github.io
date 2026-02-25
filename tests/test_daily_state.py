import os
from unittest.mock import patch
from datetime import date


def test_get_daily_state_empty(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import get_daily_state
        state = get_daily_state()

    assert state['subniches'] == []
    assert state['niche_counts'] == {}
    assert state['type_counts'] == {'breaking': 0, 'deep': 0, 'community': 0}
    assert state['total'] == 0


def test_get_daily_state_with_entries(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    today = date.today().isoformat()
    with open(state_file, 'w') as f:
        f.write(f"{today}:ai:llm:breaking\n")
        f.write(f"{today}:security:malware:breaking\n")
        f.write(f"{today}:cloud:kubernetes:deep\n")
        f.write("2020-01-01:ai:old:breaking\n")

    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import get_daily_state
        state = get_daily_state()

    assert state['total'] == 3
    assert state['niche_counts'] == {'ai': 1, 'security': 1, 'cloud': 1}
    assert state['type_counts'] == {'breaking': 2, 'deep': 1, 'community': 0}
    assert 'ai:llm' in state['subniches']
    assert 'security:malware' in state['subniches']
    assert 'cloud:kubernetes' in state['subniches']


def test_get_daily_state_file_missing(tmp_path):
    with patch('news.DAILY_CATEGORIES_FILE', str(tmp_path / "nonexistent.txt")):
        from news import get_daily_state
        state = get_daily_state()

    assert state['total'] == 0


def test_track_writes_content_type(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import track_daily_subniche
        track_daily_subniche('ai', 'llm', 'breaking')

    with open(state_file) as f:
        content = f.read()

    today = date.today().isoformat()
    assert f"{today}:ai:llm:breaking\n" in content


def test_track_appends_multiple(tmp_path):
    state_file = str(tmp_path / "daily.txt")
    with patch('news.DAILY_CATEGORIES_FILE', state_file):
        from news import track_daily_subniche
        track_daily_subniche('ai', 'llm', 'breaking')
        track_daily_subniche('security', 'malware', 'deep')

    with open(state_file) as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2
