from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, task
from app.routes import auth, tasks

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

app.include_router(tasks.router)

@app.get("/")
def root():
 return{"message":"Task Manager Api running"}


