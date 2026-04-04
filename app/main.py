from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is running"}