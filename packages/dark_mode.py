"""This is for all the dark_mode stuff"""

from tkinter import Tk, Button

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
        return r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2
    else:
        r_w_c = "#bdbdb4" # was white
        e_b_c = "#e9e9e4" # was white
        l_b_c = "#e9e9e4" # was white
        b_c = "#bdbdb4" # was white
        f_c = "black"
        f_c_2 = "black"
        return r_w_c, e_b_c, l_b_c, b_c, f_c, f_c_2 