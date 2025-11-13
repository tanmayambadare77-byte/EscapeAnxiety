from fastapi import FastAPI
from .database import engine, Base
from .routers import users, activities, content, games, ml
from . import models

app = FastAPI(title="Escape Anxiety Backend")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(activities.router)
app.include_router(content.router)
app.include_router(games.router)
app.include_router(ml.router)


@app.get("/")
def root():
    return {"message": "Escape Anxiety API — running"}
