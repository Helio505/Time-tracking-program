# Time tracking/management app

import time, datetime, sys
from datetime import datetime
from tkinter import *
from tkinter import END
import sqlite3
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from packages.easier import initialize
from packages.config_file import initialize_configs
initialize()
initialize_configs()


from packages.easier import format_tuple, table_name_function
from packages.easier import popup_windows

from packages.dark_mode import dark_mode_color_values
from packages.graph_file import graph, gantt_graph
from packages.dark_mode import dark_false, dark_true

# Some global variables:
dark_mode = True # probably not needed. # if not chosen, dark mode is active.
showing_time = False
time_now = 0
task_name = None
default_titlebar = True

# dark_mode_window()
r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2 = dark_mode_color_values()

def current_time():
    """When it is called, it returns the current time in seconds. It is isolated
    to remove interference from local tkinter stuff."""
    global time_now
    time_now = time.time()
    return time_now

# Main window:
root = Tk()

root.title("Time management app v0.74")
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
entry_box = Entry(root, width=37, bg=e_b_c, fg=f_c_2, font=(18)) # font was 20, x was 200 width was 40
entry_box.place(x=145, y=200)

# Entry to display current time passed:
label_time_passed = Label(root, width=18, height=2, bg=l_b_c, fg="#c7c7c7", font=("Courier", 30)) # relief=RIDGE, borderwidth="1" before
label_time_passed.place(x=150, y=90)



start_time = 0
finish_time = 0

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
    # calc = calc + 400

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
    
    insert_database()
    root.after(2000, clear)


def clear():
    """Just deletes what's in the main entry box:"""
    feedback(button_clear)
    entry_box.delete(0, END)
    # sys.exit()
    # "remove this"


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
        if_null_var = if_null()
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_null_var+" WHERE name = '"+task_name+"'")
        cursor.execute("UPDATE all_tasks set time_spent = "+if_null_var+" WHERE name = '"+task_name+"'")
        # print("done/timespent/null")
    else:
        if_not_null_var = if_not_null()
        cursor.execute("UPDATE "+table_name_function()+" set time_spent = "+if_not_null_var+" WHERE name = '"+task_name+"'")
        cursor.execute("UPDATE all_tasks set time_spent = "+if_not_null_var+" WHERE name = '"+task_name+"'")
        # print("done2/timespent+/NOTnull")

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

    root_show_file.geometry("294x637")
    root_show_file.resizable(width=0, height=0)
    root_show_file.configure(bg=r_w_c)

    # Somehow this scroll feature works, don't change anything here:
    textbox = Text(root_show_file, height=35, width=30, bg=r_w_c, fg=f_c, font=14)
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
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()
    #put feedback here

    # This if for toggle config window:
    global counter_config_window
    counter_config_window += 1
    if counter_config_window == 1:
        root.geometry(f"{700+400}x{335}")
    else:
        counter_config_window = 0
        root.geometry(f"{700}x{335}")
    
    frame_config = Frame(root, bg="yellow", pady=110, padx=120)
    frame_config.place(x=670, y=14)

    info_label = Label(frame_config, font=(10), text="Restart recommended", height=2, width=10, bg="red")
    # info_label.place(x="0", y="0")
    info_label.grid(row=0, column=0)

    # If something is already activated, this will make sure it is shown:
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
    check_toggle_mode = Checkbutton(frame_config, text="text2", font=("Courier", 20), bg="purple", variable=var1, onvalue=1, offvalue=0, command=mode_function)
    check_toggle_mode.grid(row=1, column=0)

    
    # Bar graph:
    var2 = IntVar()
    cursor.execute("SELECT value FROM config WHERE name = 'dark_mode'")
    value = format_tuple(cursor.fetchone(), str).replace("'", "")
    if value == "True":
        var2.set(1)
    else:
        var2.set(0)
    
    def mode_function():
            if var2.get() == 1:
                dark_true()
            else:
                dark_false()
    check_toggle_mode = Checkbutton(frame_config, text="text3", font=("Courier", 20), bg="purple", variable=var2, onvalue=1, offvalue=0, command=mode_function)
    check_toggle_mode.grid(row=2, column=0)


    conn.commit()
    conn.close()

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
        cursor.execute("INSERT INTO all_tasks (name) VALUES (?)", [project_name])
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

# Feedback for the buttons:
def feedback(button_name): #, root, bg_color_feedback, bg_color_original
    """Configures the button to another color,
     then after some miliseconds resets it to the previous color."""
    button_name.configure(bg="green")
    
    def feedback_reset():
        button_name.configure(bg=b_c)

    root.after(100, feedback_reset)

# Buttons:
button_stopwatch_start = Button(root, text=" Start ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: stopwatch_start())
button_stopwatch_finish_calculate = Button(root, text=" Stop ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: stopwatch_finish_calculate())
button_get_name = Button(root, text="Name deactvat", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c)
button_clear = Button(root, text=" Clear ", padx=40, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: clear())
button_show_file = Button(root, text="Show file", padx=28, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: show_file())
button_graph = Button(root, text="Graph", padx=32, pady=20, bg=b_c, fg=f_c, activebackground=b_c, command=lambda: graph_frame())

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

# [this is for testing ----------------------------------------------------------------------------- this is for testing]
def func0():
    gantt_graph()



def func1():
    return
button_test0 = Button(root, text="TEST0", padx=14, pady=6, bg=b_c, activebackground=b_c, fg=f_c, command=lambda: func0())
button_test1 = Button(root, text="TEST1", padx=14, pady=6, bg=b_c, activebackground=b_c, fg=f_c, command=lambda: func1())
button_test0.place(x=620, y=200)
button_test1.place(x=620, y=270)
# [this is for testing ----------------------------------------------------------------------------- this is for testing]

button_config.place(x=15, y=270)

root.mainloop()