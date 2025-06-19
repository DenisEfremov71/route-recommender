import pandas as pd
import os
from models import Store, StoreList

def load_store_data(csv_path="inputs/store_list.csv"):
    """Load store data from CSV file and return as StoreList object."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Store data file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Validate required columns
    required_columns = ['retailer', 'store_number', 'address']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in CSV: {missing_columns}")
    
    stores = []
    
    for index, row in df.iterrows():
        try:
            # Strip whitespace and ensure data types
            retailer = str(row['retailer']).strip()
            store_number = str(row['store_number']).strip()
            address = str(row['address']).strip()
            
            # Validate non-empty values
            if not retailer or not store_number or not address:
                print(f"Warning: Skipping row {index + 1} due to empty values")
                continue
                
            stores.append(Store(
                retailer=retailer,
                store_number=store_number,
                address=address
            ))
        except Exception as e:
            print(f"Warning: Error processing row {index + 1}: {e}")
            continue
    
    if not stores:
        raise ValueError("No valid store data found in CSV file")
    
    return StoreList(stores=stores)

def get_unique_retailers(store_list: StoreList):
    """Get unique retailers from store list."""
    return list(set([store.retailer for store in store_list.stores]))

def get_store_numbers_for_retailer(store_list: StoreList, retailer: str):
    """Get store numbers for a specific retailer."""
    return [store.store_number for store in store_list.stores if store.retailer == retailer]

def get_store_address(store_list: StoreList, retailer: str, store_number: str):
    """Get store address for a specific retailer and store number."""
    for store in store_list.stores:
        if store.retailer == retailer and store.store_number == store_number:
            return store.address
    return None 