# Time tracking/management app
import time
import datetime
from datetime import datetime
from tkinter import *
from tkinter import END
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import sys

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
initialize()

# Some global variables:
dark_mode = True # if not chosen, dark mode is active.
showing_time = False
time_now = 0
task_name = None
default_titlebar = True

def config_from_db():
    return
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE config (name text, value text)")
    except sqlite3.Error as error:
        print(error)

    # Making a list of what already is on the database:
    list_of_configs = []
    for i in cursor.execute("SELECT name FROM config"):
        element = format_tuple(i, str).replace("'", "")
        list_of_configs.append(element)

    configs = ["dark_mode", "more_information"]
    if configs not in list_of_configs:
        cursor.execute("INSERT INTO config (name) VALUES (?)", ('dark_mode'))
        cursor.execute("INSERT INTO config (name) VALUES (?)", ('more_information'))


    def mode():
        text = 'dark_mode'
        if text not in list_of_configs:
            cursor.execute("INSERT INTO config (name, value) VALUES (?, ?)", ('dark_mode', 'True'))
            """check if it is already in database"""

    conn.commit()
    conn.close()
    print(f"-----conn closed at config_from_db-----")

# Dark mode choice window:
def dark_mode_window():
    """Returns the value of dark_mode,
     so that it is applied according to the choice"""
    root_toggle = Tk()
    root_toggle.geometry("150x150")
    root_toggle.configure(bg="#4d4d4d")

    def light():
        global dark_mode
        dark_mode = False
        root_toggle.destroy()

    def dark():
        global dark_mode
        dark_mode = True
        root_toggle.destroy()

    button = Button(root_toggle, text="Light mode", bg="#595959", fg="white", activebackground="#595959", padx="18.7", pady="20", command=light)
    button.place(x=20, y=10)

    button2 = Button(root_toggle, text="Dark mode", bg="#595959", fg="white", activebackground="#595959", padx="20", pady="20", command=dark)
    button2.place(x=20, y=80)

    root_toggle.mainloop()
dark_mode_window()

def dark_mode_color_values():
    """This func changes the values of the colors depending on the user's choice."""
    global r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2

    if dark_mode == True:
        r_w_c = "#4d4d4d"
        e_b_c = "#c7c7c7"
        l_b_c = "#404040"
        b_c = "#595959"
        f_c = "white"
        f_c_2 = "black"
    else:
        r_w_c = "#bdbdb4" # was white
        e_b_c = "#e9e9e4" # was white
        l_b_c = "#e9e9e4" # was white
        b_c = "#bdbdb4" # was white
        f_c = "black"
        f_c_2 = "black"
dark_mode_color_values()

def current_time():
    """When it is called, it returns the current time in seconds. It is isolated
    to remove interference from local tkinter stuff."""
    global time_now
    time_now = time.time()
    return time_now


# Main window:
root = Tk()

root.title("Time management app v0...")
root.geometry("700x335")
root.resizable(width=0, height=0)
root.configure(bg=r_w_c)
root.iconphoto(False, PhotoImage(file="assets\clock_icon2.PNG"))

if default_titlebar == False:
    root.wm_overrideredirect("True")
    # root.update()
    title_bar_frame = Frame(root, bg="#333333", height=20)
    title_bar_frame.pack(expand=1, fill="x", anchor="n")
    title_bar_label = Label(title_bar_frame, text="tttttt", bg="#333333", fg="white", height=2)
    title_bar_label.pack()
    def exit():
        sys.exit()
    exit_button = Button(title_bar_frame, text="X", padx=10, pady=5, command=exit)
    exit_button.place(x='664', y='0')
    def window_drag(e):
        root.geometry(f"+{e.x_root-340}+{e.y_root-15}")

    title_bar_frame.bind("<B1-Motion>", window_drag)

    def something():
        root.overrideredirect(False)
        root.wm_state("iconic")

    exiton = Button(title_bar_frame, text="min", padx=10, pady=5, command=something)
    exiton.place(x='500', y='0')

    

# Entry to receive the name, and display the time:
entry_box = Entry(root, width=40, bg=e_b_c, fg=f_c_2, font=(20))
# entry_box.place(x=5, y=10) this is the old up there
entry_box.place(x=200, y=200)

# Entry to display current time passed:
label_time_passed = Label(root, width=18, height=2, bg=l_b_c, fg="#c7c7c7", font=("Courier", 30)) # relief=RIDGE, borderwidth="1"
label_time_passed.place(x=240, y=80)

start_time = 0
finish_time = 0

# These functions are for the stopwatch
def get_name():
    """This func gets the name of the task,
     if the task doesn't have a name stuff breaks."""
    feedback(button_get_name)

    global task_name
    task_name = entry_box.get()
    entry_box.delete(0, END)

    list_to_ignore = ["", " ", "  ", "   ", "    ", "     "]
    if task_name in list_to_ignore:
        popup_windows("error", "Project needs a name.")
        return 

    entry_box.insert(0, "~~Task was named~~")


def stopwatch_start():
    """Starts the stopwatch"""
    feedback(button_stopwatch_start)
    entry_box.delete(0, END)
    
    global start_time, showing_time
    start_time = time.time()
    showing_time = True
    update()
    
    entry_box.insert(0, "~~started~~")


def stopwatch_finish_calculate():
    """Stops the stopwatch and calculates t1-t0. Also converts everything to
    a format tkinter understands."""
    feedback(button_stopwatch_finish_calculate)

    list_to_ignore = ["", " ", "  ", "   ", "    ", "     "]
    if task_name in list_to_ignore or task_name == None:
        popup_windows("error", "Project needs a valid name.")
        return
    else:
        pass

    entry_box.delete(0, END)

    global finish_time
    finish_time = time.time()

    # if you click directly on stop, this makes sure the app doesn't break.
    if start_time == 0:
        print("something went wrong")
        sys.exit()

    calc = finish_time - start_time
    # calc = 7048.097345113754

    round_calc_sec = round(calc, 2)

    """These if statements and while loops are for the conversion from seconds, to
    minutes, hours, etc."""

    # For seconds:
    if round_calc_sec < 60:
        display_time = ("Tempo decorrido: " + str(round_calc_sec) + " sec")

    # For minutes:
    min = 0
    while round_calc_sec >= 60:
        min = min + 1
        round_calc_sec -= 60

        round_calc_b = round(round_calc_sec, 2)
        display_time = f"Tempo decorrido: {str(min)} min {str(round_calc_b)} s"

    # For hours:
    hour = 0
    while min >= 60:
        hour += 1
        min -= 60
        round_calc_sec -= 60
        display_time = f"Tempo decorrido: [{str(hour)} h / {str(min)} min / {str(round_calc_b)} s]"
    
    entry_box.insert(0, display_time)

    # These lines of code are inserting the values into the .txt file:
    creation_date = datetime.now()
    creation_str_date = str(creation_date)
    with open("tasks saved file.txt", "a") as file:
        file.write(str(task_name) + "\n")     # Task name
        file.write(creation_str_date + "\n")  # When task was created 
        file.write(display_time + "\n"*2)     # Time spent doing the task

    # print(f"round c sec after -- {round_calc_sec}")
    global showing_time, r_c_s
    showing_time = False
    r_c_s = round(calc, 2)
    print(f"TTTTT r_c_s = {r_c_s} TTTTT")
    
    insert_database()
    root.after(2000, clear)


def clear():
    """Just deletes what's in the main entry:"""
    feedback(button_clear)
    entry_box.delete(0, END)
    sys.exit()
    "remove this"

# class facilitate_life():
#     def __init__(self):
#         pass
#     def clear():
#         entry_box.delete(0, END)
#         print("works")

def popup_windows(title: str, message: str):
    popup = messagebox.showerror(title=title, message=message)


def insert_database():
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE " + table_name_function() + " (name text, time_spent real)")
    except sqlite3.Error as error:
        print(error)

    # [code below] Checks to see if the time_spent column is null or not.
    def check_database():
        """This will get the time_spent. This will be added to
         the next time_spent of the same task."""

        cursor.execute("SELECT time_spent FROM "+table_name_function()+" WHERE name = '"+task_name+"'")
        time_spent_before = cursor.fetchone()

        time_spent_before = format_tuple(time_spent_before, str)
        return time_spent_before

    def if_not_null():
        """If time spent isn't NULL, returns time spent now + time spent previously."""
        a = format_tuple(check_database(), float)
        b = str(round((a+r_c_s), 2))
        return b

    def if_null():
        """If time spent is NULL, returns only time spent now."""
        return str(r_c_s)

    # [code below] If the time_spent slot is NULL, goes with one command, if it isn't, goes with another.
    if check_database() == "None":
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_null()+" WHERE name = '"+task_name+"'")
        print("done/timespent/null")
    else:
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_not_null()+" WHERE name = '"+task_name+"'")
        print("done2/timespent+/NOTnull")

    def see_later():
        return
        """The block of code below does the same thing as the func get_elements_for_graph()"""
        global pie_components, legend_components
        pie_components = []
        legend_components = []
        for i in cursor.execute("SELECT name FROM " + table_name):
            name_element = (format_tuple(i, str)).replace("'", "") # here is ' not ''
            legend_components.append(name_element)

        for i in cursor.execute("SELECT time_spent FROM " + table_name):
            try:
                time_spent_element = format_tuple(i, str).replace("'", "")

                if time_spent_element == "None": # null elements will be ignored in the graph.
                    pass
                else:
                    time_spent_element = float(time_spent_element)
                    pie_components.append(time_spent_element)
            except:
                print("----error")

    conn.commit()
    conn.close()
    print(f"-----conn closed at insert_database-----")

def update():
    """Shows the current time passed since the start of the stopwatch.
    It exists because if it didn't you would have to save the task to database to
    see the time, but with this you can see with no influence on other stuff."""
    if showing_time == True:
        current_time()
        keep_track = time_now - start_time
        keep_track_round = round(keep_track, 2)
        label_time_passed.configure(text=(str(keep_track_round), "sec"))
        label_time_passed.after(100, update) # changing the value here, changes the update rate of the clock.
    else:
        label_time_passed.configure(text="0:00:00")
        return
update()


def show_file():
    "Opens in a new window, the file where the tasks are stored."
    feedback(button_show_file)

    with open("tasks saved file.txt") as file:
        test = file.read()


    root_show_file = Tk()

    root.resizable(width=0, height=1)
    root_show_file.geometry("350x806")
    root_show_file.configure(bg=r_w_c)

    # Somehow this scroll feature works, don't change anything here:
    textbox = Text(root_show_file, height=35, width=30, bg=r_w_c, fg=f_c, font=14)
    textbox.insert(END, test)
    textbox.grid(row=0, column=0)
    
    scrollbar = Scrollbar(root_show_file, orient="vertical", command=textbox.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    textbox["yscrollcommand"] = scrollbar.set

    root_show_file.mainloop()


def graph():
    feedback(button_graph)
    def get_elements_for_graph():
        """Gets the elements to build the graph."""
        conn = sqlite3.connect("local_database.db")
        cursor = conn.cursor()
        global pie_components, legend_components
        pie_components = []
        legend_components = []
        for i in cursor.execute("SELECT name FROM " + table_name_function()):
            name_element = (format_tuple(i, str)).replace("'", "") # here is ' not ''

            list_to_ignore = ["", " ", "  ", "   ", "    ", "     ", '', ' ', '  ', '   ', '    ']
            if name_element in list_to_ignore:
                pass
            else:
                legend_components.append(name_element)

        for i in cursor.execute("SELECT time_spent FROM " + table_name_function()):
            try:
                time_spent_element = format_tuple(i, str).replace("'", "")

                if time_spent_element == "None": # null elements will be ignored in the graph.
                    pass
                else:
                    time_spent_element = float(time_spent_element)
                    pie_components.append(time_spent_element)
            except:
                print("----error")

        conn.commit()
        conn.close()
        print(f"-----conn closed at get elements for graph-----")
    get_elements_for_graph()

    def showing_graph():
        pie_components_2 = []
        for i in pie_components:
            if i < 100:
                i = i + 300
            if i < 200:
                i = i + 200
            if i < 300:
                i = i + 100
            pie_components_2.append(i)

        porcentagem2 = round(sum(pie_components_2), 2)

        restante = 86400 - porcentagem2

        pie_components_2.append(restante)
        legend_components.append("unmarked")
    
        plt.pie(pie_components_2)
        plt.legend(legend_components, loc="upper left")
        plt.show()
        # plt.savefig("testfig2",dpi=600)

    


    root.after(250, showing_graph)


# Feedback for the buttons:
def feedback(button_name):
    """Configures the button to another color,
     then after some miliseconds resets it to the previous color."""
    button_name.configure(bg="green")

    def feedback_reset():
        button_name.configure(bg=b_c)

    root.after(100, feedback_reset)


def config_window():
    return
    feedback(button_config)
    """This is the configuration window. Used to change some values."""
    config_from_db()

    root_config = Tk()

    root_config.title("Time management app v0...")
    root_config.geometry("400x200")
    # root.resizable(width=1, height=0)

    """Put +info window here."""
    root_config.configure(bg=r_w_c)


    def placeholderdb():
        return
    
    button_toggle_mode = Button(root_config, text="dark_mode", padx=32, pady=14, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: placeholderdb())
    button_toggle_mode.grid(row=0, column=0)

    button_reset_db = Button(root_config, text="reset_database", padx=32, pady=14, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: placeholderdb())
    button_reset_db.grid(row=1, column=0)

    button_timezone = Button(root_config, text="change_timezone", padx=32, pady=14, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: placeholderdb())
    button_timezone.grid(row=2, column=0)


    def debug():
        conn = sqlite3.connect("local_database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM "+table_name_function()+"")
        print("[][][][]all elements[][][][] -> ", cursor.fetchall())

        conn.commit()
        conn.close()
        print(f"-----conn closed at debug()-----")

    button_debug = Button(root_config, text="debug", padx=32, pady=14, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: debug())
    button_debug.grid(row=3, column=0)
    

    root_config.mainloop()


def add_projects():
    feedback(button_adding)
    """This adds projects to the list of projects."""

    root2 = Tk()
    root2.title("Add projects")
    root2.geometry("280x380")
    root2.configure(bg=r_w_c)

    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE projects (name text)")
    except sqlite3.Error as error:
        print(error)

    entry_box2 = Entry(root2, width=35)
    entry_box2.grid(row=0, column=0)

    def add():
        """Function that starts the process to add a project."""
        project_name = entry_box2.get()

        list_to_ignore = ["", " ", "  ", "   ", "    ", "     "]
        if project_name in list_to_ignore:
            popup_windows("error", "Project needs a name.")
            return 

        entry_box2.delete(0, END)
        cursor.execute("INSERT INTO projects (name) VALUES (?)", [project_name]) # for some reason it wants this comma to work. # for some reason the # second argument has to be a list.
        cursor.execute("INSERT INTO "+table_name_function()+" (name) VALUES (?)", [project_name])
        conn.commit()
        conn.close()
        print(f"-----conn closed at add(add_projects())-----")
        from_the_database()

    def from_the_database():
        """Getting data from the database, to the script and to the list of projects."""
        conn = sqlite3.connect("local_database.db")
        cursor = conn.cursor()

        list_projects.delete(0, END)
        for i in cursor.execute("SELECT name FROM projects"):
            i = format_tuple(i, str).replace("'", "")
            list_projects.insert(0, i)
        conn.commit()
        conn.close()
        print(f"-----conn closed at from_the_database-----")

    def selecting_project(not_useful_parameter):
        """This gets information from the selected project in the list after double click."""

        conn = sqlite3.connect("local_database.db")
        cursor = conn.cursor()

        a = list_projects.curselection()

        project = list_projects.get(a)
        entry_box.insert(0, project) # when double clicked on the item in the list, it goes to the entry box on the main window.
        get_name()
        root2.destroy()

        cursor.execute("SELECT name from "+table_name_function()+"")
        aa = cursor.fetchall()


        list = []
        for i in aa:
            i2 = format_tuple(i, str).replace("'", "")
            list.append(i2)


        if project not in list:
            conn = sqlite3.connect("local_database.db")
            cursor2 = conn.cursor()
            cursor2.execute("INSERT INTO "+table_name_function()+" (name, time_spent) VALUES (?, ?)", [project, None])
            conn.commit()
        conn.close()
        print(f"-----conn closed at selecting_project-----")

    button_add = Button(root2, padx=60, text="add", bg="yellow", activebackground="yellow", command=add)
    button_add.grid(row=1, column=0)

    list_projects = Listbox(root2, selectmode="single", font=(4))
    list_projects.grid(row=2, column=0)
    from_the_database()

    scrollbar = Scrollbar(root2, orient="vertical")
    scrollbar.grid(row=2, column=1, sticky='ns')

    list_projects.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_projects.yview)
    list_projects.bind('<Double-Button-1>', selecting_project)

    root2.mainloop()


# Buttons:
button_stopwatch_start = Button(root, text=" Start ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: stopwatch_start())
button_stopwatch_finish_calculate = Button(root, text=" Stop ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: stopwatch_finish_calculate())
button_get_name = Button(root, text="Name deactvat", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c)
button_clear = Button(root, text=" Clear ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: clear())
button_show_file = Button(root, text="Show file", padx=28, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: show_file())
button_graph = Button(root, text="Graph", padx=32, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: graph())

# button_config icon:
imageOpened = Image.open("assets\config2_icon.png")
im2 = imageOpened.resize((65, 55))
tkimage = ImageTk.PhotoImage(im2)

button_config = Button(root, text="inf", image=tkimage, padx=32, width=90, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: config_window())
button_adding = Button(root, text="add/choose \n projects", padx=28, pady=12, bg=b_c, activebackground=b_c, fg=f_c, command=lambda: add_projects())


# Putting the buttons on the screen
# button_get_name.place(x=2, y=60)
button_stopwatch_start.place(x=2, y=130)
button_stopwatch_finish_calculate.place(x=2, y=200)
button_clear.place(x=125, y=270)
button_adding.place(x=250, y=270)
button_show_file.place(x=383, y=270)
button_graph.place(x=500, y=270)
button_config.place(x=15, y=270)

root.mainloop()
