from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post_router, user_router, auth_router, vote_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(vote_router.router)


 
@app.get('/')
def root():
    return {'message':'Hello from root'}