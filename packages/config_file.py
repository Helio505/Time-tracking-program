"""
    This folder is for the config feature.
"""

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
        # cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['above_other_windows', 'False'])
        # cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['dark_bg_graph', 'False'])
        # cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ['high_contrast_mode', 'False'])
        # TODO add default_titlebar, color_graph, focus_on_window
    conn.commit()
    conn.close()


# def above_win_true():
#     conn = sqlite3.connect("local_database.db")
#     cursor = conn.cursor()
#     cursor.execute("UPDATE config set value = 'True' WHERE name = '"+"above_other_windows"+"'")
#     conn.commit()
#     conn.close()

# def above_win_false():
#     conn = sqlite3.connect("local_database.db")
#     cursor = conn.cursor()
#     cursor.execute("UPDATE config set value = 'False' WHERE name = '"+"above_other_windows"+"'")
#     conn.commit()
#     conn.close()