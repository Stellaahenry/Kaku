import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.controllers.puzzle_controller import router as puzzle_router

load_dotenv()

app = FastAPI(title="Kaku API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(puzzle_router)
