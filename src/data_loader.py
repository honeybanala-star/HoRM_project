# src/data_loader.py
import pandas as pd
import os
import streamlit as st
import numpy as np

def load_data(path: str = "data/attendance_sample.xlsx") -> pd.DataFrame:
    """
    Loads the attendance Excel file
    """
    try:
        # Make path absolute relative to project root
        base_dir = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_dir, path)
        
        if not os.path.exists(full_path):
            st.warning("📋 Using sample data as file not found")
            return create_sample_data()
        
        df = pd.read_excel(full_path, engine="openpyxl")
        st.success(f"✅ Loaded {len(df)} records from file")
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.warning("📋 Using sample data instead")
        return create_sample_data()

def create_sample_data() -> pd.DataFrame:
    """
    Create sample data for demonstration
    """
    np.random.seed(42)
    
    sample_data = {
        'Employee ID': range(1, 21),
        'Employee Name': [f'Employee {i}' for i in range(1, 21)],
        'Account code': [f'ACC{np.random.randint(100, 999)}' for _ in range(20)],
        'Avg. In Time': np.round(np.random.normal(9.0, 0.5, 20), 2),
        'Avg. Out Time': np.round(np.random.normal(18.0, 0.5, 20), 2),
        'Avg. Break Hrs': np.round(np.random.normal(0.5, 0.2, 20), 2),
        'Avg. Cafeteria Hrs': np.round(np.random.normal(0.3, 0.1, 20), 2),
        'Avg. Office Hrs': np.round(np.random.normal(8.5, 0.3, 20), 2),
        'Avg. OOO Hrs': np.round(np.random.normal(0.2, 0.1, 20), 2),
        'Full Day Leave': np.random.randint(0, 5, 20),
        'Half Day Leave': np.random.randint(0, 3, 20),
        'Billed': np.random.choice([True, False], 20, p=[0.8, 0.2])
    }
    
    df = pd.DataFrame(sample_data)
    return df