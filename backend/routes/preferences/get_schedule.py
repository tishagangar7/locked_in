def process_user_schedule(data):
    """
    Process the user's selected schedule and preferences.
    :param data: A dictionary containing the user's selected time slots and preferences.
    Example:
    {
        "duration": 2,
        "schedule": {
            "2025-04-15": {
                "best": ["9:00 AM - 11:00 AM"],
                "works": ["1:00 PM - 3:00 PM"],
                "not_preferred": ["4:00 PM - 6:00 PM"]
            }
        }
    }
    :return: Processed schedule data.
    """
    duration = data.get("duration", 1)
    schedule = data.get("schedule", {})
    return {
        "duration": duration,
        "schedule": schedule
    }