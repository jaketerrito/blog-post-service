from beanie import PydanticObjectId
from fastapi import status

from tests.conftest import AUTHOR_ID


def test_create_blog_post(client):
    response = client.put(
        "/blog-post",
        headers={"user-id": AUTHOR_ID},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert PydanticObjectId.is_valid(response.json())
