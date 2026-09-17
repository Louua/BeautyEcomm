import time
from fastapi import APIRouter, HTTPException, Query
from typing import List
import numpy as np

from src.api.schemas import ForecastData, StandardResponse
from src.api.dependencies import get_sarima_model

router = APIRouter(
    prefix="/v1/predict/forecast",
    tags=["Forecasting"]
)

@router.get("", response_model=StandardResponse)
@router.get("/", response_model=StandardResponse, include_in_schema=False)
def predict_forecast(weeks: int = Query(4, description="Number of weeks to forecast", gt=0, le=52)):
    start_time = time.perf_counter()
    try:
        model = get_sarima_model()
        if model is None:
            raise HTTPException(status_code=500, detail="SARIMA model not loaded.")
        
        # Inference
        forecast_res = model.get_forecast(steps=weeks)
        forecast_values = forecast_res.predicted_mean.tolist()
        ci = forecast_res.conf_int()
        if isinstance(ci, np.ndarray):
            lower_bound = ci[:, 0].tolist()
            upper_bound = ci[:, 1].tolist()
        else:
            lower_bound = ci.iloc[:, 0].tolist()
            upper_bound = ci.iloc[:, 1].tolist()
        
        forecast_data = ForecastData(
            forecast=forecast_values,
            lower_bound=lower_bound,
            upper_bound=upper_bound
        )
        
        execution_time_ms = (time.perf_counter() - start_time) * 1000
        return StandardResponse.success_response(
            data=forecast_data,
            execution_time_ms=execution_time_ms
        )
    except Exception as e:
        execution_time_ms = (time.perf_counter() - start_time) * 1000
        return StandardResponse.error_response(
            error_details=str(e),
            execution_time_ms=execution_time_ms
        )
