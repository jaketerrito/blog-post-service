from beanie import PydanticObjectId

from tests.conftest import AUTHOR_ID


def test_create_blog_post(client):
    response = client.put(
        "/blog-post",
        params={"user_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    assert PydanticObjectId.is_valid(response.json())
