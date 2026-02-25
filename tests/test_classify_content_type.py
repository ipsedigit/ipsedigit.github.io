from news import classify_content_type


def test_creator_source_is_community():
    entry = {'title': 'How I Built My Startup', 'source_type': 'creator', 'tags': []}
    assert classify_content_type(entry) == 'community'


def test_show_hn_is_community():
    entry = {'title': 'Show HN: A new terminal emulator', 'source_type': 'aggregator', 'tags': []}
    assert classify_content_type(entry) == 'community'


def test_announcement_is_breaking():
    entry = {'title': 'OpenAI launches GPT-5', 'source_type': 'research_blog', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_vulnerability_is_breaking():
    entry = {'title': 'Critical vulnerability in OpenSSL', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_cve_is_breaking():
    entry = {'title': 'CVE-2026-1234: Remote code execution', 'source_type': 'security', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_research_paper_is_deep():
    entry = {'title': 'New arxiv paper on attention mechanisms', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_how_we_is_deep():
    entry = {'title': 'How we scaled to 1M websocket connections', 'source_type': 'corporate_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_tutorial_is_deep():
    entry = {'title': 'A complete guide to Kubernetes networking', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_research_blog_source_is_deep():
    entry = {'title': 'Improving language model efficiency', 'source_type': 'research_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_se_blog_source_is_deep():
    entry = {'title': 'Thoughts on software complexity', 'source_type': 'se_blog', 'tags': []}
    assert classify_content_type(entry) == 'deep'


def test_security_source_with_threat_is_breaking():
    entry = {'title': 'New ransomware campaign targets hospitals', 'source_type': 'security', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_generic_news_defaults_to_breaking():
    entry = {'title': 'Google acquires startup for $2B', 'source_type': 'news', 'tags': []}
    assert classify_content_type(entry) == 'breaking'


def test_built_a_is_community():
    entry = {'title': 'I built a CLI tool for managing dotfiles', 'source_type': 'aggregator', 'tags': []}
    assert classify_content_type(entry) == 'community'
