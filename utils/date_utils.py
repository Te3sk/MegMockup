from datetime import datetime, timedelta

def validate_date(date_str):
    """
    Checks if a string represents a valid date in the format YYYY-MM-DD.

    Args:
        date_str (str): The date to validate.

    Returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """
    Checks if a string represents a valid time in the format HH:MM.

    Args:
        time_str (str): The time to validate.

    Returns:
        bool: True if the time is valid, False otherwise.
    """
    try:
        if time_str == "":
            return False
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def get_current_date():
    """
    Returns the current date in the format YYYY-MM-DD.

    Returns:
        str: The current date.
    """
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    """
    Returns the current time in the format HH:MM.

    Returns:
        str: The current time.
    """
    return datetime.now().strftime("%H:%M")

def add_days(date_str, days):
    """
    Adds a number of days to a date and returns the new date.

    Args:
        date_str (str): The initial date in the format YYYY-MM-DD.
        days (int): The number of days to add.

    Returns:
        str: The new date in the format YYYY-MM-DD.
    """
    if not validate_date(date_str):
        raise ValueError("The provided date is invalid.")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = date + timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")

def days_difference(start_date, end_date):
    """
    Calculates the difference in days between two dates.

    Args:
        start_date (str): The start date in the format YYYY-MM-DD.
        end_date (str): The end date in the format YYYY-MM-DD.

    Returns:
        int: The difference in days between the two dates.
    """
    if not (validate_date(start_date) and validate_date(end_date)):
        raise ValueError("One or both provided dates are invalid.")
    date1 = datetime.strptime(start_date, "%Y-%m-%d")
    date2 = datetime.strptime(end_date, "%Y-%m-%d")
    difference = date2 - date1
    return difference.days

def compare_dates(date1, date2):
    """
    Compares two dates and returns which one is greater.

    Args:
        date1 (str): The first date in the format YYYY-MM-DD.
        date2 (str): The second date in the format YYYY-MM-DD.

    Returns:
        int: -1 if date1 < date2, 0 if date1 == date2, 1 if date1 > date2.
    """
    if not (validate_date(date1) and validate_date(date2)):
        raise ValueError("One or both provided dates are invalid.")
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    if d1 < d2:
        return -1
    elif d1 > d2:
        return 1
    else:
        return 0

def convert_date_to_readable(date_str):
    """
    Converts a date in the format YYYY-MM-DD to a more readable format.

    Args:
        date_str (str): The date in the format YYYY-MM-DD.

    Returns:
        str: The date in a readable format, e.g., "20 December 2024".
    """
    if not validate_date(date_str):
        raise ValueError("The provided date is invalid.")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%d %B %Y")
