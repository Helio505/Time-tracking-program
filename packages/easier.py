"""This file is to make the code of the __main__ file more readable."""

import time, sqlite3
from tkinter import messagebox

def format_tuple(tuple_value: tuple, data_type):
    """Turns tuple into str/int/etc without commas or parenthesis.
    Receives the tuple, and returns the formatted value.
    tuple_value = tuple input
    data_type = str, int, float, etc."""

    tuple_value = str(tuple_value)
    tuple_value_1 = tuple_value.replace("(", "")
    tuple_value_2 = tuple_value_1.replace(")", "")
    tuple_value_final = tuple_value_2.replace(",", "")

    tuple_value_final = data_type(tuple_value_final)
    return tuple_value_final

def table_name_function():
    """Creates a name for the table. One table for each day.
    - Takes the day and month from time module, and creates a table name.
    - Returns the table name."""
    table_name_raw = time.gmtime()
    tab2 = (table_name_raw.tm_mday, table_name_raw.tm_mon)
    tab3 = format_tuple(tab2, str)
    tab4 = tab3.replace(" ", "_")
    table_name_final = ("date__" + tab4)
    return table_name_final

def initialize():
    """What to do: start main database, start tables.
    Start storage of configurations. 
    Initializes important files. Initializes functions
    that have to be defined before other things."""

    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE projects (name text)")
    except sqlite3.Error as error:
        print(error)

    try:
        cursor.execute("CREATE TABLE config (name text, value text)")
    except sqlite3.Error as error:
        print(error)

    table_name = table_name_function()
    try:
        cursor.execute("CREATE TABLE " + table_name + " (name text, time_spent real)")
    except sqlite3.Error as error:
        print(error)

    conn.commit()
    conn.close()
    print(f"-----conn closed at initialize func -----")
    print(f"~~Database initialization completed.~~")

def popup_windows(title: str, message: str):
    popup = messagebox.showerror(title=title, message=message)