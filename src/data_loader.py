# src/data_loader.py
import pandas as pd

def load_data(path: str = "data/attendance_sample.xlsx") -> pd.DataFrame:
    """
    Loads the attendance Excel file and returns a pandas DataFrame.
    """
    try:
        df = pd.read_excel(path, engine="openpyxl")
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Attendance data file not found. Please check the 'data/' folder.")
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")
