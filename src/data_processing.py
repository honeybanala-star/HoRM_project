# src/data_processing.py

import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess attendance data:
    - Convert time-like columns to hours
    - Fill missing values with 0
    """
    time_cols = ['Avg. In Time', 'Avg. Out Time', 'Avg. Office hrs',
                 'Avg. Bay hrs', 'Avg. Break hrs', 'Avg. Cafeteria hrs', 'Avg. OOO hrs']

    for col in time_cols:
        if col in df.columns:
            # Convert to timedelta if looks like time strings
            try:
                df[col] = pd.to_timedelta(df[col]).dt.total_seconds() / 3600
            except Exception:
                # If numeric, keep as hours
                df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)
    return df

def get_employee_kpis(df: pd.DataFrame, employee_id: int) -> dict:
    """
    Get KPI stats for a specific employee and return as a dictionary.
    """
    emp_df = df[df['Employee ID'] == employee_id]
    if emp_df.empty:
        return {}

    emp_stats = emp_df.agg({
        'Avg. In Time': 'mean',
        'Avg. Out Time': 'mean',
        'Avg. Office hrs': 'mean',
        'Avg. Bay hrs': 'mean',
        'Avg. Break hrs': 'mean',
        'Avg. Cafeteria hrs': 'mean',
        'Avg. OOO hrs': 'mean',
        'Unbilled': 'sum',
        'Half-Day leave': 'sum',
        'Full-Day leave': 'sum',
        'Online Check-in': 'sum',
        'Excemptions': 'sum',
        'Allocation': 'count'
    })


    return emp_stats.to_dict()
