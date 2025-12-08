import air
from fastapi import FastAPI
from routers import web, api
from utils.logger import logger
from config import settings

# Initialize Air application for web routes
app = air.Air()

# Create a separate FastAPI app for API routes to ensure proper JSON serialization
fastapi_app = FastAPI()
fastapi_app.include_router(api.router)

# Startup event to pre-initialize RAG service on FastAPI app
@fastapi_app.on_event("startup")
async def startup_event():
    """Initialize RAG service during application startup."""
    logger.info("Starting DOF Chat application...")
    try:
        from rag_service import rag_service
        rag_service.initialize()
        logger.info("RAG service pre-initialized")
    except Exception as e:
        logger.error(f"Failed to pre-initialize RAG service: {e}")

# Mount static files directory first to avoid routing conflicts
app.mount("/static", air.StaticFiles(directory="static"), name="static")

# Mount the API app under /api
app.mount("/api", fastapi_app)

# Add session middleware with secure configuration
app.add_middleware(air.SessionMiddleware, secret_key=settings.session_secret_key)

# Include web routers in Air app
app.include_router(web.router)


# TODO: Authentication system implementation pending

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DOF Chat application")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
