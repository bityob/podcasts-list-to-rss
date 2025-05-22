from requests import Session

from db import RssFeed

session = Session()


class Cache:
    @classmethod
    def _get_rss_feed_by_podcast_id(cls, podcast_id: str) -> str:
        json_data = {
            "uuids": podcast_id,
        }

        response = session.post("https://refresh.pocketcasts.com/import/export_feed_urls", json=json_data)

        response.raise_for_status()

        return response.json()["result"][podcast_id]

    @classmethod
    def get_rss_feed_by_podcast_id(cls, podcast_id, podcast_name_func):
        rss_feed = cls._get_rss_feed_by_podcast_id(podcast_id)
        RssFeed.get_or_create(
            **dict(
                podcast_id=podcast_id,
                rss_feed=rss_feed,
                podcast_name=podcast_name_func(),
            ),
        )
        return rss_feed
