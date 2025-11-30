from dotenv import load_dotenv
import os

load_dotenv()  # FIRST

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app = FastAPI(title="AI-Assisted Document Authoring Platform")  # FIRST

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


from .database import Base, engine            # AFTER MIDDLEWARE
from .routers import auth_router, projects_router, export_router

Base.metadata.create_all(bind=engine)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(export_router.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
