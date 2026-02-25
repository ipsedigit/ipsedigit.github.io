import os
import json
from unittest.mock import patch
from news import generate_dev_profiles


MOCK_DEVS = {
    'testdev': {
        'name': 'Test Dev',
        'slug': 'test-dev',
        'url': 'https://testdev.com',
        'bio': 'A test developer.',
        'source_name': 'Test Dev Blog',
        'featured_since': '2026-02-25',
    },
}


def test_generates_devs_json(tmp_path):
    data_dir = tmp_path / "docs" / "_data"
    devs_dir = tmp_path / "docs" / "devs"

    with patch('news.FEATURED_DEVS', MOCK_DEVS):
        generate_dev_profiles(
            data_path=str(data_dir / "devs.json"),
            devs_dir=str(devs_dir),
        )

    assert (data_dir / "devs.json").exists()
    data = json.loads((data_dir / "devs.json").read_text())
    assert len(data['devs']) == 1
    assert data['devs'][0]['name'] == 'Test Dev'
    assert data['devs'][0]['slug'] == 'test-dev'
    assert data['devs'][0]['url'] == 'https://testdev.com'


def test_generates_profile_markdown(tmp_path):
    data_dir = tmp_path / "docs" / "_data"
    devs_dir = tmp_path / "docs" / "devs"

    with patch('news.FEATURED_DEVS', MOCK_DEVS):
        generate_dev_profiles(
            data_path=str(data_dir / "devs.json"),
            devs_dir=str(devs_dir),
        )

    md_file = devs_dir / "test-dev.md"
    assert md_file.exists()
    content = md_file.read_text()
    assert 'layout: dev' in content
    assert 'permalink: /devs/test-dev/' in content
    assert 'dev_name: "Test Dev"' in content
    assert 'dev_url: https://testdev.com' in content
    assert 'dev_source_name: "Test Dev Blog"' in content
