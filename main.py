# Punto di ingresso dell'app
import features 
import curses

import features.add_event  # Import the curses module for building command-line user interfaces.

def menu_navigation(stdscr, options):
# Disable the cursor for better visual appearance
    curses.curs_set(0)
    # Enable color support (optional)
    curses.start_color()
    # Define a color pair (foreground: black, background: white) for the selected option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Set the initial selected option index
    selected_idx = 0

    # Enable keypad mode to ensure special keys are captured
    stdscr.keypad(True)

    # Infinite loop for handling menu interactions
    while True:
        # Clear the screen before each rendering
        stdscr.clear()
        # Get the screen dimensions (height and width)
        h, w = stdscr.getmaxyx()
        
        # Iterate over each option in the menu
        for idx, option in enumerate(options):
            # Calculate the horizontal position to center the text
            x = 0 #w // 2 - len(option) // 2
            # Calculate the vertical position for each option
            y = h // 2 - len(options) // 2 + idx
            
            # Highlight the selected option
            if idx == selected_idx:
                stdscr.attron(curses.color_pair(1))  # Turn on the highlight color pair
                stdscr.addstr(y, x, option)  # Display the highlighted option
                stdscr.attroff(curses.color_pair(1))  # Turn off the highlight
            else:
                # Display non-selected options normally
                stdscr.addstr(y, x, option)
        
        # Refresh the screen to apply changes
        stdscr.refresh()

        # Wait for user key press
        key = stdscr.getch()

        # Handle UP arrow key
        if key in [curses.KEY_UP, 259]:
            selected_idx = (selected_idx - 1) % len(options)  # Move selection up
        # Handle DOWN arrow key
        elif key in [curses.KEY_DOWN, 258]:
            selected_idx = (selected_idx + 1) % len(options)  # Move selection down
        # Handle ENTER key
        elif key in [10, 13]:
            if options[selected_idx] == 'Esci':
                break  # Exit the loop if "Esci" is selected
            else:
                # Clear the screen and show the selected option
                stdscr.clear()
                # message = f"Hai selezionato: {options[selected_idx]}"
                # stdscr.addstr(h // 2, w // 2 - len(message) // 2, message)
                stdscr.refresh()
                return selected_idx
        # Handle ESC key
        elif key == 27:
            break  # Exit the loop on ESC key press

# Main menu function
def main_menu(stdscr):
    # Define the list of menu options
    options = ['Aggiungi Evento', 'Eventi di Oggi', 'Eventi di Domani', 'Cerca Evento', 'Seleziona Giorno', 'Esci']
    selected_idx = menu_navigation(stdscr, options)
    print(options[selected_idx])
    
    if selected_idx == 0:
        features.add_event.add_event(stdscr)
    elif selected_idx == 1:
        print("eventi di oggi")
    elif selected_idx == 2:
        print("eventi di domani")
    elif selected_idx == 3:
        print("cerca evento")
    elif selected_idx == 4:
        print("seleziona giorno")
    elif selected_idx == 5:
        print("esci")

# Main function to initialize curses
def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.keypad(True)  # Enable keypad mode to capture special keys (e.g., arrows)
    main_menu(stdscr)  # Call the main menu function


# Start the curses application using the wrapper
curses.wrapper(main)  # Ensures proper initialization and cleanup of curses
