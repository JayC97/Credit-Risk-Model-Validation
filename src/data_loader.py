# src/data_loader.py

import os
import numpy as np
import pandas as pd

# Use relative pathing based on a clean project root structure
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/"))

def load_validation_splits():
    """
    Safely loads the serialized dataframes from disk into 
    the validation notebooks.
    """
    train_path = os.path.join(DATA_DIR, "df_train_tweaked.csv")
    val_path = os.path.join(DATA_DIR, "df_val_final.csv")
    oot_path = os.path.join(DATA_DIR, "df_oot_final.csv")
    scorecard_path = os.path.join(DATA_DIR, "df_scorecard_points.csv")
    
    # Simple check to guarantee files exist before running
    for path in [train_path, val_path, oot_path, scorecard_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"🚨 Missing expected artifact at: {path}. Run development notebook export first!")
            
    df_train = pd.read_csv(train_path, index_col=0)
    df_val = pd.read_csv(val_path, index_col=0)
    df_oot = pd.read_csv(oot_path, index_col=0)
    df_scorecard = pd.read_csv(scorecard_path)
    
    return df_train, df_val, df_oot, df_scorecard
    