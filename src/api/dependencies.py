import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Cache models
_models = {}

def load_models():
    """Load models at startup to avoid reloading them on each request."""
    models_dir = Path(__file__).resolve().parent.parent.parent / "models"
    
    try:
        logger.info("Loading scaler...")
        _models["scaler"] = joblib.load(models_dir / "scaler.pkl")
    except Exception as e:
        logger.error(f"Failed to load scaler: {e}")
        
    try:
        logger.info("Loading kmeans model...")
        _models["kmeans"] = joblib.load(models_dir / "kmeans_model.pkl")
    except Exception as e:
        logger.error(f"Failed to load kmeans model: {e}")
        
    try:
        logger.info("Loading sarima model...")
        _models["sarima"] = joblib.load(models_dir / "sarima_model.pkl")
    except Exception as e:
        logger.error(f"Failed to load sarima model: {e}")

def get_scaler():
    return _models.get("scaler")

def get_kmeans_model():
    return _models.get("kmeans")

def get_sarima_model():
    return _models.get("sarima")
