from peewee import (
    SQL,
    CharField,
    CompositeKey,
    Database,
    DateTimeField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
    TextField,
    UUIDField,
)

from settings import DB_URL


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
    message_id = CharField()
    link = CharField()
    episode = ForeignKeyField(Episode, backref="message_links")
    rss_item = TextField(null=True)

    class Meta:  # noqa
        database = db  # noqa
        table_name = "message_links"  # noqa
        primary_key = CompositeKey("message_id", "link")


# db.create_tables([RssFeed, Episode, MessageLink])
