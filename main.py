from fastapi import FastAPI
from database import Base, engine
from api import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include API routes
app.include_router(api_router)
