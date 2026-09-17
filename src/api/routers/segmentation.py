import time
import numpy as np
from fastapi import APIRouter, HTTPException

from src.api.schemas import CustomerData, SegmentationData, StandardResponse
from src.api.dependencies import get_kmeans_model, get_scaler

router = APIRouter(
    prefix="/v1/predict/segment",
    tags=["Segmentation"]
)

def assign_segment(cluster_id: int) -> str:
    mapping = {
        0: "Champions",
        1: "Loyal",
        2: "At Risk",
        3: "Lost",
        4: "Need Attention"
    }
    return mapping.get(cluster_id, "Unknown")

@router.post("", response_model=StandardResponse)
@router.post("/", response_model=StandardResponse, include_in_schema=False)
def predict_segment(data: CustomerData):
    start_time = time.perf_counter()
    try:
        model = get_kmeans_model()
        scaler = get_scaler()
        
        if model is None or scaler is None:
            raise HTTPException(status_code=500, detail="Model or Scaler not loaded.")
        
        # Inference
        features = scaler.transform([[data.recency, data.frequency, data.monetary]])
        cluster_id = int(model.predict(features)[0])
        
        segment_data = SegmentationData(
            cluster_id=cluster_id,
            segment_name=assign_segment(cluster_id)
        )
        
        execution_time_ms = (time.perf_counter() - start_time) * 1000
        return StandardResponse.success_response(
            data=segment_data,
            execution_time_ms=execution_time_ms
        )
    except Exception as e:
        execution_time_ms = (time.perf_counter() - start_time) * 1000
        return StandardResponse.error_response(
            error_details=str(e),
            execution_time_ms=execution_time_ms
        )
