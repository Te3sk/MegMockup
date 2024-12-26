from datetime import datetime
from . import file_utils as fu
from . import date_utils as du
import inspect

# Path to the JSON file
EVENTS_FILE = "../data/events.json"

def generate_id(events):
    """
    Generate a new unique ID for an event.

    Args:
        events (list of dict): A list of event dictionaries, where each dictionary contains an "id" key.

    Returns:
        int: A new unique ID for the event. If the list is empty, returns 1.
    """
    if not events:
        return 1
    return max(event["id"] for event in events) + 1

def add_event(title, date, time, description, location):
    """
    Adds a new event to the event list.

    Args:
        title (str): The title of the event.
        date (str): The date of the event in the "YYYY-MM-DD" format.
        time (str): The time of the event in the "HH:MM" format.
        description (str): The description of the event.
        location (str): The location of the event.

    Returns:
        str: An error message if the date or time are invalid, otherwise None.
    """
    
    print("enter in utils/add_event")

    events = fu.load_events()

    # TODO - temp debug print
    print(f"{__file__}\\{inspect.currentframe().f_code.co_name} - event json loaded: {events}")

    # Validate the date and time
    if du.validate_date(date) is False:
        return "Error: Invalid date or time. Please try again."
    
    if time != "":
        if du.validate_time(time) is False:
            return "Error: Invalid date or time. Please try again."
        
    # TODO - temp debug print
    print(f"{__file__}\\{inspect.currentframe().f_code.co_name} - date and time validated")

    # Generate a new ID and create the event
    new_event = {
        "id": generate_id(events),
        "title": title,
        "date": date,
        "time": time,
        "description": description,
        "location": location,
        "tags": []
    }

    # Add the event to the list and save it
    events.append(new_event)
    fu.save_events(events)

def edit_event(event_id, new_title, new_date, new_time, new_description, new_location):
    """
    Edits an existing event with the provided new details.

    Args:
        event_id (int): The ID of the event to be edited.
        new_title (str): The new title of the event.
        new_date (str): The new date of the event.
        new_time (str): The new time of the event.
        new_description (str): The new description of the event.
        new_location (str): The new location of the event.

    Returns:
        str: An error message if the event with the specified ID is not found, otherwise None.
    """
    # Load existing events
    events = fu.load_events()

    # Check if events are available
    if not events:
        return "No events available."

    # Find the event with the specified ID
    event_found = next((event for event in events if event["id"] == event_id), None)

    if event_found:
        # Update the event details
        event_found["title"] = new_title
        event_found["date"] = new_date
        event_found["time"] = new_time
        event_found["description"] = new_description
        event_found["location"] = new_location

        # Save the updated events
        fu.save_events(events)
    else:
        return "Error: No event found with the specified ID."

def search_events_by_keyword(keyword):
    """
    Searches for events that match the provided keyword.

    The search is case-insensitive and checks the title, location, and description fields of the events.
    Events are returned in priority order: first matches in the title, then in the location, and finally in the description.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        list: A list of event IDs that match the keyword, sorted by match priority.
    """
    keyword = keyword.lower()  # Convert the keyword to lowercase for case-insensitive comparison
    events = fu.load_events()
    results = []

    # Separate events by match priority
    match_title = []
    match_location = []
    match_description = []

    for event in events:
        # Case-insensitive comparison for title, location, and description
        if keyword in event["title"].lower():
            match_title.append(event["id"])
        elif keyword in event["location"].lower():
            match_location.append(event["id"])
        elif keyword in event["description"].lower():
            match_description.append(event["id"])

    # Combine results sorted by priority
    results.extend(match_title)
    results.extend(match_location)
    results.extend(match_description)

    return results

def get_events_by_date(date_input):
    """
    Filters and sorts events for a specific date.

    Args:
        date_input (str): The date in string format (YYYY-MM-DD).

    Returns:
        list: A list of events filtered and sorted by time. If the provided date is invalid (ValueError), returns an empty list.
    """
    if not du.validate_date(date_input):
        print("Error: The provided date is invalid. Please use the format YYYY-MM-DD.")
        return []
    
    # Validate the date
    date_input = datetime.strptime(date_input, "%Y-%m-%d").date()

    events = fu.load_events()
    # Filter events by the provided date
    filtered_events = [event for event in events if event["date"] == date_input.strftime("%Y-%m-%d")]

    # Sort events by time
    sorted_events = sorted(filtered_events, key=lambda event: event["time"])

    return sorted_events

def delete_event(event_id):
    """
    Deletes an event with the specified ID from the JSON events file.

    Args:
        event_id (int): The ID of the event to delete.

    Returns:
        bool: True if the event was successfully deleted, False if the event was not found.
    Raises:
        FileNotFoundError: If the events file does not exist.
        JSONDecodeError: If the events file is not a valid JSON.
    """
    # Load events from the JSON file
    events = fu.load_events()

    # Find the event with the specified ID
    event_found = next((event for event in events if event["id"] == event_id), None)

    if event_found:
        # Remove the event from the list
        events = [event for event in events if event["id"] != event_id]
        # Save the updated events
        fu.save_events(events)
        print(f"\nEvent with ID {event_id} successfully deleted!")
        return True
    else:
        print(f"\nError: No event found with ID {event_id}.")
        return False

def today_event():
    """
    Displays the events scheduled for today.

    Returns:
        list: A list of events scheduled for today, sorted by time. If no events are found, returns an empty list.
    """
    today = du.get_current_date()
    return get_events_by_date(today)

def tomorrow_events():
    """
    Displays the events scheduled for tomorrow.

    Returns:
        list: A list of events scheduled for tomorrow, sorted by time. If no events are found, returns an empty list.
    """
    tomorrow = du.add_days(du.get_current_date(), 1)
    return get_events_by_date(tomorrow)

def main():
    print("This is the main function of the event_manager module.")
    title = input("title: ")
    date = input("date (yyyy-mm-dd): ")
    time = input("time (hh:mm): ")
    description = input("description: ")
    location = input("location: ")
    add_event(title, date, time, description, location)

if __name__ == "__main__":
    main()