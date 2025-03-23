import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BlogPost(BaseModel):
    id: str
    author_id: str
    public: bool
    created_at: datetime
    updated_at: datetime
    content: str


example = BlogPost(
    id="123",
    author_id="123",
    public=True,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    content="Hello World",
)


@app.get("/get_blog_post/{blog_post_id}")
async def get_blog_post(blog_post_id: str) -> BlogPost:
    return example


@app.post("/create_blog_post")
async def create_blog_post(blog_post: BlogPost):
    return "Success"


class UpdateBlogPostContent(BaseModel):
    id: str
    author_id: str
    content: str


@app.patch("/update_blog_post/content")
def update_blog_post_content(params: UpdateBlogPostContent):
    return "Success"


class UpdateBlogPostPublic(BaseModel):
    id: str
    author_id: str
    public: bool


@app.patch("/update_blog_post/public")
def update_blog_post_public(params: UpdateBlogPostPublic):
    return "Success"


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
