from fastapi import FastAPI

from app.database import Base, engine
from app.models.record import Record
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.records import router as record_router
from app.routes.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(record_router)


@app.get("/")
def root():
    return {"message": "Backend is running"}
