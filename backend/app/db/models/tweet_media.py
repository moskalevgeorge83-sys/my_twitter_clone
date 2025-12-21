"""Many-to-many таблица связи твитов и медиафайлов."""

from sqlalchemy import Column, ForeignKey, Integer, Table

from ..base import Base

tweet_media_table: Table = Table(
    "tweet_media",
    Base.metadata,
    Column(
        "tweet_id",
        Integer,
        ForeignKey("tweets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "media_id",
        Integer,
        ForeignKey("medias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
