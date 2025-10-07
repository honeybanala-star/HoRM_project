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
st.set_page_config(page_title="Employee Attendance Dashboard", layout="wide")
st.title("📊 Employee Attendance & Next Best Action Dashboard")
st.markdown("Enter an Employee ID or Employee Name below to explore detailed KPIs and insights 👇")

# -----------------------
# 📥 Load & preprocess data
# -----------------------
@st.cache_data
def load_and_prepare():
    try:
        df = load_data()
        # any data prep steps here
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_and_prepare()
if df is not None:
    st.dataframe(df.head())
# -----------------------
# 🔎 Employee Input
# -----------------------
employee_input = st.text_input("Search by Employee ID or Name", placeholder="e.g., 0, 1, 2, ... or John Doe")

# Safe numeric conversion
def safe_float(value, decimals=2):
    try:
        return round(float(value), decimals)
    except:
        return 0.0

# -----------------------
# 📊 Dashboard
# -----------------------
if employee_input:
    try:
        # Determine if input is numeric ID or string name
        if employee_input.isnumeric():
            emp_id_int = int(employee_input)
            emp_kpis = get_employee_kpis(df, emp_id_int)
            emp_row = df[df['Employee ID'] == emp_id_int]
        else:
            emp_row = df[df['Employee Name'].str.contains(employee_input, case=False, na=False)]
            if len(emp_row) > 0:
                emp_id_int = emp_row.iloc[0]['Employee ID']
                emp_kpis = get_employee_kpis(df, emp_id_int)
            else:
                emp_kpis = None

        if not emp_kpis or emp_row.empty:
            st.error("❌ Employee not found. Please check and try again.")
        else:
            # -----------------------
            # 👤 Employee Summary Bar
            # -----------------------
            st.markdown("### 👤 Selected Employee Overview")
            col_id, col_name, col_account = st.columns(3)

            col_id.metric("Employee ID", emp_row.iloc[0]['Employee ID'])

            if 'Account code' in df.columns:
                account_val = emp_row['Account code'].values[0] if pd.notna(emp_row['Account code'].values[0]) else "N/A"
                col_account.metric("Account", account_val)
            else:
                col_account.metric("Account", "N/A")

            st.markdown("---")  # Separator before KPI cards

            # -----------------------
            # KPI Cards including Billing Status
            # -----------------------
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)

            # Compute overall averages from numeric columns only
            overall_kpis = df.select_dtypes(include='number').mean().to_dict()

            col1.metric("Avg. In Time (hrs)",
                        safe_float(emp_kpis.get("Avg. In Time")),
                        f"vs {safe_float(overall_kpis.get('Avg. In Time'))} avg")
            col2.metric("Avg. Out Time (hrs)",
                        safe_float(emp_kpis.get("Avg. Out Time")),
                        f"vs {safe_float(overall_kpis.get('Avg. Out Time'))} avg")
            col3.metric("Avg. Office Hrs",
                        safe_float(emp_kpis.get("Avg. Office hrs")),
                        f"vs {safe_float(overall_kpis.get('Avg. Office hrs'))} avg")

            # Billed / Unbilled status
            billed_status = "Billed" if emp_kpis.get("Billed") else "Unbilled"
            col4.metric("Billing Status", billed_status,
                        f"Overall: {df['Billed'].value_counts().idxmax() if 'Billed' in df.columns else 'N/A'}")

            col5.metric("Half-Day Leaves",
                        safe_float(emp_kpis.get("Half-Day leave"), 0),
                        f"vs {safe_float(overall_kpis.get('Half-Day leave'), 0)} avg")
            col6.metric("Full-Day Leaves",
                        safe_float(emp_kpis.get("Full-Day leave"), 0),
                        f"vs {safe_float(overall_kpis.get('Full-Day leave'), 0)} avg")

            st.markdown("---")

            # -----------------------
            # 📊 Bar Chart 1 – In/Out/Office Hours
            # -----------------------
            st.subheader("📈 Avg. In Time vs Out Time vs Office Hours")
            categories = ["Avg. In Time", "Avg. Out Time", "Avg. Office hrs"]
            emp_values = [safe_float(emp_kpis.get(c)) for c in categories]
            overall_values = [safe_float(overall_kpis.get(c)) for c in categories]

            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=categories, y=emp_values,
                name="Employee", marker_color="#1f77b4"
            ))
            fig1.add_trace(go.Bar(
                x=categories, y=overall_values,
                name="Overall Avg", marker_color="#ff7f0e"
            ))
            fig1.update_layout(barmode='group', height=400, template='plotly_white')
            st.plotly_chart(fig1, use_container_width=True)

            # -----------------------
            # 📊 Bar Chart 2 – Break/Cafeteria/Bay/OOO Hours
            # -----------------------
            st.subheader("🍽️ Break, Cafeteria, Bay & OOO Hours Comparison")
            categories2 = ["Avg. Break hrs", "Avg. Cafeteria hrs", "Avg. Bay hrs", "Avg. OOO hrs"]
            emp_values2 = [safe_float(emp_kpis.get(c)) for c in categories2]
            overall_values2 = [safe_float(overall_kpis.get(c)) for c in categories2]

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=categories2, y=emp_values2,
                name="Employee", marker_color="#2ca02c"
            ))
            fig2.add_trace(go.Bar(
                x=categories2, y=overall_values2,
                name="Overall Avg", marker_color="#d62728"
            ))
            fig2.update_layout(barmode='group', height=400, template='plotly_white')
            st.plotly_chart(fig2, use_container_width=True)

            # -----------------------
            # 📶 Gauge Chart – Office Hours Progress
            # -----------------------
            st.subheader("📶 Office Hours Completion Gauge")
            office_hours = safe_float(emp_kpis.get("Avg. Office hrs"))
            target_hours = 8
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=office_hours,
                delta={'reference': target_hours, 'increasing': {'color': "green"}},
                gauge={'axis': {'range': [0, 10]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 6], 'color': "#ffcccc"},
                           {'range': [6, 8], 'color': "#ffe0b3"},
                           {'range': [8, 10], 'color': "#ccffcc"}
                       ],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 8}},
                title={'text': "Office Hours Progress"}
            ))
            fig_gauge.update_layout(height=300, template='plotly_white')
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("---")

            # -----------------------
            # 🧭 HR-Focused Recommendations
            # -----------------------
            st.markdown("## 🧭 Next Best Actions for HR")
            recs = recommend_action(emp_kpis, overall_kpis=overall_kpis)
            for r in recs:
                st.markdown(f"- {r}")

    except ValueError:
        st.error("❌ Please enter a valid numeric Employee ID or Name.")
