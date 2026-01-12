from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import properties

settings = get_settings()

app = FastAPI(
    title="Real Estate API",
    description="A FastAPI wrapper for HomeHarvest - scrape real estate data from Realtor.com",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(properties.router)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "realstate-api"}


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Real Estate API",
        "version": "1.0.0",
        "description": "A FastAPI wrapper for HomeHarvest",
        "docs": "/docs",
        "health": "/health",
    }
