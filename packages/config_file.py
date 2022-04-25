import sqlite3
from packages.easier import format_tuple

def initialize_configs():
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    list_of_configs = []
    for i in cursor.execute("SELECT name FROM config"):
        element = format_tuple(i, str).replace("'", "")
        list_of_configs.append(element)

    # this is initializing all config options:
    if list_of_configs == []: # if it is empty it will do this.
        cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['dark_mode', 'False'])
        cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['extra_information', 'False'])
        cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['graph_type', 'BAR'])
    conn.commit()
    conn.close()



