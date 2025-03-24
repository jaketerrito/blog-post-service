from datetime import UTC, datetime

import pymongo
from beanie import Document
from pymongo import IndexModel


class BlogPost(Document):
    author_id: str
    public: bool
    title: str
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)
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
        ]
