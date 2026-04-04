from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.routes.users import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}