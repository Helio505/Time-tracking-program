"""
    This module gets the name of the database, and enables choosing the
    database file.
"""

import os
from tkinter.filedialog import askopenfilename
from tkinter import Tk

def choose_file():
    """
        - Brings the dialog box for choosing files.
        - Goes through the collected database name.
    """
    root_temporary = Tk()
    root_temporary.title("Nothing important here")

    CURRENT_WORKING_DIRECTORY = str(os.getcwd())

    global DATABASE_NAME
    
    database_name_modifiable = "local_database.db" # default
    database_name_modifiable = askopenfilename(initialdir=CURRENT_WORKING_DIRECTORY,
                                    filetypes=(('db files', '*.db'), ('All files', '*.*')))
    if database_name_modifiable == None:
        database_name_modifiable = "local_database.db"
    elif database_name_modifiable in ["", " ", "   ", None]:
        database_name_modifiable = "local_database.db"
    else:
        pass
    
    DATABASE_NAME = database_name_modifiable
    root_temporary.destroy()
    root_temporary.mainloop()
    return DATABASE_NAME

def database_file_path():
    """
        - Returns the database name after all the operations.
    """
    global DATABASE_NAME
    return DATABASE_NAME