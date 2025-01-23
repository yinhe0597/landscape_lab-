from fastapi import FastAPI
from database import Base, engine
from routers import user

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Landscape Lab API"}
