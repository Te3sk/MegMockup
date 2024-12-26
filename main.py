# Punto di ingresso dell'app
from features import add_event 
from utils import event_manager as em
import curses
from datetime import datetime
import inspect


def menu_navigation(stdscr, options, message=None):
    """
    Displays a menu and handles navigation using the curses library.
    Args:
        stdscr: The curses window object.
        options (list of str): A list of menu options to display.
    Returns:
        int: The index of the selected option if ENTER is pressed.
            Returns None if the "Esci" option is selected or ESC is pressed.
    The function uses the curses library to create a simple text-based menu.
    It highlights the currently selected option and allows the user to navigate
    using the UP and DOWN arrow keys. The ENTER key selects an option, and the
    ESC key exits the menu.
    """
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
        
        # Display the optional message if provided (not part of the menu)
        if message is not None:
            x_msg = max(0, w // 2 - len(message) // 2)  # Center the message horizontally
            stdscr.addstr(1, x_msg, message, curses.A_BOLD)

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

def today_event(stdscr):
    today = datetime.now().strftime("%Y-%m-%d")
    td_ev = em.get_events_by_date(today)
    if td_ev != []:
        idx = menu_navigation(stdscr, td_ev)
        selected_event = td_ev[idx]
        # TODO - temp debug print
        print(f"{__file__}/{inspect.currentframe().f_code.co_name} - Selected event: {selected_event}")
    else:
        # Mostra il messaggio fisso
        stdscr.clear()
                
        # Mostra solo il menu con "Indietro"
        selected_idx = menu_navigation(stdscr, ["Indietro"], "Nessun evento per oggi")
        
        if selected_idx == 0:  # "Indietro"
            return


# Main menu function
def main_menu(stdscr):
    # Define the list of menu options
    options = ['Aggiungi Evento', 'Eventi di Oggi', 'Eventi di Domani', 'Cerca Evento', 'Seleziona Giorno', 'Esci']
    selected_idx = menu_navigation(stdscr, options)
    
    if selected_idx == 0:
        add_event.main(stdscr)
        main_menu(stdscr)
    elif selected_idx == 1:
        today_event(stdscr)
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
