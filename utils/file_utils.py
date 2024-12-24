import json

# Path to the JSON file
EVENTS_FILE = "../data/events.json"

def load_events():
    """
    Loads events from a JSON file.

    Attempts to open and read the file specified by the EVENTS_FILE variable.
    If the file exists and contains valid data, it returns a list of events.
    If the file does not exist or is corrupted, it returns an empty list.

    Returns:
        list: A list of events if the file exists and contains valid data, otherwise an empty list.
    """
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("events", [])
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        return []
    except json.JSONDecodeError:
        # If the file is corrupted, return an empty list
        return []

def save_events(events):
    """
    Saves a list of events to a JSON file.

    Args:
        events (list): The list of events to save.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        IOError: If an error occurs while writing to the file.
    """
    with open(EVENTS_FILE, "w", encoding="utf-8") as file:
        json.dump({"events": events}, file, indent=4, ensure_ascii=False)

def clear_calendar():
    """
    Clears all events from the calendar.

    This function initializes an empty list of events and saves it,
    effectively removing all existing events from the calendar.
    """
    events = []
    save_events(events)