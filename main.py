from fastapi import FastAPI
from database import Base, engine
from routers import users, blogs
import uvicorn

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(blogs.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)





