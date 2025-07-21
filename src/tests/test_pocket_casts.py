import pytest


@pytest.mark.parametrize("url, expected_match", [
    (
        "https://pocketcasts.com/podcasts/02f40f60-527e-0134-ec21-0d50f522381b/158aeb67-e8d7-4b51-b26c-f2e9bf87a720",
        ("02f40f60-527e-0134-ec21-0d50f522381b", "158aeb67-e8d7-4b51-b26c-f2e9bf87a720")
    ),
    (
            "https://play.pocketcasts.com/podcasts/02f40f60-527e-0134-ec21-0d50f522381b/158aeb67-e8d7-4b51-b26c-f2e9bf87a720",
            ("02f40f60-527e-0134-ec21-0d50f522381b", "158aeb67-e8d7-4b51-b26c-f2e9bf87a720")
    )
])
def test_get_podcast_id_from_response_url(url, expected_match):
    from src.pocket_casts import PocketCasts

    result = PocketCasts.get_podcast_id_from_response_url(url)
    assert result == expected_match, f"Expected {expected_match}, but got {result}"