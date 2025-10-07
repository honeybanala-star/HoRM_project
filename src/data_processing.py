# src/data_processing.py

import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess attendance data - ensure all columns are numeric
    """
    # List of columns that should be numeric
    numeric_columns = [
        'Avg. In Time', 'Avg. Out Time', 'Avg. Break Hrs',
        'Avg. Cafeteria Hrs', 'Avg. Office Hrs', 'Avg. OOO Hrs',
        'Full Day Leave', 'Half Day Leave'
    ]
    
    # Convert each column to numeric, coerce errors to NaN then fill with 0
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)
    
    # Ensure Employee ID is proper
    if 'Employee ID' in df.columns:
        df['Employee ID'] = pd.to_numeric(df['Employee ID'], errors='coerce')
        df = df.dropna(subset=['Employee ID'])
        df['Employee ID'] = df['Employee ID'].astype(int)
    
    return df

def get_employee_kpis(df: pd.DataFrame, employee_id: int) -> dict:
    """
    Get KPI stats for a specific employee
    """
    # Filter data for the specific employee
    emp_data = df[df['Employee ID'] == employee_id]
    
    if emp_data.empty:
        return {}
    
    kpis = {}
    
    # Extract all relevant KPIs
    kpi_mappings = {
        'Avg. In Time': 'mean',
        'Avg. Out Time': 'mean',
        'Avg. Break Hrs': 'mean',
        'Avg. Cafeteria Hrs': 'mean',
        'Avg. Office Hrs': 'mean',
        'Avg. OOO Hrs': 'mean',
        'Full Day Leave': 'sum',
        'Half Day Leave': 'sum',
        'Billed': 'first'
    }
    
    for column, agg_func in kpi_mappings.items():
        if column in emp_data.columns:
            if agg_func == 'mean':
                kpis[column] = float(emp_data[column].mean())
            elif agg_func == 'sum':
                kpis[column] = float(emp_data[column].sum())
            elif agg_func == 'first':
                kpis[column] = emp_data[column].iloc[0] if not emp_data.empty else True
    
    return kpis