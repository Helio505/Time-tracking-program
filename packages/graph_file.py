"""
    This file is for the graphs.
"""

from packages.easier import format_tuple, table_name_function
import sqlite3
from packages.dark_mode import dark_mode_color_values

r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2, f_c_3, e_b_c_2, config_icon_path = dark_mode_color_values()

#--deactivated
# import matplotlib.pyplot as plt 
#--deactivated

from tkinter import *

from changing_database import database_file_path
DATABASE_NAME = database_file_path()

def bar_true():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE config set value = 'BAR' WHERE name = '"+"graph_type"+"'")
    conn.commit()
    conn.close()

def bar_false():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE config set value = 'PIE' WHERE name = '"+"graph_type"+"'")
    conn.commit()
    conn.close()

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute("SELECT value FROM config WHERE name = 'graph_type'")
value = format_tuple(cursor.fetchone(), str).replace("'", "")

graph_type = value
dark_graph = False

def graph(feedback_func_bt_par, root):
    """feedback_func_bt_par means -- feedback function with button as parameter.
    - Gets some data from main, and creates graph.
    """
    feedback_func_bt_par
    def get_elements_for_graph():
        """Gets the elements to build the graph."""
        conn = sqlite3.connect(DATABASE_NAME)
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
        """ This graph shows time spent on stuff today. """
        global pie_components
        test_element = []
        for sec_elem in pie_components:
            min_elem = sec_elem / 60
            test_element.append(min_elem)
        pie_components = test_element
        
        if len(legend_components) != len(pie_components): # to remove problem of index out of range
            pie_components.append(0) # error division by zero

        pie_components_percentage = []
        for i in pie_components:
            percentage = (i / sum(pie_components))*100
            pie_components_percentage.append(round(percentage, 2))

        b = 0
        for i in legend_components:
            legend_components[b] = legend_components[b] + f" [{str(pie_components_percentage[b])}%]"
            b += 1

        # print(f"legend -- {legend_components} pie -- {pie_components}")
        # print(f"legend -- {legend_components} pie 2 -- {pie_components_percentage}")
        with open("file_current_day.txt", mode="a", encoding="utf-8") as file:
            file.truncate(0)
            file.write(f"[~~Distrib of time(current day)~~]\n\n")
            counter = 0
            for i in legend_components:
                file.write(f"-- {i} --\n")
                file.write(f"{str(round(pie_components[counter], 2))} min \n")
                file.write("\n")
                counter += 1
            file.close()

        def show_file():
            with open("file_current_day.txt") as file:
                contents_of_file = file.read()

            root_show_file = Tk()

            root_show_file.geometry("293x600")
            root_show_file.title("Daily tasks")
            root_show_file.resizable(width=0, height=0)
            root_show_file.configure(bg=r_w_c)

            textbox = Text(root_show_file, height=35, width=30, bg=r_w_c, fg=f_c, font=("Arial", 10), padx=32, pady=22)
            textbox.insert(END, contents_of_file)
            textbox.grid(row=0, column=0)
            
            scrollbar = Scrollbar(root_show_file, orient="vertical", command=textbox.yview)
            scrollbar.grid(row=0, column=1, sticky='ns')

            textbox["yscrollcommand"] = scrollbar.set

            root_show_file.mainloop()
        show_file()


        #--deactivated
        # if dark_graph == True:
        #     plt.style.use('dark_background')
        # else:
        #     pass

        # if graph_type == "PIE":
        #     plt.title("Distribution of time (current day)")
        #     plt.pie(pie_components)
        #     plt.legend(legend_components, loc="upper left")
        #     plt.show()
        # elif graph_type == "BAR":
        #     fig, ax = plt.subplots()
        #     bars = ax.bar(legend_components, pie_components)
        #     ax.bar_label(bars)
        #     plt.title("Distribution of time (current day)")
        #     plt.bar(legend_components, pie_components, color="darkgreen", bottom=0, align="center")
        #     plt.xlabel("Taskname (and % of time tracked)"), plt.ylabel("Time spent (minutes)")
        #     plt.rc("xtick", labelsize=7)
        #     plt.show()
        # elif graph_type == "DONUT":
        #     pass
        # elif graph_type == "HORIBAR":
        #     pass
        # else:
        #     pass
        #--deactivated
    root.after(250, showing_graph)


def graph_with_all_tasks():
    """ This shows all the time spent on each project."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    legend = []
    values = []
    for i in cursor.execute("SELECT name FROM all_tasks").fetchall():
            i = format_tuple(i, str).replace("'", "")
            legend.append(i)

    for i in cursor.execute("SELECT time_spent FROM all_tasks").fetchall():
            if str(i) == "(None,)":
                i = 0
            i = format_tuple(i, float)
            values.append(i)
    
    
    values_in_min = []
    for i in values:
        i = i / 60
        values_in_min.append(i)
    values = values_in_min
    
    conn.commit()
    conn.close()

    with open("file_all_tasks.txt", mode="a", encoding="utf-8") as file:
        file.truncate(0)
        file.write(f"[~~All time spent on tasks~~]\n\n")
        counter = 0
        for i in legend:
            file.write(f"-- {i} --\n")
            file.write(f"{str(round(values[counter], 2))} min \n")
            file.write("\n")
            counter += 1
        file.close()
    

    def show_file():
        with open("file_all_tasks.txt") as file:
            contents_of_file = file.read()

        root_show_file = Tk()

        root_show_file.geometry("293x600")
        root_show_file.title("All tasks")
        root_show_file.resizable(width=0, height=0)
        root_show_file.configure(bg=r_w_c)

        textbox = Text(root_show_file, height=35, width=30, bg=r_w_c, fg=f_c, font=("Arial", 10), padx=32, pady=22)
        textbox.insert(END, contents_of_file)
        textbox.grid(row=0, column=0)
        
        scrollbar = Scrollbar(root_show_file, orient="vertical", command=textbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        textbox["yscrollcommand"] = scrollbar.set

        root_show_file.mainloop()
    show_file()

    #--deactivated
    # fig, ax = plt.subplots()
    # bars = ax.bar(legend, values)
    # ax.bar_label(bars)
    # plt.title("Distribution of time")
    # plt.bar(legend, values, color="darkgreen", bottom=0, align="center")
    # plt.xlabel("Taskname"), plt.ylabel("Time spent (minutes)")
    # plt.rc("xtick", labelsize=7)
    # plt.show()
    #--deactivated
