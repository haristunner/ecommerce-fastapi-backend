from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.connection import Base, engine

from app.routes import api_router

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(e)


app = FastAPI(
    title="E-Commerce API",
)

app.include_router(api_router)

# Add CORS middleware
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "E-Commerce Backend Running Successfully"}


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"message": "DB connected!"}
