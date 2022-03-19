from posixpath import ismount
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.schemas.post_schema import PostSchema, CreatePostSchema, PostOut
from src.database import get_db
from src.models import Post,User, Vote
from src.oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[PostOut])
async def all_posts(db:Session= Depends(get_db), user:User = Depends(get_current_user), limit:int=10,
 skip:int = 0, search:Optional[str] = ""):

    posts = db.query(Post, func.count(Vote.post_id).label('votes')).join(Vote, Vote.post_id == Post.id, isouter=True)\
    .group_by(Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(post:CreatePostSchema, db:Session=Depends(get_db), user:User = Depends(get_current_user)):
    new_post = Post(**post.dict(), owner_id = user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/:id', response_model=dict[str,PostOut])
async def detail_post(id:int, db:Session=Depends(get_db), user:User = Depends(get_current_user)):
    post = db.query(Post, func.count(Vote.post_id).label('votes')).join(Vote, Vote.post_id == Post.id, isouter=True)\
    .group_by(Post.id).filter(Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    print(post)
    return {'post':post}

@router.delete('/:id')
async def delete_post(id:int, db:Session=Depends(get_db), user:User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You dont have permission to delete this post so fuck off')
  
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/:id')
async def update_post(id:int, post:CreatePostSchema, db:Session=Depends(get_db), user:User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id==id)
    found_post = post_query.first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}

