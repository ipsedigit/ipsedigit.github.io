from const import FEATURED_DEVS, NEWS_SOURCES


def test_featured_devs_have_required_fields():
    required = {'name', 'slug', 'url', 'bio', 'source_name', 'featured_since'}
    for key, dev in FEATURED_DEVS.items():
        missing = required - set(dev.keys())
        assert not missing, f"{key} missing fields: {missing}"


def test_featured_devs_source_names_match_news_sources():
    """Every featured dev's source_name should match a source in NEWS_SOURCES."""
    all_names = {s['name'] for s in NEWS_SOURCES.values()}
    for key, dev in FEATURED_DEVS.items():
        assert dev['source_name'] in all_names, (
            f"{key}: source_name '{dev['source_name']}' not found in NEWS_SOURCES"
        )


def test_slugs_are_unique():
    slugs = [d['slug'] for d in FEATURED_DEVS.values()]
    assert len(slugs) == len(set(slugs)), "Duplicate slugs found"
