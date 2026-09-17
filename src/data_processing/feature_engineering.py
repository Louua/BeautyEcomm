import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def add_temporal_features(df: pd.DataFrame, date_col: str = 'order_purchase_ts') -> pd.DataFrame:
    """
    Extracts temporal features from a datetime column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        date_col (str): The name of the datetime column.

    Returns:
        pd.DataFrame: The DataFrame with new temporal columns (year, month, week, day_of_week, is_weekend, quarter).
    """
    if date_col not in df.columns:
        logger.error(f"Column {date_col} not found in DataFrame.")
        raise ValueError(f"Column {date_col} is required for temporal features.")
        
    df = df.copy()
    
    logger.info(f"Adding temporal features based on {date_col}...")
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['week'] = df[date_col].dt.isocalendar().week
    df['day_of_week'] = df[date_col].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['quarter'] = df[date_col].dt.quarter
    
    return df

def add_delivery_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates delivery-related features (delivery_days, is_late).

    Args:
        df (pd.DataFrame): The input DataFrame containing delivery dates.

    Returns:
        pd.DataFrame: The DataFrame with delivery features.
    """
    df = df.copy()
    
    logger.info("Adding delivery features...")
    # Calculate delivery days (from purchase to delivery)
    if 'order_delivered_ts' in df.columns and 'order_purchase_ts' in df.columns:
        df['delivery_days'] = (df['order_delivered_ts'] - df['order_purchase_ts']).dt.days
    else:
        logger.warning("Required date columns for delivery_days are missing.")
        
    # Check if late
    if 'order_delivered_ts' in df.columns and 'order_estimated_delivery' in df.columns:
        df['is_late'] = (df['order_delivered_ts'] > df['order_estimated_delivery']).astype(int)
    else:
        logger.warning("Required date columns for is_late are missing.")
        
    return df

def build_rfm(df: pd.DataFrame, current_date: pd.Timestamp = None) -> pd.DataFrame:
    """
    Builds Recency, Frequency, and Monetary (RFM) metrics per customer.

    Args:
        df (pd.DataFrame): The input DataFrame containing 'customer_unique_id', 'order_purchase_ts', and 'order_value'.
        current_date (pd.Timestamp, optional): The reference date for calculating Recency. 
                                               If None, uses the max date in the dataset + 1 day.

    Returns:
        pd.DataFrame: A DataFrame with RFM metrics indexed by customer_unique_id.
    """
    logger.info("Building RFM metrics...")
    req_cols = ['customer_unique_id', 'order_purchase_ts', 'order_value']
    for col in req_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    if current_date is None:
        current_date = df['order_purchase_ts'].max() + pd.Timedelta(days=1)
        
    rfm = df.groupby('customer_unique_id').agg(
        recency=('order_purchase_ts', lambda x: (current_date - x.max()).days),
        frequency=('order_purchase_ts', 'count'),
        monetary=('order_value', 'sum')
    ).reset_index()
    
    logger.info("RFM metrics built successfully.")
    return rfm
