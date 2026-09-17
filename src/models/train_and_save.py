import os
import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = ROOT_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

def train_and_save_kmeans():
    print("Training dummy K-Means and Scaler...")
    # Dummy data
    X = np.random.rand(100, 3) * 1000
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(X_scaled)
    
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    joblib.dump(kmeans, MODELS_DIR / "kmeans_model.pkl")
    print("Saved kmeans_model.pkl and scaler.pkl")

def train_and_save_sarima():
    print("Training dummy SARIMA...")
    # Dummy data (random walk)
    np.random.seed(42)
    y = np.cumsum(np.random.normal(0, 1, 100))
    
    model = SARIMAX(y, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0))
    results = model.fit(disp=False)
    
    joblib.dump(results, MODELS_DIR / "sarima_model.pkl")
    print("Saved sarima_model.pkl")

if __name__ == "__main__":
    train_and_save_kmeans()
    train_and_save_sarima()
    print("All models generated and saved to models/ directory.")
