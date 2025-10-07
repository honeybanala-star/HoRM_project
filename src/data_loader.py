# src/data_loader.py
import pandas as pd
import os

def load_data(path: str = "data/attendance_sample.xlsx") -> pd.DataFrame:
    """
    Loads the attendance Excel file and returns a pandas DataFrame.
    """
    # Make path relative to this file
    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes one level up from src/
    full_path = os.path.join(base_dir, path)

    try:
        df = pd.read_excel(full_path, engine="openpyxl")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Attendance data file not found at: {full_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")
