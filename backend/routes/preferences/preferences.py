from datetime import datetime, timedelta

def process_user_schedule(data):
    try:
        schedule = data.get('schedule', [])

        if not schedule:
            return {"success": False, "message": "No schedule data provided"}

        # Current time for validation
        current_time = datetime.now()

        # Validate each time slot
        valid_slots = []
        invalid_slots = []
        for slot in schedule:
            try:
                # Parse the date and time
                date = slot.get('date')
                time_range = slot.get('time')
                category = slot.get('category')

                if not date or not time_range or not category:
                    raise ValueError("Missing required fields: date, time, or category")

                # Parse the start and end times
                start_time_str, end_time_str = time_range.split(" - ")
                start_time = datetime.strptime(f"{date} {start_time_str}", "%Y-%m-%d %I:%M %p")
                end_time = datetime.strptime(f"{date} {end_time_str}", "%Y-%m-%d %I:%M %p")

                # Validation: Check if the time is in the past
                if start_time < current_time:
                    raise ValueError("Start time is in the past")

                # Validation: Check if the time is within 1 hour from now
                if start_time < current_time + timedelta(hours=1):
                    raise ValueError("Start time must be at least 1 hour from now")

                # Validation: Check if the end time is after the start time
                if end_time <= start_time:
                    raise ValueError("End time must be after start time")

                # If all validations pass, add to valid slots
                valid_slots.append({
                    "date": date,
                    "time": time_range,
                    "category": category
                })

            except ValueError as e:
                # Add invalid slots with error messages
                invalid_slots.append({
                    "slot": slot,
                    "error": str(e)
                })

        # Return the results
        return {
            "success": True,
            "valid_slots": valid_slots,
            "invalid_slots": invalid_slots
        }

    except Exception as e:
        # Handle unexpected errors
        return {"success": False, "message": "An error occurred", "error": str(e)}