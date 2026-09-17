import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"

# Random state for reproducibility
RANDOM_STATE = 42

# List of all expected raw CSV files
RAW_FILES = [
    "customers.csv",
    "brands.csv",
    "products.csv",
    "warehouses.csv",
    "geolocation.csv",
    "orders.csv",
    "order_items.csv",
    "order_payments.csv",
    "order_reviews.csv",
    "inventory_snapshots.csv",
    "purchase_orders.csv",
    "marketing_campaigns.csv",
    "marketing_performance.csv"
]
