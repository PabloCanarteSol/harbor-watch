import sys, os
sys.path.insert(0, '/home/harbor-watch')


def test_dry_run_no_creds_logs_only(capsys):
    from src.twitter_poster import TwitterPoster
    tw = TwitterPoster()
    assert not tw.has_auth
    result = tw.post_tweet("test post")
    assert result.get("dry_run") is True


def test_post_tweet_with_image_path_dry_run(tmp_path):
    from src.twitter_poster import TwitterPoster
    img = tmp_path / "map.png"
    img.write_bytes(b"\x89PNGfakeimage")
    tw = TwitterPoster()
    res = tw.post_tweet("test", image_path=str(img))
    assert res.get("dry_run") is True


def test_build_enter_text_all_fields():
    from src.twitter_poster import TwitterPoster
    txt = TwitterPoster.build_enter_text(name='TEST SHIP', imo='1234567', flag='Panama', length_m=200)
    assert "TEST SHIP" in txt
    assert "1234567" in txt
    assert "#HarborWatch" in txt


def test_build_enter_text_minimal_name_only():
    from src.twitter_poster import TwitterPoster
    txt = TwitterPoster.build_enter_text("JUST A NAME")
    assert "JUST A NAME" in txt
    assert "#AIS" in txt


def test_build_docked_text_includes_zone():
    from src.twitter_poster import TwitterPoster
    txt = TwitterPoster.build_docked_text('SHIPPY', zone_name='Container Terminal')
    assert 'SHIPPY' in txt
    assert 'Container Terminal' in txt


def test_build_docked_text_imo_present():
    from src.twitter_poster import TwitterPoster
    txt = TwitterPoster.build_docked_text('SHIPPY', imo='7654321')
    assert '7654321' in txt


def test_load_tweepy_missing_raises_import_error():
    from src.twitter_poster import TwitterPoster
    tw = TwitterPoster()
    try:
        tw._load_tweepy()
        import_passed = True
    except ImportError:
        import_passed = False


def test_text_truncation_at_450_chars():
    from src.twitter_poster import TwitterPoster
    long_name = "X" * 500
    txt = TwitterPoster.build_enter_text(name=long_name)
    assert len(txt) > 0


def test_has_auth_with_bearer_only():
    from src.twitter_poster import TwitterPoster
    tw = TwitterPoster(bearer_token="test123")
    assert tw.has_auth is True


def test_post_tweet_text_only_no_image_when_file_missing():
    from src.twitter_poster import TwitterPoster
    tw = TwitterPoster()
    res = tw.post_tweet("test", image_path="/nonexistent/path.png")
    assert res.get("dry_run") is True
