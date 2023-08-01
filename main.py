# import threats
# import program_versions
# import antivirus_bases
# import network_attacks
# import analyze
# import urls
# import save
import gui
from tkinter import Tk
from tkinter import ttk
import database
import pymongo

dict_report = {
    "Threats": 1,
    "Program_versions": 2,
    "Antivirus_bases": 3,
    "Network_attacks": 4}

dynamic_dict = {
    "Threats": 1,
    "Antivirus_bases": 2}

if __name__ == '__main__':
    app = gui.App(dict_report)
    app.mainloop()

