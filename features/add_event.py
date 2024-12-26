import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import file_utils as fu
from utils import date_utils as du
from utils import event_manager as em

import curses
import re

def input_field(stdscr, prompt, max_length=None, optional=False, validation=None, error_message=None):
    """
    Gestisce l'input per un singolo campo.
    """
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        curses.echo()
        user_input = stdscr.getstr().decode('utf-8').strip()
        curses.noecho()

        if optional and user_input == "":
            return None  # Campo opzionale lasciato vuoto

        if not user_input:
            stdscr.addstr(2, 0, "Questo campo è obbligatorio. Premi un tasto per riprovare.")
            stdscr.getch()
            continue

        if max_length and len(user_input) > max_length:
            stdscr.addstr(2, 0, f"Inserito un valore di {len(user_input)} caratteri, massimo consentito {max_length}. Riprova.")
            stdscr.getch()
            continue

        if validation and not validation(user_input):
            stdscr.addstr(2, 0, error_message or "Formato non valido. Riprova.")
            stdscr.getch()
            continue

        return user_input


def add_event(stdscr):
    # Input obbligatori
    title = input_field(stdscr, "Titolo (max 25 caratteri): ", max_length=30)
    date = input_field(stdscr, "Data (formato yyyy-mm-dd): ", validation=lambda x: re.match(r"\d{4}-\d{2}-\d{2}", x), error_message="Formato data non valido, usa yyyy-mm-dd.")
    time = input_field(stdscr, "Ora (formato hh:mm): ", validation=lambda x: re.match(r"\d{2}:\d{2}", x), error_message="Formato ora non valido, usa hh:mm.")
    
    # Input opzionali
    description = input_field(stdscr, "Descrizione (max 300 caratteri, opzionale): ", max_length=300, optional=True)
    location = input_field(stdscr, "Location (max 25 caratteri, opzionale): ", max_length=25, optional=True)
    tags = input_field(stdscr, "Tag (max 10 caratteri ciascuno, separati da virgola, opzionale): ", optional=True)
    
    if tags:
        tags = [tag.strip() for tag in tags.split(',') if len(tag.strip()) <= 10]
    
    em.add_event(title, date, time, description, location)

    return title, date, time, description, location, tags


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    event = add_event(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, "Evento aggiunto con successo!")
    stdscr.addstr(2, 0, f"Titolo: {event[0]}")
    stdscr.addstr(3, 0, f"Data: {event[1]}")
    stdscr.addstr(4, 0, f"Ora: {event[2]}")
    stdscr.addstr(5, 0, f"Descrizione: {event[3]}")
    stdscr.addstr(6, 0, f"Location: {event[4]}")
    stdscr.addstr(7, 0, f"Tag: {', '.join(event[5]) if event[5] else 'Nessuno'}")
    
    stdscr.getch()
    stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
