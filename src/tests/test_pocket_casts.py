import pytest


@pytest.mark.parametrize(
    "url, expected_match",
    [
        (
            "https://pocketcasts.com/podcasts/02f40f60-527e-0134-ec21-0d50f522381b/158aeb67-e8d7-4b51-b26c-f2e9bf87a720",
            ("02f40f60-527e-0134-ec21-0d50f522381b", "158aeb67-e8d7-4b51-b26c-f2e9bf87a720"),
        ),
        (
            "https://play.pocketcasts.com/podcasts/02f40f60-527e-0134-ec21-0d50f522381b/158aeb67-e8d7-4b51-b26c-f2e9bf87a720",
            ("02f40f60-527e-0134-ec21-0d50f522381b", "158aeb67-e8d7-4b51-b26c-f2e9bf87a720"),
        ),
        (
            "https://pocketcasts.com/podcast/%D7%A2%D7%95%D7%A9%D7%99%D7%9D-%D7%AA%D7%A0%D7%9A-%D7%A2%D7%9D-%D7%99%D7%95%D7%AA%D7%9D-%D7%A9%D7%98%D7%99%D7%99%D7%A0%D7%9E%D7%9F-osim-tanach/7575bbb0-bb00-0134-10a8-25324e2a541d/%D7%96%D7%99%D7%9B%D7%A8%D7%95%D7%9F-%D7%AA%D7%A8%D7%95%D7%A2%D7%94-%D7%A0%D7%96%D7%9B%D7%A8%D7%99%D7%9D-%D7%91%D7%A8%D7%90%D7%A9-%D7%94%D7%A9%D7%A0%D7%94-%D7%A9%D7%97%D7%A8-%D7%A2%D7%A0%D7%91%D7%A8-%D7%A2%D7%95%D7%A9%D7%99%D7%9D-%D7%AA%D7%A0%D7%9A/24133df2-78c3-4acb-883f-805a402bc5d6",
            ("7575bbb0-bb00-0134-10a8-25324e2a541d", "24133df2-78c3-4acb-883f-805a402bc5d6"),
        ),
    ],
)
def test_get_podcast_id_from_response_url(url, expected_match):
    from src.pocket_casts import PocketCasts

    result = PocketCasts.get_podcast_id_from_response_url(url)
    assert result == expected_match, f"Expected {expected_match}, but got {result}"
