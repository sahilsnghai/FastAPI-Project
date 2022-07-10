from fastapi import HTTPException, status, Depends, APIRouter, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schemas.PostOut])
# @router.get('/')
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()

    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # print(search)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    result = db.query(
        models.Post,func.count(models.Vote.post_id).label("Likes")).join(
            models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(
                models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result)
    # print(posts)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # posts = new_post.dict()
    # # posts['id'] = randrange(0, 100000)
    # # my_posts.append(posts)
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
    #             (new_post.title, new_post.content, new_post.published))
    # new_posts = cur.fetchone()
    # conn.commit()
    print(current_user.email)
    new_posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    print(current_user.email)
    # posts = db.query(models.Post).filter(models.Post.id == id).first()

    posts =db.query(
        models.Post,func.count(models.Vote.post_id).label("Likes")).join(
            models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With id {id} NOT FOUND.")
    # if posts.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authenticated to perfrom requested task")

    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM  posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    delete = deleted_post.first()
    if delete == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Post with id: {id} Not exist.")

    if delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authenticated to perfrom requested task")
    deleted_post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def upd_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id =%s returning *""",
    #             (post.title, post.content, post.published, str(id)))
    # update_post = cur.fetchone()
    # conn.commit()
    post_qury = db.query(models.Post).filter(models.Post.id == id)
    post_new = post_qury.first()
    if post_new == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} Not exist.")
    if post_new.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authenticated to perfrom requested task")

    post_qury.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_qury.first()
