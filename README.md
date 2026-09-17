# Beauty E-commerce Analytics

## Project Overview
This project transforms raw data from a cosmetics e-commerce platform into actionable business insights. It encompasses data processing, RFM customer segmentation, K-Means clustering, and sales forecasting using SARIMA.

##  Dataset
The dataset originates from the **Beauty Commerce Dataset II (Kaggle)** and contains 13 relational CSV files covering customers, products, orders, marketing, and inventory.

## Project Structure
- `data/` - Raw, processed, and exported data
- `notebooks/` - Jupyter notebooks for exploratory analysis and visualization
- `src/` - Modularized Python code for data processing, segmentation, and forecasting
- `sql/` - PostgreSQL schema and analytics queries
- `tests/` - Unit tests
- `powerbi/` - Dashboard documentation

## Setup & Execution
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Generate dummy models for API (optional): `python src/models/train_and_save.py`
4. Place raw CSV files in `data/raw/`
5. Run the notebooks or modular scripts to reproduce the analysis.

##  FastAPI Service
To run the API server locally:
```bash
uvicorn src.api.main:app --reload
```

### Endpoints
- `GET /v1/health` : Healthcheck
- `POST /v1/predict/segment` : Predict customer segment from RFM features
- `GET /v1/predict/forecast?weeks=N` : Forecast sales for the next N weeks

Documentation (Swagger) is available at `http://localhost:8000/docs` when the server is running.

##  Streamlit Frontend
To run the interactive web application locally:
```bash
streamlit run frontend/app.py
```
By default, the frontend will connect to `http://localhost:8000`. You can configure this via the `API_URL` environment variable.

##  Deployment

### 1. API on Render
The project includes a `render.yaml` and a `Dockerfile`. 
1. Create an account on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Render will automatically detect the `render.yaml` Blueprint and deploy the Web Service.
4. Note the public URL provided by Render (e.g., `https://beauty-ecom-api.onrender.com`).

### 2. Frontend on Streamlit Cloud
1. Create an account on [Streamlit Community Cloud](https://streamlit.io/cloud).
2. Connect your GitHub repository.
3. Deploy a new app and set the **Main file path** to `frontend/app.py`.
4. In the app settings (Advanced settings -> Secrets), add the `API_URL` variable pointing to your Render API URL:
   ```toml
   API_URL = "https://beauty-ecom-api.onrender.com"
   ```
