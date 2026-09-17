import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the orders DataFrame by handling duplicates, parsing dates,
    and handling invalid values (e.g., negative prices or unexpected statuses).

    Args:
        df (pd.DataFrame): The raw orders DataFrame.

    Returns:
        pd.DataFrame: The cleaned orders DataFrame.
    """
    logger.info("Starting orders data cleaning...")
    
    # 1. Copy to avoid SettingWithCopyWarning
    df_clean = df.copy()
    
    # 2. Remove duplicates
    initial_shape = df_clean.shape
    df_clean = df_clean.drop_duplicates()
    logger.info(f"Dropped {initial_shape[0] - df_clean.shape[0]} duplicate rows.")
    
    # 3. Convert date columns to datetime
    date_cols = ['order_purchase_ts', 'order_delivered_ts', 'order_estimated_delivery']
    for col in date_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            
    # 4. Filter negative values for financial columns if they exist
    financial_cols = ['order_value', 'freight_value']
    for col in financial_cols:
        if col in df_clean.columns:
            invalid_count = (df_clean[col] < 0).sum()
            if invalid_count > 0:
                logger.warning(f"Found {invalid_count} negative values in {col}. Filtering them out.")
                df_clean = df_clean[df_clean[col] >= 0]
                
    # 5. Clean up statuses (optional: depending on business logic, we might keep only 'delivered')
    # For now, we ensure it's uppercase/lowercase standardized and not null.
    if 'order_status' in df_clean.columns:
        df_clean['order_status'] = df_clean['order_status'].str.lower().str.strip()
        
    logger.info("Orders data cleaning completed.")
    return df_clean
