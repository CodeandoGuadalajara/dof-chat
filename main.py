
import air
import airsqlmodel as sql
from routers import web, api, auth
import logging
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Air application with AirSQLModel lifespan
app = air.Air(lifespan=sql.create_async_db_lifespan(url=settings.database_url))

# Add session middleware using settings with proper cookie configuration
app.add_middleware(
    air.SessionMiddleware,
    secret_key=settings.session_secret_key,
)

# Include routers
app.include_router(web.router)
app.include_router(api.router)
app.include_router(api.auth_router)  # JSON auth endpoints

# Health check endpoint at root level
@app.get("/health")
async def root_health():
    """Root health check endpoint."""
    return {"status": "ok", "service": "dof-chat"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DOF Chat application...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
