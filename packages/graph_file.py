from packages.easier import format_tuple, table_name_function
import sqlite3
import matplotlib.pyplot as plt

dark_graph = False
graph_type = "BAR"

def graph(feedback_func_bt_par, root):
    """feedback_func_bt_par means -- feedback function with button as parameter.
    - Gets some data from main, and creates graph.
    """
    feedback_func_bt_par
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
    # ------------------- testing changing seconds to minutes in the graph
        global pie_components
        test_element = []
        for i in pie_components:
            i = i / 60
            test_element.append(i)
        
        pie_components = test_element
    # -------------------

        if len(legend_components) != len(pie_components): # to remove problem of index out of range
            pie_components.append(0)

        pie_components_percentage = []
        for i in pie_components:
            percentage = (i / sum(pie_components))*100
            pie_components_percentage.append(round(percentage, 2))

        b = 0
        for i in legend_components:
            legend_components[b] = legend_components[b] + f" [{str(pie_components_percentage[b])}%]"
            b += 1

        print(f"legend = {legend_components}")

        if dark_graph == True:
            plt.style.use('dark_background')
        else:
            pass

        if graph_type == "PIE":
            plt.title("Distribution of time")
            plt.pie(pie_components)
            plt.legend(legend_components, loc="upper left")
            plt.show()
        elif graph_type == "BAR":
            fig, ax = plt.subplots()
            bars = ax.bar(legend_components, pie_components)
            ax.bar_label(bars)
            plt.title("Distribution of time")
            plt.bar(legend_components, pie_components, color="darkgreen", bottom=0, align="center")
            plt.xlabel("Taskname"), plt.ylabel("Time spent (minutes)")
            plt.rc("xtick", labelsize=7)
            plt.show()
        elif graph_type == "DONUT":
            pass
        elif graph_type == "HORIBAR":
            pass
        else:
            pass

        # plt.savefig("testfig2", dpi=600)

    root.after(250, showing_graph)


def gantt_graph():
    return
