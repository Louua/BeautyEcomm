import time
from fastapi import APIRouter
from src.api.schemas import StandardResponse

router = APIRouter(tags=["Health"])

@router.get("/v1/health", response_model=StandardResponse)
def health_check():
    start_time = time.perf_counter()
    # Simulating simple health check logic
    execution_time_ms = (time.perf_counter() - start_time) * 1000
    
    return StandardResponse.success_response(
        data={"status": "ok", "message": "Beauty E-commerce ML API is healthy."},
        execution_time_ms=execution_time_ms
    )
