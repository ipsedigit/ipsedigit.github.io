from const import (
    CONTENT_TYPE_PATTERNS,
    MIN_SCORE,
    MIN_SCORE_FALLBACK,
    DAILY_TARGET,
    DAILY_MINIMUM,
    MAX_PER_TYPE,
    MAX_POSTS_PER_NICHE_PER_DAY,
)


def test_constants_exist_and_are_sane():
    assert MIN_SCORE == 70
    assert MIN_SCORE_FALLBACK == 60
    assert DAILY_TARGET == 12
    assert DAILY_MINIMUM == 8
    assert MAX_PER_TYPE == 4
    assert MAX_POSTS_PER_NICHE_PER_DAY == 3

    assert 'breaking' in CONTENT_TYPE_PATTERNS
    assert 'deep' in CONTENT_TYPE_PATTERNS
    assert 'community' in CONTENT_TYPE_PATTERNS

    for ctype, patterns in CONTENT_TYPE_PATTERNS.items():
        assert isinstance(patterns, list)
        assert len(patterns) > 0
