from src.api.dependencies import load_models, get_sarima_model

load_models()
model = get_sarima_model()

try:
    forecast_res = model.get_forecast(steps=4)
    forecast_values = forecast_res.predicted_mean.tolist()
    ci = forecast_res.conf_int()
    print("Forecast mean:", forecast_values)
    print("Conf int columns:", ci.columns)
    lower_bound = ci.iloc[:, 0].tolist()
    upper_bound = ci.iloc[:, 1].tolist()
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
