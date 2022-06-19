# Time-tracking-program

![Version](https://img.shields.io/badge/Version-0.7-lightgrey)

This is the time tracking app I'm developing in Python. I was developing it for some time, now I'm uploading it to GitHub.

How it looks (version 0.7):

<img src=https://user-images.githubusercontent.com/95880348/163757358-de6633e9-30bb-4ab4-bc95-20ce9f005c02.PNG width="550">

<img src=https://user-images.githubusercontent.com/95880348/163757415-66d6465e-3c62-4397-b495-c324dfce5899.PNG width="550">


## How to use:
1. Choose between light and dark mode.
2. Add a project by clicking in the add/choose projects button, writing the name of the pj, then clicking add.
3. Double click the name in the list below, this will choose the project and close the window.
4. Click start, it will start counting.
5. Click stop, it will stop counting, calculate and store the data. The data stored is: the name of the task, and the time spent doing it.
6. Now go to show file(for a text file containing all tasks and time spent) or graph(it will show a pie graph with the tasks of the day))

<br />

- Summary of how it works is: You create a project, then start the clock, when you are done, stop the clock. It will save the name of the task and time spent.
- On the first initialization, the script will create 2 files, one txt, and a .db file.
- If you spend time on a project now then later, it will add the times.

## Recommendations/What you need to have:
- I recommend cloning the whole repository and getting the folder, this build is developed enough that the program is almost usable.
- Task names must only use symbols present in English. Words like à,ç,é,í may not work properly.
- I only tested it on Windows 10.
- Python 3.9.6
- The main libraries are:
  - tkinter -- 8.6
  - Pillow -- 9.0.0
  - matplotlib -- 3.5.1
  - sqlite3 -- 3.35.5
  - time, datetime, sys
- I was able to turn it into a .exe with cx_freeze without much trouble, so I recommend that.
- To visualize databases I recommend this https://sqlitebrowser.org/

obs. information for version 0.70
