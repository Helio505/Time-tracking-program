"""
    This folder is for the config feature.
    Has to do with the storage of semi-permanent configs in the database.
"""

import sqlite3
from packages.easier import format_tuple

from changing_database import database_file_path
DATABASE_NAME = database_file_path()

def initialize_configs():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    list_of_configs = []
    for i in cursor.execute("SELECT name FROM config"):
        element = format_tuple(i, str).replace("'", "")
        list_of_configs.append(element)

    # this is initializing all config options:
    if list_of_configs == []: # if it is empty it will do this.
        cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['dark_mode', 'False'])
    conn.commit()
    conn.close()