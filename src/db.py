from peewee import (
    SQL,
    CharField,
    CompositeKey,
    Database,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
    TextField,
    UUIDField,
)

from src.settings import DB_URL


def get_db() -> Database:
    if DB_URL.startswith("postgresql://"):
        return PostgresqlDatabase(DB_URL, autocommit=True, autorollback=True)  # pragma: no cover
    return SqliteDatabase(DB_URL)


db = get_db()


class RssFeed(Model):
    """
    Mapping between podcast_id and rss_feed
    """

    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    podcast_id = UUIDField(primary_key=True)
    rss_feed = CharField()
    podcast_name = TextField()

    class Meta:  # noqa
        database = db  # noqa
        table_name = "rss_feeds"  # noqa


class Episode(Model):
    """
    Mapping between episode_id and podcast_id
    """

    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    episode_id = UUIDField(primary_key=True)
    podcast = ForeignKeyField(RssFeed, backref="episodes")
    episode_name = TextField()

    class Meta:  # noqa
        database = db  # noqa
        table_name = "episodes"  # noqa


class MessageLink(Model):
    """
    Episodes links from messages; an episode can be linked to multiple messages
    """

    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    message_id = IntegerField()
    link = CharField()
    episode = ForeignKeyField(Episode, backref="message_links")
    rss_item = TextField(null=True)
    message_url = CharField(null=True)

    class Meta:  # noqa
        database = db  # noqa
        table_name = "message_links"  # noqa
        primary_key = CompositeKey("message_id", "link")


class Error(Model):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    message_id = IntegerField()
    link = CharField()
    exception_type = CharField()
    exception_message = TextField()
    exception_traceback = TextField()

    class Meta:  # noqa
        database = db  # noqa
        table_name = "errors"  # noqa
        primary_key = CompositeKey("message_id", "link")


message_ids_cache = None


def get_message_object_from_cache(message_id, link):
    global message_ids_cache

    if message_ids_cache is None:
        message_ids_cache = {
            (m.message_id, m.link): m
            for m in (
                MessageLink.select(MessageLink, Episode, RssFeed)
                .join(Episode)
                .join(RssFeed)
                .where((MessageLink.episode_id == Episode.episode_id) & (Episode.podcast_id == RssFeed.podcast_id))
            )
        }

    return message_ids_cache.get((message_id, link))


error_cache = None


def get_error_object_from_cache(message_id, link):
    global error_cache

    if error_cache is None:
        error_cache = {(m.message_id, m.link): m for m in Error.select()}

    return error_cache.get((message_id, link))


# db.create_tables([RssFeed, Episode, MessageLink, Error])
