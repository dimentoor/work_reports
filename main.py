import gui


dict_report = {
    "Threats": 1,
    "Program_versions": 2,
    "Antivirus_bases": 3,
    # "Network_attacks": 4,
    "Installed_software": 5}

dynamic_dict = {
    "Threats": 1,
    "Antivirus_bases": 2}

if __name__ == '__main__':

    app = gui.App(dict_report)
    app.mainloop()



