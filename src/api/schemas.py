from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone

class CustomerData(BaseModel):
    recency: float = Field(..., description="Recency in days", ge=0)
    frequency: float = Field(..., description="Number of orders", ge=0)
    monetary: float = Field(..., description="Total amount spent", ge=0)

class SegmentationData(BaseModel):
    customer_id: Optional[str] = None
    cluster_id: int
    segment_name: str

class ForecastData(BaseModel):
    forecast: List[float]
    lower_bound: Optional[List[float]] = None
    upper_bound: Optional[List[float]] = None

class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    model_version: str = "1.0.0"
    execution_time_ms: float
    timestamp: str

    @classmethod
    def success_response(cls, data: Any, execution_time_ms: float):
        return cls(
            success=True,
            data=data,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    @classmethod
    def error_response(cls, error_details: Any, execution_time_ms: float = 0.0):
        return cls(
            success=False,
            data=error_details,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
