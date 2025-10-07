# rule_based.py

def recommend_action(emp_kpis, overall_kpis=None):
    """
    Generate HR-focused recommendations based on employee KPIs
    """
    recommendations = []

    # Helper function to safely convert to float
    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    # Extract KPIs with safe conversion
    avg_in_time = safe_float(emp_kpis.get("Avg. In Time", 0))
    avg_out_time = safe_float(emp_kpis.get("Avg. Out Time", 0))
    avg_office_hrs = safe_float(emp_kpis.get("Avg. Office Hrs", 0))
    avg_break_hrs = safe_float(emp_kpis.get("Avg. Break Hrs", 0))
    avg_cafeteria_hrs = safe_float(emp_kpis.get("Avg. Cafeteria Hrs", 0))
    avg_ooo_hrs = safe_float(emp_kpis.get("Avg. OOO Hrs", 0))
    half_day_leaves = safe_float(emp_kpis.get("Half Day Leave", 0))
    full_day_leaves = safe_float(emp_kpis.get("Full Day Leave", 0))
    billed = emp_kpis.get("Billed", True)

    # Generate recommendations based on thresholds
    
    # Attendance and Leave Patterns
    if full_day_leaves > 3:
        recommendations.append("🚨 High full-day leaves detected: Schedule counseling session to understand reasons")
    elif full_day_leaves > 1:
        recommendations.append("⚠️ Moderate full-day leaves: Monitor leave pattern for consistency")

    if half_day_leaves > 2:
        recommendations.append("⚠️ Frequent half-day leaves: Discuss proper leave planning procedures")
    elif half_day_leaves > 1:
        recommendations.append("📝 Some half-day leaves: Ensure work handover during leaves")

    # Office Timing Patterns
    if avg_in_time > 9.5:
        recommendations.append("⏰ Consistently late arrivals: Discuss flexible timing options")
    elif avg_in_time > 9.0:
        recommendations.append("⏰ Slightly late arrivals: Gentle reminder about office timing")

    if avg_out_time < 17.0:
        recommendations.append("🏃 Early departures: Review workload and task completion status")
    
    # Office Hours
    if avg_office_hrs < 7.0:
        recommendations.append("📉 Low office hours: Check task allocation and employee engagement")
    elif avg_office_hrs < 8.0:
        recommendations.append("📊 Below target office hours: Monitor productivity and provide support")

    # Break and Activity Patterns
    if avg_break_hrs > 1.0:
        recommendations.append("☕ Long break hours: Discuss time management and break policies")
    
    if avg_cafeteria_hrs > 0.8:
        recommendations.append("🍽️ Extended cafeteria time: Encourage efficient break usage")
    
    if avg_ooo_hrs > 1.5:
        recommendations.append("🏠 High OOO hours: Verify work-from-home arrangements")

    # Billing Status
    if not billed:
        recommendations.append("💼 Employee not billed: Review project allocation and client assignments")

    # Positive reinforcement for good patterns
    if (full_day_leaves <= 1 and half_day_leaves <= 1 and 
        avg_office_hrs >= 8.0 and avg_in_time <= 9.0 and avg_out_time >= 17.0):
        recommendations.append("⭐ Excellent attendance record: Consider for recognition or rewards")

    # Fallback if no specific recommendations
    if not recommendations:
        recommendations.append("✅ Attendance patterns are within normal ranges. Continue regular monitoring.")

    return recommendations