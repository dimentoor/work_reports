import tkinter as tk
from tkinter import filedialog
import threats
import program_versions
import antivirus_bases
import network_attacks
import analyze
import save
import main
from datetime import date
from tkinter import messagebox as mbox


# dynamic form
class Form2(tk.Toplevel):
    threats_objects = list()
    antivirus_bases_objects = list()
    dynamic_th = analyze.Analyzer()
    dynamic_ab = analyze.Analyzer()

    def __init__(self, parent, dynamic_dict):
        super().__init__(parent)
        self.dynamic = dynamic_dict
        self.var = tk.IntVar()
        self.urls_list_open = list()
        self.folder_save = str
        self.urls_list_save = list()  # result save list
        self.current_date = date.today()

        label = tk.Label(self, text="Choose report type")
        radios = [tk.Radiobutton(self, text=key, value=value,
                                 variable=self.var) for key, value in self.dynamic.items()]

        open_btn = tk.Button(self, text="1) Open file", command=self.get_file_names)
        analyze_btn = tk.Button(self, text="2) Analyze", command=self.report_create)
        save_btn = tk.Button(self, text="3) Save reports", command=self.save_files)
        database_btn = tk.Button(self, text="4) Upload to database", command=self.add_to_database)
        close_btn = tk.Button(self, text="Close", command=self.destroy)

        # pack
        label.pack(padx=10, pady=10)
        for radio in radios:
            radio.pack(padx=10, anchor=tk.W)

        open_btn.pack()
        analyze_btn.pack()
        save_btn.pack()
        database_btn.pack()
        close_btn.pack()

    def clear_state(self):
        self.urls_list_open.clear()
        self.urls_list_save.clear()

        self.threats_objects.clear()
        self.antivirus_bases_objects.clear()

    def dict_values(self):
        return self.var.get()

    def get_file_names(self):
        self.urls_list_open.extend(filedialog.askopenfilenames(title='Choose a file'))
        print("---")

    def report_create(self):
        if self.dict_values() == 1:
            # THREATS
            for path in self.urls_list_open:
                Form2.threats_objects.append(threats.ThreatsReport(path, threats.th_sheet_name))
            # (rework)  rewrite like same as above
            for obj in range(len(Form2.threats_objects)):
                Form2.threats_objects[obj].all_samples_threats()
            Form2.dynamic_th.all_samples_th(Form2.threats_objects)

        elif self.dict_values() == 2:
            # ANTIVIRUS_BASES
            for path in self.urls_list_open:
                Form2.antivirus_bases_objects.append(antivirus_bases.AntivirusBases(
                    path, antivirus_bases.ab_sheet_name))
            # (rework) rewrite like same as above
            for obj in range(len(Form2.antivirus_bases_objects)):
                Form2.antivirus_bases_objects[obj].all_samples_antivirus_bases()
            Form2.dynamic_ab.all_samples_ab(Form2.antivirus_bases_objects)

        else:
            output = "Invalid selection"
            print(output)

    def save_files(self):
        self.folder_save = filedialog.askdirectory(title='Choose a directory')

        if self.dict_values() == 1:
            self.urls_list_save.append(
                self.folder_save + "/dynamic_th_" + self.current_date.strftime("%Y-%m-%d") + ".xlsx")
            Form2.dynamic_th.save_result_th(self.urls_list_save[0])

        elif self.dict_values() == 2:
            self.urls_list_save.append(
                self.folder_save + "/dynamic_ab_" + self.current_date.strftime("%Y-%m-%d") + ".xlsx")
            Form2.dynamic_ab.save_result_ab(self.urls_list_save[0])

        else:
            output = "Invalid selection"
            print(output)

        self.clear_state()

    def add_to_database(self):
        if self.dict_values() == 1:
            save.MongoDumper.df_to_json(Form2.dynamic_th.dict, '{}_{}'.format(self.current_date.strftime("%Y-%m-%d"),
                                                                              Form2.dynamic_th.col_name_th))

        elif self.dict_values() == 2:
            save.MongoDumper.df_to_json(Form2.dynamic_ab.dict, '{}_{}'.format(self.current_date.strftime("%Y-%m-%d"),
                                                                              Form2.dynamic_ab.col_name_ab))

        else:
            output = "Invalid selection"
            print(output)


# main form
class App(tk.Tk):
    threats_objects = list()
    antivirus_bases_objects = list()
    network_attacks_objects = list()
    program_versions_objects = list()

    def __init__(self, dict_report):
        super().__init__()
        self.dict = dict_report
        self.var = tk.IntVar()
        self.urls_list_open = list()
        self.folder_save = str
        self.filenames_list = list()  # changed urls_list_open list
        self.urls_list_save = list()  # result save list

        label = tk.Label(self, text="Choose report type")
        radios = [tk.Radiobutton(self, text=key, value=value,
                                 variable=self.var) for key, value in self.dict.items()]

        open_btn = tk.Button(self, text="1) Open file", command=self.get_file_names)
        analyze_btn = tk.Button(self, text="2) Analyze", command=self.report_create)
        save_btn = tk.Button(self, text="3) Save reports", command=self.save_files)
        database_btn = tk.Button(self, text="4) Upload to database", command=self.add_to_database)
        dynamic_btn = tk.Button(self, text="5) Dynamic report", command=self.dynamic_report)
        close_btn = tk.Button(self, text="Close", command=self.destroy)

        # pack
        label.pack(padx=10, pady=10)
        for radio in radios:
            radio.pack(padx=10, anchor=tk.W)

        open_btn.pack()
        analyze_btn.pack()
        save_btn.pack()
        database_btn.pack()
        dynamic_btn.pack()
        close_btn.pack()

    def clear_state(self):
        self.urls_list_open.clear()
        self.filenames_list.clear()
        self.urls_list_save.clear()

        self.threats_objects.clear()
        self.antivirus_bases_objects.clear()
        self.network_attacks_objects.clear()
        self.program_versions_objects.clear()

    def dict_values(self):
        return self.var.get()

    def get_file_names(self):
        self.urls_list_open.extend(filedialog.askopenfilenames(title='Choose a file'))
        # print("------")
        for path in range(len(self.urls_list_open)):
            el = self.urls_list_open[path].rfind('/')
            self.filenames_list.append('/report_' + self.urls_list_open[path][el + 1:])
        print(self.filenames_list)

    def save_files(self):
        self.folder_save = filedialog.askdirectory(title='Choose a directory')

        for path in range(len(self.filenames_list)):
            self.urls_list_save.append(self.folder_save + self.filenames_list[path])

        if self.dict_values() == 1:
            for obj in range(len(App.threats_objects)):
                App.threats_objects[obj].save_result(self.urls_list_save[obj])

        elif self.dict_values() == 2:
            for obj in range(len(App.program_versions_objects)):
                App.program_versions_objects[obj].save_result(self.urls_list_save[obj])

        elif self.dict_values() == 3:
            for obj in range(len(App.antivirus_bases_objects)):
                App.antivirus_bases_objects[obj].save_result(self.urls_list_save[obj])

        elif self.dict_values() == 4:
            for obj in range(len(App.network_attacks_objects)):
                App.network_attacks_objects[obj].save_result(self.urls_list_save[obj])
        else:
            output = "Invalid selection"
            print(output)

        self.clear_state()

    def report_create(self):
        if self.dict_values() == 1:
            # THREATS
            print(len(self.urls_list_open))
            for path in self.urls_list_open:
                App.threats_objects.append(threats.ThreatsReport(path, threats.th_sheet_name))
            # (rework)  rewrite like same as above
            for obj in range(len(App.threats_objects)):
                App.threats_objects[obj].all_samples_threats()

        elif self.dict_values() == 2:
            # PROGRAM_VERSIONS
            for path in self.urls_list_open:
                App.program_versions_objects.append(program_versions.ProgramVersions(
                    path, program_versions.pv_sheet_name))
            # (rework) rewrite like same as above
            for obj in range(len(App.program_versions_objects)):
                App.program_versions_objects[obj].all_samples_program_versions()

        elif self.dict_values() == 3:
            # ANTIVIRUS_BASES
            for path in self.urls_list_open:
                App.antivirus_bases_objects.append(antivirus_bases.AntivirusBases(path, antivirus_bases.ab_sheet_name))
            # (rework) rewrite like same as above
            for obj in range(len(App.antivirus_bases_objects)):
                App.antivirus_bases_objects[obj].all_samples_antivirus_bases()

        elif self.dict_values() == 4:
            # NETWORK_ATTACKS
            for path in self.urls_list_open:
                App.network_attacks_objects.append(network_attacks.NetworkAttacks(path, network_attacks.na_sheet_name))
            # (rework) rewrite like same as above
            for obj in range(len(App.network_attacks_objects)):
                App.network_attacks_objects[obj].all_samples_network_attack()
        else:
            output = "Invalid selection"
            print(output)

        mbox.showinfo("Information", "Analysis is done!")

    def add_to_database(self):
        if self.dict_values() == 1:
            for obj in range(len(App.threats_objects)):
                save.MongoDumper.df_to_json(App.threats_objects[obj].dict,
                                            '{}_{}'.format(obj, App.threats_objects[obj].col_name))
        elif self.dict_values() == 2:
            for obj in range(len(App.program_versions_objects)):
                save.MongoDumper.df_to_json(App.program_versions_objects[obj].dict,
                                            '{}_{}'.format(obj, App.program_versions_objects[obj].col_name))
        elif self.dict_values() == 3:
            for obj in range(len(App.antivirus_bases_objects)):
                save.MongoDumper.df_to_json(App.antivirus_bases_objects[obj].dict,
                                            '{}_{}'.format(obj, App.antivirus_bases_objects[obj].col_name))
        elif self.dict_values() == 4:
            for obj in range(len(App.network_attacks_objects)):
                save.MongoDumper.df_to_json(App.network_attacks_objects[obj].dict,
                                            '{}_{}'.format(obj, App.network_attacks_objects[obj].col_name))
        else:
            output = "Invalid selection"
            print(output)

    def dynamic_report(self):
        dynamic_window = Form2(self, main.dynamic_dict)
        # user = dynamic_window.open()
