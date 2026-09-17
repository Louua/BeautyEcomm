from src.api.main import app
from fastapi.testclient import TestClient
import json

with TestClient(app) as client:
    response = client.get("/v1/predict/forecast?weeks=4")
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
