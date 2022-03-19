from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.vote_schema import VoteSchema
from src.oauth2 import get_current_user
from src.models import Vote, Post

router = APIRouter(
    tags=['Vote'],
    prefix='/votes'
)

@router.post('',status_code=status.HTTP_201_CREATED)
async def vote(vote:VoteSchema, db:Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == user.id)
    vote_exists = vote_query.first()
    if vote.dir == 1:
        if  vote_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You cannot vote twice")
        new_vote = Vote(post_id=vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'Successfully upvoted'}
    else:
        if not vote_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_200_OK)

