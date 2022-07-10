from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    Likes: int   
    # class Config:
    #     orm_mode = True


class Usercreate(BaseModel):
    email: EmailStr
    password: str


class Userlogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str


class tokendata(BaseModel):
    id: Optional[str] = None


class vote(BaseModel):
    post_id: int
    dir: conint(le=1)
