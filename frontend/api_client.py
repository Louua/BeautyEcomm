import os
import requests
from typing import Dict, Any, Tuple

# URL from environment variable, default to local FastAPI server
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def get_health() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/v1/health")
        if response.status_code == 200:
            return response.json().get("success", False)
        return False
    except Exception:
        return False

def predict_segment(recency: float, frequency: float, monetary: float) -> Tuple[bool, Dict[str, Any]]:
    payload = {
        "recency": recency,
        "frequency": frequency,
        "monetary": monetary
    }
    try:
        response = requests.post(f"{API_BASE_URL}/v1/predict/segment", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return True, data["data"]
            return False, {"error": "API returned success=False"}
        else:
            return False, {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return False, {"error": str(e)}

def predict_forecast(weeks: int) -> Tuple[bool, Dict[str, Any]]:
    try:
        response = requests.get(f"{API_BASE_URL}/v1/predict/forecast", params={"weeks": weeks})
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return True, data["data"]
            return False, {"error": "API returned success=False"}
        else:
            return False, {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return False, {"error": str(e)}
