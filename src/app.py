# src/app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data_loader import load_data
from data_processing import preprocess_data, get_employee_kpis
from rule_based import recommend_action

# -----------------------
# 🔧 Streamlit Page Config
# -----------------------
st.set_page_config(
    page_title="Employee Attendance Dashboard", 
    layout="wide",
    page_icon="📊"
)

st.title("📊 Employee Attendance & Next Best Action Dashboard")
st.markdown("Enter an Employee ID below to explore detailed KPIs and HR insights 👇")

# -----------------------
# 📥 Load & preprocess data
# -----------------------
@st.cache_data
def load_and_prepare():
    df = load_data()
    if df.empty:
        st.error("No data available. Please check your data file.")
        return pd.DataFrame()
    return preprocess_data(df)

# Load data
df = load_and_prepare()

if df.empty:
    st.stop()

# -----------------------
# 🔎 Employee Input
# -----------------------
employee_input = st.text_input("**Search by Employee ID**", placeholder="e.g., 1, 2, 3, ... (1-20 for sample data)")

# Helper function for safe numeric conversion
def safe_float(value, decimals=2):
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return 0.0

# -----------------------
# 📊 Main Dashboard
# -----------------------
if employee_input:
    try:
        if employee_input.isnumeric():
            emp_id_int = int(employee_input)
            emp_kpis = get_employee_kpis(df, emp_id_int)
            emp_row = df[df['Employee ID'] == emp_id_int]
        else:
            st.error("❌ Please enter a valid numeric Employee ID.")
            st.stop()

        if not emp_kpis or emp_row.empty:
            st.error(f"❌ Employee ID {employee_input} not found. Try IDs 1-20 for sample data.")
        else:
            # -----------------------
            # 👤 Employee Summary Section
            # -----------------------
            st.markdown("### 👤 Selected Employee Overview")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric("**Employee ID**", emp_id_int)
            
            with col2:
                if 'Employee Name' in emp_row.columns and not emp_row.empty:
                    emp_name = emp_row['Employee Name'].iloc[0]
                    st.metric("**Employee Name**", emp_name)
                else:
                    st.metric("**Employee Name**", "N/A")
            
            with col3:
                if 'Account code' in emp_row.columns and not emp_row.empty:
                    account_val = emp_row['Account code'].iloc[0]
                    st.metric("**Account**", account_val)
                else:
                    st.metric("**Account**", "N/A")

            st.markdown("---")

            # -----------------------
            # 📊 KPI Cards Section
            # -----------------------
            st.markdown("### 📊 Key Performance Indicators")
            
            # Create 3 columns for first row of KPIs
            col1, col2, col3 = st.columns(3)
            
            # Create 3 columns for second row of KPIs  
            col4, col5, col6 = st.columns(3)

            # Get employee KPI values
            emp_in_time = safe_float(emp_kpis.get("Avg. In Time", 0))
            emp_out_time = safe_float(emp_kpis.get("Avg. Out Time", 0))
            emp_office_hrs = safe_float(emp_kpis.get("Avg. Office Hrs", 0))
            emp_break_hrs = safe_float(emp_kpis.get("Avg. Break Hrs", 0))
            emp_cafeteria_hrs = safe_float(emp_kpis.get("Avg. Cafeteria Hrs", 0))
            emp_ooo_hrs = safe_float(emp_kpis.get("Avg. OOO Hrs", 0))
            emp_half_leaves = safe_float(emp_kpis.get("Half Day Leave", 0))
            emp_full_leaves = safe_float(emp_kpis.get("Full Day Leave", 0))
            billed_status = "Billed" if emp_kpis.get("Billed", True) else "Unbilled"

            # Calculate overall averages
            overall_in_time = safe_float(df['Avg. In Time'].mean()) if 'Avg. In Time' in df.columns else 0
            overall_out_time = safe_float(df['Avg. Out Time'].mean()) if 'Avg. Out Time' in df.columns else 0
            overall_office_hrs = safe_float(df['Avg. Office Hrs'].mean()) if 'Avg. Office Hrs' in df.columns else 0
            overall_half_leaves = safe_float(df['Half Day Leave'].mean()) if 'Half Day Leave' in df.columns else 0
            overall_full_leaves = safe_float(df['Full Day Leave'].mean()) if 'Full Day Leave' in df.columns else 0

            # KPI Card 1: Average In Time
            with col1:
                delta_in_time = emp_in_time - overall_in_time
                st.metric(
                    label="**Avg. In Time**",
                    value=f"{emp_in_time:.1f} hrs",
                    delta=f"{delta_in_time:+.1f} hrs vs avg",
                    delta_color="inverse" if delta_in_time > 0 else "normal"
                )

            # KPI Card 2: Average Out Time
            with col2:
                delta_out_time = emp_out_time - overall_out_time
                st.metric(
                    label="**Avg. Out Time**",
                    value=f"{emp_out_time:.1f} hrs",
                    delta=f"{delta_out_time:+.1f} hrs vs avg",
                    delta_color="normal" if delta_out_time > 0 else "inverse"
                )

            # KPI Card 3: Average Office Hours
            with col3:
                delta_office_hrs = emp_office_hrs - overall_office_hrs
                st.metric(
                    label="**Avg. Office Hours**",
                    value=f"{emp_office_hrs:.1f} hrs",
                    delta=f"{delta_office_hrs:+.1f} hrs vs avg",
                    delta_color="normal" if delta_office_hrs > 0 else "inverse"
                )

            # KPI Card 4: Billing Status
            with col4:
                st.metric(
                    label="**Billing Status**",
                    value=billed_status
                )

            # KPI Card 5: Half-Day Leaves
            with col5:
                delta_half_leaves = emp_half_leaves - overall_half_leaves
                st.metric(
                    label="**Half-Day Leaves**",
                    value=f"{int(emp_half_leaves)}",
                    delta=f"{delta_half_leaves:+.0f} vs avg",
                    delta_color="inverse" if delta_half_leaves > 0 else "normal"
                )

            # KPI Card 6: Full-Day Leaves
            with col6:
                delta_full_leaves = emp_full_leaves - overall_full_leaves
                st.metric(
                    label="**Full-Day Leaves**",
                    value=f"{int(emp_full_leaves)}",
                    delta=f"{delta_full_leaves:+.0f} vs avg",
                    delta_color="inverse" if delta_full_leaves > 0 else "normal"
                )

            st.markdown("---")

            # -----------------------
            # 📈 Charts Section
            # -----------------------
            st.markdown("### 📈 Visual Analytics")

            # Chart 1: Attendance Hours Comparison
            st.subheader("Office Hours Comparison")
            
            chart1_data = pd.DataFrame({
                'Metric': ['In Time', 'Out Time', 'Office Hours'],
                'Employee': [emp_in_time, emp_out_time, emp_office_hrs],
                'Overall Average': [overall_in_time, overall_out_time, overall_office_hrs]
            })
            
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                name=f'Employee {emp_id_int}',
                x=chart1_data['Metric'],
                y=chart1_data['Employee'],
                text=chart1_data['Employee'].round(1),
                textposition='auto',
                marker_color='#1f77b4'
            ))
            fig1.add_trace(go.Bar(
                name='Overall Average',
                x=chart1_data['Metric'],
                y=chart1_data['Overall Average'],
                text=chart1_data['Overall Average'].round(1),
                textposition='auto',
                marker_color='#ff7f0e'
            ))
            
            fig1.update_layout(
                barmode='group',
                height=400,
                template='plotly_white',
                yaxis_title='Hours',
                showlegend=True
            )
            
            st.plotly_chart(fig1, use_container_width=True)

            # Chart 2: Activity Hours Comparison
            st.subheader("Activity Hours Comparison")
            
            overall_break_hrs = safe_float(df['Avg. Break Hrs'].mean()) if 'Avg. Break Hrs' in df.columns else 0
            overall_cafeteria_hrs = safe_float(df['Avg. Cafeteria Hrs'].mean()) if 'Avg. Cafeteria Hrs' in df.columns else 0
            overall_ooo_hrs = safe_float(df['Avg. OOO Hrs'].mean()) if 'Avg. OOO Hrs' in df.columns else 0
            
            chart2_data = pd.DataFrame({
                'Activity': ['Break Hours', 'Cafeteria Hours', 'OOO Hours'],
                'Employee': [emp_break_hrs, emp_cafeteria_hrs, emp_ooo_hrs],
                'Overall Average': [overall_break_hrs, overall_cafeteria_hrs, overall_ooo_hrs]
            })
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                name=f'Employee {emp_id_int}',
                x=chart2_data['Activity'],
                y=chart2_data['Employee'],
                text=chart2_data['Employee'].round(1),
                textposition='auto',
                marker_color='#2ca02c'
            ))
            fig2.add_trace(go.Bar(
                name='Overall Average',
                x=chart2_data['Activity'],
                y=chart2_data['Overall Average'],
                text=chart2_data['Overall Average'].round(1),
                textposition='auto',
                marker_color='#d62728'
            ))
            
            fig2.update_layout(
                barmode='group',
                height=400,
                template='plotly_white',
                yaxis_title='Hours',
                showlegend=True
            )
            
            st.plotly_chart(fig2, use_container_width=True)

            # Chart 3: Office Hours Gauge
            st.subheader("Office Hours Progress")
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=emp_office_hrs,
                delta={'reference': 8.0},
                gauge={
                    'axis': {'range': [0, 12]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 6], 'color': "lightcoral"},
                        {'range': [6, 8], 'color': "lightyellow"},
                        {'range': [8, 12], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                },
                title={'text': "Target: 8.0 hours"}
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("---")

            # -----------------------
            # 🎯 Recommendations Section
            # -----------------------
            st.markdown("## 🎯 HR Recommendations & Next Best Actions")
            
            # Prepare overall KPIs for recommendations
            overall_kpis_dict = {
                'Avg. In Time': overall_in_time,
                'Avg. Out Time': overall_out_time,
                'Avg. Office Hrs': overall_office_hrs,
                'Half Day Leave': overall_half_leaves,
                'Full Day Leave': overall_full_leaves
            }
            
            # Get recommendations
            recommendations = recommend_action(emp_kpis, overall_kpis_dict)
            
            # Display recommendations in a nice format
            for i, recommendation in enumerate(recommendations, 1):
                st.markdown(f"{i}. {recommendation}")

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Try entering an Employee ID between 1-20 for sample data")

# -----------------------
# 🏠 Welcome Section (when no employee selected)
# -----------------------
else:
    st.markdown("## 🏠 Welcome to Employee Analytics Dashboard")
    
    # Display quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_employees = len(df['Employee ID'].unique()) if 'Employee ID' in df.columns else 0
        st.metric("Total Employees", total_employees)
    
    with col2:
        st.metric("Total Records", len(df))
    
    with col3:
        if 'Billed' in df.columns:
            if df['Billed'].dtype == bool:
                billed_count = df['Billed'].sum()
            else:
                billed_count = (df['Billed'] == 'Billed').sum() if 'Billed' in df.columns else 0
            st.metric("Billed Employees", int(billed_count))
        else:
            st.metric("Billed Employees", "N/A")
    
    st.markdown("---")
    
    # Instructions
    st.info("""
    💡 **How to use this dashboard:**
    1. Enter an **Employee ID** in the search box above
    2. View detailed **KPIs and analytics** for that employee
    3. Get **HR recommendations** based on attendance patterns
    4. Compare with **overall team averages**
    
    🔍 **For sample data, try Employee IDs from 1 to 20**
    """)