"""DOF Chat - RAG system for Official Gazette document queries."""

# Load environment variables first to ensure AirClerk finds them
from dotenv import load_dotenv
load_dotenv()

import air
import airclerk
from routers import web, api
import logging
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Air application
app = air.Air()



# Add session middleware using settings
app.add_middleware(
    air.SessionMiddleware,
    secret_key=settings.session_secret_key,
)


# Include routers
app.include_router(web.router)
app.include_router(airclerk.router)
app.include_router(api.router)



@app.get("/health")
async def root_health():
    """Root health check endpoint."""
    return {"status": "ok", "service": "dof-chat"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DOF Chat application...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
