from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.routes.users import router as user_router
from app.routes.auth import router as auth_router
from app.models.record import Record
from app.routes.records import router as record_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(record_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
