from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import interactions, chat

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM - HCP Module",
    description="AI-powered CRM for managing Healthcare Professional interactions",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://0.0.0.0:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(interactions.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "name": "AI-First CRM - HCP Module",
        "version": "1.0.0",
        "endpoints": {
            "hcps": "/api/hcps",
            "interactions": "/api/interactions",
            "chat": "/api/chat",
            "follow_ups": "/api/follow-ups",
            "docs": "/docs",
        }
    }
