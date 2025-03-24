# AUTHOR_ID = "test_author_id"
# USER_ID = "test_user_id"


# def test_integration(client):
#     response = client.get(
#         "/create_blog_post",
#         params={"user_id": AUTHOR_ID},
#     )
#     blog_post_id = response.json()

#     # Test author access
#     response = client.get(
#         "/get_blog_post",
#         params={"blog_post_id": blog_post_id, "user_id": AUTHOR_ID},
#     )
#     assert response.status_code == 200
#     assert response.json()["_id"] == id

#     # Test other user access to public post
#     response = client.get(
#         "/get_blog_post",
#         params={"blog_post_id": id, "user_id": USER_ID},
#     )
#     assert response.status_code == 200
#     assert response.json()["_id"] == id


# def test_exists_not_public(client, blog_post):
#     # Make the blog post private
#     # blog_post.public = False
#     # await blog_post.save()

#     # Test author access to private post
#     response = client.get(
#         "/get_blog_post",
#         params={"blog_post_id": str(BLOG_POST_ID), "user_id": AUTHOR_ID},
#     )
#     assert response.status_code == 200
#     assert response.json()["_id"] == str(BLOG_POST_ID)

#     # Test other user access to private post - should get 403
#     response = client.get(
#         "/get_blog_post",
#         params={"blog_post_id": str(BLOG_POST_ID), "user_id": USER_ID},
#     )
#     assert response.status_code == 403
#     assert "Not authorized" in response.json()["detail"]


# def test_not_exist(client):
#     non_existent_id = PydanticObjectId()

#     response = client.get(
#         "/get_blog_post",
#         params={"blog_post_id": str(non_existent_id), "user_id": USER_ID},
#     )

#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]
