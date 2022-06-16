"""
    This is for all the dark_mode/light_mode stuff.
"""

import sqlite3
from packages.easier import format_tuple

from changing_database import database_file_path
DATABASE_NAME = database_file_path()
# print(f"dbname = {DATABASE_NAME}")

def dark_true():
    "Connects to the db and updates value of dark mode to True"
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE config set value = 'True' WHERE name = '"+"dark_mode"+"'")
    conn.commit()
    conn.close()

def dark_false():
    "Connects to the db and updates value of dark mode to False"
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE config set value = 'False' WHERE name = '"+"dark_mode"+"'")
    conn.commit()
    conn.close()

dark_mode = False
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute("SELECT value FROM config WHERE name = 'dark_mode'")
value = format_tuple(cursor.fetchone(), str).replace("'", "")

# gets dark mode value from database and changes it here:
if value == "True":
    dark_mode = True
else:
    dark_mode = False
conn.commit()
conn.close()

def dark_mode_color_values():
    """
    This func changes the values of the colors depending on the user's choice.
    - One set of colors for dark mode, and one set for light mode.
    """
    global r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2, f_c_3, e_b_c_2, config_icon_path

    if dark_mode == True:
        r_w_c = "#4d4d4d"
        e_b_c = "#c7c7c7"
        l_b_c = "#404040"
        b_c = "#595959"
        f_c = "white"
        f_c_2 = "black"
        f_c_3 = "#c7c7c7"
        e_b_c_2 = "#bbbbbb"
        config_icon_path = "assets\config2_icon.png"
        return r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2, f_c_3, e_b_c_2, config_icon_path
    else:
        r_w_c = "#bdbdb4" # was white
        e_b_c = "#e9e9e4" # was white
        l_b_c = "#e9e9e4" # was white
        b_c = "#bdbdb4" # was white
        f_c = "black"
        f_c_2 = "black"
        f_c_3 = "black"
        e_b_c_2 = "#e9e9e4"
        config_icon_path = "assets\config1_icon.png"
        return r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2, f_c_3, e_b_c_2, config_icon_path