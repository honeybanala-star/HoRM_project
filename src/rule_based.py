# rule_based.py

def recommend_action(emp_kpis, overall_kpis=None):
    """
    Generate HR-focused recommendations based on employee KPIs and attendance patterns.
    Takes into account account assignment, billed/unbilled status, attendance, office behavior, and overall patterns.
    """
    recommendations = []

    def safe_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    # Employee KPIs
    avg_in_time = safe_float(emp_kpis.get("Avg. In Time"))
    avg_out_time = safe_float(emp_kpis.get("Avg. Out Time"))
    avg_office_hrs = safe_float(emp_kpis.get("Avg. Office hrs"))
    avg_break_hrs = safe_float(emp_kpis.get("Avg. Break hrs"))
    avg_cafeteria_hrs = safe_float(emp_kpis.get("Avg. Cafeteria hrs"))
    avg_bay_hrs = safe_float(emp_kpis.get("Avg. Bay hrs"))
    avg_ooo_hrs = safe_float(emp_kpis.get("Avg. OOO hrs"))
    billed = emp_kpis.get("Billed", True)  # True = billed, False = unbilled
    half_day_leaves = safe_float(emp_kpis.get("Half-Day leave"))
    full_day_leaves = safe_float(emp_kpis.get("Full-Day leave"))
    online_checkins = safe_float(emp_kpis.get("Online Check-in"))
    exemptions = safe_float(emp_kpis.get("Excemptions"))
    account = emp_kpis.get("Account Code", "N/A")

    # --- HR-Focused Recommendations ---

    # Attendance
    if full_day_leaves > 3:
        recommendations.append("Multiple full-day leaves → Schedule counseling and investigate reasons.")
    if half_day_leaves > 2:
        recommendations.append("Frequent half-day leaves → Encourage planned leaves and monitor patterns.")
    if avg_in_time > 9:
        recommendations.append("Late arrivals → Send reminders or discuss flexible hours with employee.")
    if avg_out_time < 17:
        recommendations.append("Early departures → Ensure timely clock-outs; discuss workload expectations.")
    if avg_office_hrs < 8:
        recommendations.append("Low office hours → Verify engagement in tasks and workload allocation.")

    # Breaks & Bay hours
    if avg_break_hrs > 1.5:
        recommendations.append("Excessive break hours → Remind about break policies and time management.")
    if avg_cafeteria_hrs > 1.0:
        recommendations.append("Long cafeteria breaks → Coach employee on effective break usage.")
    if avg_bay_hrs < 1.0:
        recommendations.append("Low bay hours → Ensure employee is contributing to account tasks.")
    if avg_ooo_hrs > 2.0:
        recommendations.append("High OOO hours → Check WFH or offsite compliance with policy.")

    # Billing / Account
    if not billed:
        if account != "N/A":
            recommendations.append(f"Employee not billed to account '{account}' → Follow up on allocation or project assignment.")
        else:
            recommendations.append("Employee not billed to any account → Assign to a project or account.")

    # Online check-ins & exemptions
    if online_checkins < 5:
        recommendations.append("Low online check-ins → Encourage regular attendance logging.")
    if exemptions > 2:
        recommendations.append("High exemptions → Investigate patterns and compliance with policy.")

    # Positive reinforcement
    if full_day_leaves <= 1 and half_day_leaves <= 1 and avg_office_hrs >= 8:
        recommendations.append("Consistent attendance → Recognize and reward positive behavior.")

    # Fallback
    if not recommendations:
        recommendations.append("No specific actions recommended at this time.")

    return recommendations
