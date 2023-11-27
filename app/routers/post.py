from itertools import count
from pyexpat import model
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
import sqlalchemy
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

#from typing_extensions import deprecated
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # if cur is None:
    #     print("cur is None")
    # cur.execute("SELECT * FROM posts ")
    # posts = cur.fetchall()
    #print(search)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
            
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # if cur is None:
    #     print("cur is None")
    # cur.execute("INSERT INTO posts (title, content, published) VALUEs (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    # if conn is None:
    #     print("conn is None")
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # if cur is None:
    #     print("cur is None")
    # cur.execute("SELECT * FROM posts WHERE id = %s ", (id,))
    # post = cur.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # if cur is None:
    #     print("cur is None")
    # cur.execute("DELETE FROM posts WHERE id = %s RETURNING * ", (id,))
    # deleted_post = cur.fetchone()
    # conn.commit()
    # if conn is None:
    #     print("conn is None")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
        
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # if cur is None:
    #     print("cur is None")
    # cur.execute("UPDATE posts SET title = %s, content=%s,  published = %s WHERE id = %s  RETURNING * ", (post.title, post.content, post.published, (id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    # if conn is None:
    #     print("conn is None")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")
    
    
    #post_query.update(updated_post.model_dump(), synchronize_session=False)
    post_query.update({key: value for key, value in updated_post.model_dump().items() if hasattr(models.Post, key)}, synchronize_session=False)
    db.commit()
    #print(post_query)
    return post_query.first()

