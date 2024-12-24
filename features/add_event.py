import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import file_utils as fu
from utils import date_utils as du
from utils import event_manager as em


def main():
    print("--- New Event ---")

    # Get the event details from the user
    while True: # Loop until a valid title is entered
        title = input("Title: ")
        if not title:
            print("Error: Title cannot be empty. Please try again.")
        else:
            break
    ad = input("All day? (Y/N): ")
    while True: # Loop until a valid date is entered
        while True: # Loop until a valid day is entered
            day = input("Day: ")
            if not day:
                print("Error: Day cannot be empty. Please try again.")
            else:
                break
        while True: # Loop until a valid month is entered
            month = input("Month: ")
            if not month:
                print("Error: Month cannot be empty. Please try again.")
            else:
                break
        while True: # Loop until a valid year is entered
            year = input("Year: ")
            if not year:
                print("Error: Year cannot be empty. Please try again.")
            else:
                break
        date_str = f"{year}-{month}-{day}"
        if not du.validate_date(date_str):
            print("Error: Invalid date format. Please try again.")
        else:
            break
    while True: # Loop until a valid time is entered
        while True: # Loop until a valid hours is entered
            hours = input("Hours: ")
            if not hours:
                print("Error: Hours cannot be empty. Please try again.")
            else:
                break
        while True: # Loop until a valid minutes is entered
            minutes = input("Minutes: ")
            if not minutes:
                print("Error: Minutes cannot be empty. Please try again.")
            else:
                break
        time_str = f"{hours}:{minutes}"
        if not du.validate_time(time_str):
            print("Error: Invalid time format. Please try again.")
        else:
            break
    location = input("Location: ")
    description = input("Description: ")

    # Add the event to the list
    error = em.add_event(title, date_str, time_str, description, location)
    if error:
        print(error)
    else:
        print("Event added successfully.")


if __name__ == "__main__":
    main()