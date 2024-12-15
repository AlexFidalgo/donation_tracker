def format_currency(value):
    return float(value.replace("R$", "").replace(".", "").replace(",", "."))

def calculate_percentage(donation, goal):
    return (donation / goal) * 100

def prepare_data(donation_value, goal_value):
    donation = format_currency(donation_value)
    goal = format_currency(goal_value)
    percentage = calculate_percentage(donation, goal)
    return {
        "donation": donation_value,
        "goal": goal_value,
        "percentage": f"{percentage:.2f}%"
    }
