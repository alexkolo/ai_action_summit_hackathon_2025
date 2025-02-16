from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Comprehensive Document Summary API", version="1.0.0")

# Register API endpoints
app.include_router(endpoints.router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
