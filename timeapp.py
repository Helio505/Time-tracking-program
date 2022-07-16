# Time tracking/management app

import time
import datetime
import sys
from datetime import datetime

from tkinter import *
from tkinter import END

import sqlite3
from PIL import Image, ImageTk

from changing_database import choose_file
DATABASE_NAME = choose_file()
print(f"Database_file_being_used = {DATABASE_NAME}")

from packages.easier import initialize
from packages.config_file import initialize_configs
initialize()
initialize_configs()

from packages.easier import format_tuple, table_name_function
from packages.easier import popup_windows, popup_windows_info

from packages.dark_mode import dark_mode_color_values, dark_false, dark_true
from packages.graph_file import graph, graph_with_all_tasks

# Some global variables:
dark_mode = True # probably not needed. # if not chosen, dark mode is active.
showing_time = False
time_now = 0
task_name = None
in_task = False

r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2, f_c_3, e_b_c_2, config_icon_path = dark_mode_color_values()

def current_time():
    """When it is called, it returns the current time in seconds. It is isolated
    to remove interference from local tkinter stuff."""
    global time_now
    time_now = time.time()
    return time_now

# Main window:
root = Tk()

root.title("Time management app v0.81")
root.geometry("700x335")
root.resizable(width=0, height=0)
root.configure(bg=r_w_c)
root.iconphoto(False, PhotoImage(file="assets\clock_icon2.PNG"))

# Entry to receive the name, and display the time:
entry_box = Entry(root,
    width=37, bg=e_b_c, fg=f_c_2, font=(18)) # font was 20, x was 200 width was 40
entry_box.place(x=150, y=220)

label_entry_title = Label(root,
    width=18, text="Event box", height=1,
    bg=l_b_c, fg=f_c_3, font=("Courier", 8)) # relief=RIDGE, borderwidth="1" before
label_entry_title.place(x=150, y=200)

# Entry to display current time passed:
label_time_passed = Label(root,
    width=18, height=2, bg=l_b_c,
    fg=f_c_3, font=("Courier", 30)) # relief=RIDGE, borderwidth="1" before
label_time_passed.place(x=150, y=90)

label_time_passed_title = Label(root,
    width=18, text="Counter", height=1, bg=l_b_c,
    fg=f_c_3, font=("Courier", 8)) # relief=RIDGE, borderwidth="1" before
label_time_passed_title.place(x=150, y=70)

# Entry to input the goal time:
entry_box_goal = Entry(root,
    width=10, bg=e_b_c, fg="#180dea", font=(18))
entry_box_goal.place(x=500, y=220)

label_goal_title = Label(root,
    width=6, text="Goal", height=1,
    bg=l_b_c, fg=f_c_3, font=("Courier", 8)) # relief=RIDGE, borderwidth="1" before
label_goal_title.place(x=500, y=200)

def goal_func():
    goal_time = entry_box_goal.get()
    list_to_ignore = ["", " ", "  ", "   ", "    ", "     ", None]
    if goal_time in list_to_ignore:
        return
    goal_time_converted = int(goal_time)
    return goal_time_converted

def disable_not_in_use_buttons(in_task):
    if in_task == True:
        button_clear.config(state="disabled")
        button_config.config(state="disabled")
        button_get_name.config(state="disabled")
        button_graph.config(state="disabled")
        button_show_file.config(state="disabled")
        button_timeline_plotly.config(state="disabled")
        button_all_tasks.config(state="disabled")
        button_adding.config(state="disabled")
        button_stopwatch_start.config(state="disabled")
    else:
        button_clear.config(state="normal")
        button_config.config(state="normal")
        button_get_name.config(state="normal")
        button_graph.config(state="normal")
        button_show_file.config(state="normal")
        button_timeline_plotly.config(state="normal")
        button_all_tasks.config(state="normal")
        button_adding.config(state="normal")
        button_stopwatch_start.config(state="normal")

start_time = 0
finish_time = 0
start_date = 0
finish_date = 0

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
 
    list_to_ignore = ["", " ", "  ", "   ", "    ", "     ", None]
    if entry_box.get() in list_to_ignore:
        popup_windows("error", "Project needs a valid name. \
        \nSelect or create and select a project first.")
        return
    else:
        pass

    entry_box.delete(0, END)
    
    global start_time, showing_time, start_date
    start_time = time.time()
    start_date = datetime.now()
    showing_time = True
    update()

    goal_time = goal_func()
    def scan_for_goal():
        if goal_time in list_to_ignore:
            return
        if (current_time() - start_time)/60 > goal_time: 
            popup_windows_info("Alert", f"Goal of {goal_time} min reached.")
            return
        root.after(1000, scan_for_goal)
    scan_for_goal()


    def checking_goal():
        table_name_raw = time.localtime()
        possible_seconds = [55, 56, 57, 58, 59, 60]
        if table_name_raw.tm_hour == 23 and table_name_raw.tm_min == 59 and table_name_raw.tm_sec in possible_seconds:
            try:
                stopwatch_finish_calculate()
            except:
                print("EXCEPTION")
            popup_windows_info("Event", """Your task was stopped(and saved) to prevent a bug.\
            \nWaiting 5 seconds is recommended.\
            \nThis will only happen at around 23:59:55 (your timezone).\
            \nThe app will freeze for 5 seconds.""")
            time.sleep(5)
            return
        root.after(500, checking_goal)
    checking_goal()
    global in_task
    in_task = True
    disable_not_in_use_buttons(in_task)

    entry_box.insert(0, f"~~started~~ -> {task_name}")


def stopwatch_finish_calculate():
    """Stops the stopwatch and calculates t1-t0. Also converts everything to
    a format tkinter understands."""
    feedback(button_stopwatch_finish_calculate)
    global in_task
    in_task = False
    disable_not_in_use_buttons(in_task)

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

    round_calc_sec = round(calc, 2)

    """
    These if statements and while loops are for the conversion from seconds, to
    minutes, hours, etc.
    """

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

    global showing_time, r_c_s, finish_date
    showing_time = False
    r_c_s = round(calc, 2)
    finish_date = datetime.now()
    
    insert_database()
    insert_into_all_tasks_database()
    root.after(1000, clear)


def clear():
    """
    Just deletes what's in the main entry box:
    """
    feedback(button_clear)
    entry_box.delete(0, END)


def insert_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE " + table_name_function() + " (name text, time_spent real)")
    except sqlite3.Error as error:
        print(error)

    # [code below] Checks to see if the time_spent column is null or not.
    def check_database():
        """
        This will get the time_spent. This will be added to
         the next time_spent of the same task.
        """

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
        if_null_var = if_null()
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_null_var+" WHERE name = '"+task_name+"'")
    else:
        if_not_null_var = if_not_null()
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_not_null_var+" WHERE name = '"+task_name+"'")

    conn.commit()
    conn.close()
    print(f"-----conn closed at insert_database-----")


def insert_into_all_tasks_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    def check_database_all_tasks_table():
        """
        This will get the time_spent. This will be added to
         the next time_spent of the same task.
        """
        cursor.execute("SELECT time_spent FROM all_tasks WHERE name = '"+task_name+"'")
        time_spent_before = cursor.fetchone()
        time_spent_before = format_tuple(time_spent_before, str)
        return time_spent_before


    def if_not_null():
        """If time spent isn't NULL, returns time spent now + time spent previously."""
        a = format_tuple(check_database_all_tasks_table(), float)
        b = str(round((a+r_c_s), 2))
        return b

    def if_null():
        """If time spent is NULL, returns only time spent now."""
        return str(r_c_s)


    if check_database_all_tasks_table() == "None":
        if_null_var = if_null()
        cursor.execute("UPDATE all_tasks set time_spent = "+if_null_var+" WHERE name = '"+task_name+"'")

        cursor.execute("INSERT INTO all_tasks_log (name, time_spent, starting_date, finishing_date) VALUES (?,?,?,?)",
        [task_name, r_c_s, str(start_date), str(finish_date)])
    else:
        if_not_null_var = if_not_null()
        cursor.execute("UPDATE all_tasks set time_spent = "+if_not_null_var+" WHERE name = '"+task_name+"'")

        cursor.execute("INSERT INTO all_tasks_log (name, time_spent, starting_date, finishing_date) VALUES (?,?,?,?)",
        [task_name, r_c_s, str(start_date), str(finish_date)])

    conn.commit()
    conn.close()
    print(f"-----conn closed at insert_all_tasks_database-----")


def update():
    """Shows the current time passed since the start of the stopwatch.
    It exists because if it didn't you would have to save the task to database to
    see the time, but with this you can see with no influence on other stuff."""
    if showing_time == True:
        current_time()
        keep_track = time_now - start_time
        keep_track_round = round(keep_track, 1)

        round_calc_sec = keep_track_round
        """These if statements and while loops are for the conversion from seconds, to
        minutes, hours, etc."""
        # For seconds:
        if round_calc_sec < 60:
            display_time = f"00:00:{str(round_calc_sec)}"
        # For minutes:
        min = 0
        while round_calc_sec >= 60:
            min = min + 1
            round_calc_sec -= 60
            round_calc_b = round(round_calc_sec, 2)
            display_time = f"00:{str(min)}:{str(round_calc_b)}"
        # For hours:
        hour = 0
        while min >= 60:
            hour += 1
            min -= 60
            round_calc_sec -= 60
            display_time = f"{str(hour)}:{str(min)}:{str(round_calc_b)}"

        label_time_passed.configure(text=(str(display_time)))

        # label_time_passed.configure(text=(str(keep_track_round), "sec")) old version
        label_time_passed.after(150, update) # changing the value here, changes the update rate of the clock.
    else:
        label_time_passed.configure(text="00:00:00")
        return
update()

def show_file():
    "Opens in a new window, the file where the tasks are stored."
    feedback(button_show_file)

    with open("tasks saved file.txt") as file:
        contents_of_file = file.read()

    root_show_file = Tk()

    root_show_file.geometry("293x600")
    root_show_file.title("Task logs")
    root_show_file.resizable(width=0, height=0)
    root_show_file.configure(bg=r_w_c)

    # Somehow this scroll feature works, don't change anything here:
    textbox = Text(root_show_file, height=35, width=30, bg=r_w_c, fg=f_c, font=("Arial", 10), padx=32, pady=22)
    textbox.insert(END, contents_of_file)
    textbox.grid(row=0, column=0)
    
    scrollbar = Scrollbar(root_show_file, orient="vertical", command=textbox.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    textbox["yscrollcommand"] = scrollbar.set

    root_show_file.mainloop()


def graph_frame():
    graph(feedback(button_graph), root)


counter_config_window = 0
def config_window():
    feedback(button_config)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # This if for toggle config window:
    global counter_config_window
    counter_config_window += 1
    if counter_config_window == 1:
        root.geometry(f"{700+400}x{335}")
    else:
        counter_config_window = 0
        root.geometry(f"{700}x{335}")
    
    frame_config = Frame(root, bg="darkgrey", pady=100, padx=50)
    frame_config.place(x=700, y=14)

    info_label = Label(frame_config,
        font=("Courier", 8), text="'Restart needed for all changes.'",
        height=2, width=40, bg="darkgrey")
    info_label.grid(row=0, column=0)

    def for_dark_mode():
        var1 = IntVar()
        cursor.execute("SELECT value FROM config WHERE name = 'dark_mode'")
        value = format_tuple(cursor.fetchone(), str).replace("'", "")
        if value == "True":
            var1.set(1)
        else:
            var1.set(0)
        
        def mode_function():
                if var1.get() == 1:
                    dark_true()
                else:
                    dark_false()
        check_toggle_mode = Checkbutton(frame_config,
            text="Dark mode", font=("Courier", 15), width=10,
            relief="ridge", bg="grey", variable=var1, onvalue=1,
            offvalue=0, command=mode_function)
        check_toggle_mode.grid(row=1, column=0)
    for_dark_mode()
    # check_buttons.for_graph_type()
    # check_buttons.for_keeping_focus_on_window()
    conn.commit()
    conn.close()

def add_projects():
    """This adds projects to the list of projects."""

    root2 = Tk()
    feedback(button_adding)
    root2.title("Add projects")
    root2.geometry("240x270")
    root2.configure(bg=r_w_c)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE projects (name text)")
    except sqlite3.Error as error:
        print(error)
    
    entry_box_naming_project = Entry(root2, width=35, bg=e_b_c_2, fg=f_c_2)
    entry_box_naming_project.grid(row=0, column=0)

   
    def add():
        """Function that starts the process to add a project."""
        project_name = entry_box_naming_project.get()

        list_to_ignore = ["", " ", "  ", "   ", "    ", "     ", None]
        if project_name in list_to_ignore:
            popup_windows("error", "Project needs a name.")
            return

        entry_box_naming_project.delete(0, END)
        cursor.execute("INSERT INTO projects (name) VALUES (?)", [project_name]) # for some reason it wants this comma to work. # for some reason the # second argument has to be a list.
        cursor.execute("INSERT INTO "+table_name_function()+" (name) VALUES (?)", [project_name])
        cursor.execute("INSERT INTO all_tasks (name) VALUES (?)", [project_name])
        conn.commit()
        conn.close()
        print(f"-----conn closed at add(add_projects())-----")
        from_the_database()

    def from_the_database():
        """Getting data from the database, to the script and to the list of projects."""
        conn = sqlite3.connect(DATABASE_NAME)
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

        conn = sqlite3.connect(DATABASE_NAME)
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
            conn = sqlite3.connect(DATABASE_NAME)
            cursor2 = conn.cursor()
            cursor2.execute("INSERT INTO "+table_name_function()+" (name, time_spent) VALUES (?, ?)", [project, None])
            conn.commit()
        conn.close()
        print(f"-----conn closed at selecting_project-----")

    button_add = Button(root2, padx=60, text="add", bg=e_b_c_2, fg=f_c_2, activebackground="yellow", command=add)
    button_add.grid(row=1, column=0)

    list_projects = Listbox(root2, selectmode="single", font=(3), bg=e_b_c_2, fg=f_c_2)
    list_projects.grid(row=2, column=0)
    from_the_database()

    scrollbar = Scrollbar(root2, orient="vertical")
    scrollbar.grid(row=2, column=1, sticky='ns')

    list_projects.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_projects.yview)
    list_projects.bind('<Double-Button-1>', selecting_project)

    root2.mainloop()

# Feedback for the buttons:
def feedback(button_name): #, root, bg_color_feedback, bg_color_original
    """
    Configures the button to another color,
    then after some miliseconds resets it to the previous color.
    """
    button_name.configure(bg="#349544")
    
    def feedback_reset():
        button_name.configure(bg=b_c)

    root.after(75, feedback_reset)

# Buttons:
button_stopwatch_start = Button(root,
    text=" Start ", padx=40, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c,
    command=lambda: stopwatch_start())

button_stopwatch_finish_calculate = Button(root,
    text=" Stop ", padx=40, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c,
    command=lambda: stopwatch_finish_calculate())

button_get_name = Button(root,
    text="Name deactvat", padx=40, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c)

button_clear = Button(root,
    text=" Clear ", padx=40, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c,
    command=lambda: clear())

button_show_file = Button(root,
    text="Show file", padx=28, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c,
    command=lambda: show_file())

button_graph = Button(root,
    text="Graph", padx=32, pady=20, bg=b_c, fg=f_c,
    activebackground=b_c,
    command=lambda: graph_frame())

# button_config icon:
imageOpened = Image.open(config_icon_path)
im2 = imageOpened.resize((53, 51))
tkimage = ImageTk.PhotoImage(im2)

button_config = Button(root,
    text="inf", image=tkimage, padx=32, width=90,
    pady=20, bg=b_c, fg=f_c, activebackground=b_c,
    command=lambda: config_window())

button_adding = Button(root,
    text="add/choose \n projects", padx=28, pady=12,
    bg=b_c, activebackground=b_c, fg=f_c,
    command=lambda: add_projects())

button_stopwatch_start.place(x=2, y=130)
button_stopwatch_finish_calculate.place(x=2, y=200)
button_clear.place(x=125, y=270)
button_adding.place(x=250, y=270)
button_show_file.place(x=383, y=270)
button_graph.place(x=500, y=270)

def all_tasks_graph():
    feedback(button_all_tasks)
    graph_with_all_tasks()

def timeline_plotly_graph():
    feedback(button_timeline_plotly)
    print("Plotly is deactivated, cannot show timeline")
    return
    # import packages.dataframe
    # """
    # The act of importing dataframe, executes all the code in that file and creates the chart.
    # """

button_all_tasks = Button(root,
    text="all_tasks", padx=14, pady=6,
    bg=b_c, activebackground=b_c, fg=f_c,
    command=lambda: all_tasks_graph())

button_timeline_plotly = Button(root,
    text="timeline", padx=14, pady=6,
    bg=b_c, activebackground=b_c, fg=f_c,
    command=lambda: timeline_plotly_graph())

button_timeline_plotly.place(x=612, y=296)
button_all_tasks.place(x=612, y=256)
button_config.place(x=15, y=270)

root.mainloop()