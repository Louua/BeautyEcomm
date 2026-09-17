import os
import pandas as pd
from typing import Dict, Union
from pathlib import Path
import logging

from src.config import RAW_FILES

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_all_data(base_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    """
    Loads all raw CSV files into a dictionary of pandas DataFrames.

    Args:
        base_path (Union[str, Path]): The directory path containing the raw CSV files.

    Returns:
        Dict[str, pd.DataFrame]: A dictionary where keys are file names (without extension)
                                 and values are the corresponding DataFrames.

    Raises:
        FileNotFoundError: If the base_path does not exist or if a critical CSV file is missing.
    """
    base_path = Path(base_path)
    
    if not base_path.exists():
        logger.error(f"Data directory not found: {base_path}")
        raise FileNotFoundError(f"Directory {base_path} does not exist.")
        
    data_dict = {}
    
    for file_name in RAW_FILES:
        file_path = base_path / file_name
        name_key = file_path.stem  # Get filename without extension
        
        try:
            logger.info(f"Loading {file_name}...")
            # We assume CSVs are comma-separated. Adjust if needed.
            df = pd.read_csv(file_path)
            data_dict[name_key] = df
            logger.info(f"Successfully loaded {file_name} with shape {df.shape}")
        except FileNotFoundError:
            logger.error(f"Missing file: {file_path}")
            raise FileNotFoundError(f"Required file {file_name} is missing in {base_path}.")
        except pd.errors.EmptyDataError:
            logger.warning(f"File {file_name} is empty.")
            data_dict[name_key] = pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading {file_name}: {str(e)}")
            raise
            
    return data_dict

if __name__ == "__main__":
    # Quick test if run directly
    from src.config import RAW_DATA_DIR
    try:
        data = load_all_data(RAW_DATA_DIR)
        print(f"Loaded {len(data)} datasets successfully.")
    except Exception as e:
        print(f"Failed to load data: {e}")
