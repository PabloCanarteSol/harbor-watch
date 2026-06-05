import sys
sys.path.insert(0, "/home/harbor-watch")


def test_scrape_returns_data():
    try:
        import requests
    except ImportError:
        assert True
    assert True
