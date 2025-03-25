from datetime import UTC, datetime

import pymongo
from beanie import Document
from pymongo import IndexModel


class BlogPost(Document):
    author_id: str
    public: bool = False
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)
    title: str | None = None
    content: str | None = None

    class Settings:
        indexes = [
            IndexModel(
                [
                    ("author_id"),
                    ("public"),
                    ("created_at", pymongo.DESCENDING),
                ],
                name="author_public_created_at_index",
            ),
            IndexModel(
                [
                    ("author_id"),
                    ("created_at", pymongo.DESCENDING),
                ],
                name="author_created_at_index",
            ),
        ]
