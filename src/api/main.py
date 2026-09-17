from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from src.api.routers import health, segmentation, forecasting
from src.api.dependencies import load_models

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Beauty E-commerce ML API",
    description="API for customer segmentation and sales forecasting.",
    version="1.0.0"
)

# CORS middleware for potential frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up API and loading models...")
    load_models()

# Include routers
app.include_router(health.router)
app.include_router(segmentation.router)
app.include_router(forecasting.router)

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
