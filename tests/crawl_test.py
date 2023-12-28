import pytest

from app.crawl import get_last_url_segment


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://example.com/path/to/resource", "resource"),
        ("https://example.com/path/to/resource/", "resource"),
        ("https://example.com", "root"),
        ("https://", "root"),
        ("https://example.com/path/to/some/very/deep/resource", "resource"),
        ("https://example.com/path/to/resource?query=param", "resource"),
        ("https://example.com/path/to/resource#anchor", "resource"),
        ("https://example.com/", "root"),
    ],
)
def test_get_last_url_segment(url, expected):
    assert get_last_url_segment(url) == expected
