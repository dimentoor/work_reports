import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from datetime import datetime

import copy

import graphics
import installed_software
import threats
import program_versions
import antivirus_bases
import network_attacks
import analyze
import save
import main


# dynamic form
class Form2(tk.Toplevel):
    threats_objects = list()
    antivirus_bases_objects = list()
    # dynamic_th = analyze.Analyzer(reports_indexes=Form2.get_file_names())
    # dynamic_ab = analyze.Analyzer()
    # reports_indexes = list()

    def __init__(self, parent, dynamic_dict):
        super().__init__(parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Рассчитать координаты для центрирования окна
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        # Установить координаты окна
        self.geometry('{}x{}+{}+{}'.format(200, 540, x, y))

        self.dynamic = dynamic_dict
        self.var = tk.IntVar()
        self.urls_list_open = list()
        self.folder_save = str
        self.filenames_list = list()  # changed urls_list_open list
        self.urls_list_save = list()  # result save list
        self.current_date = datetime.now()

        self.filenames_word = list()  # test word
        self.urls_list_save_word = list()  # result save word

        self.reports_indexes = list()  # test for dynamic

        self.dynamic_th = analyze.Analyzer(self.reports_indexes)
        self.dynamic_ab = analyze.Analyzer(self.reports_indexes)

        # buttons
        self.open_btn = tk.Button(self, text="Open file(s)", command=self.get_file_names)
        self.analyze_btn = tk.Button(self, text="Analyze", command=self.report_create)
        self.analyze_btn.configure(state='disabled')
        self.save_btn = tk.Button(self, text="Save report(s)", command=self.save_files)
        self.save_btn.configure(state='disabled')
        self.database_btn = tk.Button(self, text="Upload to database", command=self.add_to_database)
        self.database_btn.configure(state='disabled')
        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.skip_btn = tk.Button(self, text="Skip upload to database", command=self.skip_step)
        self.skip_btn.configure(state='disabled')

        # labels
        label_1 = tk.Label(self, text="Select file(s) for analyze")
        label_2 = tk.Label(self, text="Select report type")

        # radiobutton
        self.radios = [tk.Radiobutton(self, text=key, value=value,
                                      variable=self.var, state='disabled') for key, value in self.dynamic.items()]
        # listbox
        self.path_list = tk.Listbox(self, height=5, selectmode=tk.EXTENDED)

        # pack
        label_1.pack(padx=10, pady=10)

        self.open_btn.pack(fill=X)
        self.path_list.pack(fill=X)

        label_2.pack(padx=10, pady=10)
        for radio in self.radios:
            radio.pack(padx=10, anchor=tk.CENTER)

        self.analyze_btn.pack(fill=X)
        self.database_btn.pack(fill=X)
        self.skip_btn.pack(fill=X)
        self.save_btn.pack(fill=X)
        self.close_btn.pack()

    def clear_state(self):
        self.urls_list_open.clear()
        self.urls_list_save.clear()
        self.filenames_list.clear()

        self.reports_indexes.clear()

        self.filenames_word.clear()  # new word
        self.urls_list_save_word.clear()  # new word

        self.threats_objects.clear()
        self.antivirus_bases_objects.clear()

        self.analyze_btn.configure(state='disabled')
        self.save_btn.configure(state='disabled')
        self.database_btn.configure(state='disabled')
        self.skip_btn.configure(state='disabled')

        for radio in self.radios:
            radio.deselect()

    def skip_step(self):
        self.save_btn.configure(state='normal')
        self.database_btn.configure(state='disabled')
        self.skip_btn.configure(state='disabled')

    def dict_values(self):
        return self.var.get()

    def get_file_names(self):
        self.urls_list_open.extend(filedialog.askopenfilenames(title='Choose a file'))

        for path in range(len(self.urls_list_open)):
            el = self.urls_list_open[path].rfind('/')
            names_ = '/dynamic_' + self.urls_list_open[path][el + 1:]
            # word_str = names_[:-4] + "docx"  # word

            el_index = names_.rfind('_')  #
            names_index = names_[el_index + 1:-5]  #
            if names_index not in self.reports_indexes:  #
                self.reports_indexes.append(names_index)  #

            if names_ not in self.filenames_list:
                self.filenames_list.append(names_)

                self.path_list.insert(path, self.filenames_list[path])
        # self.urls_list_save.append(self.filenames_list[0][0:len(
        #     self.filenames_list[0]) - 5] + "-" + self.filenames_list[-1][-9:-5])

            # if word_str not in self.filenames_word:
            #     self.filenames_word.append(word_str)

        print(self.filenames_list)
        print(self.reports_indexes)  #


        # dynamic_th = analyze.Analyzer(self.reports_indexes)
        # dynamic_ab = analyze.Analyzer(self.reports_indexes)

        if len(self.filenames_list) == 0:
            self.error_message("Open files", "Please select a file")
        else:
            self.urls_list_save.append(self.filenames_list[0][0:len(
                self.filenames_list[0]) - 5] + "-" + self.filenames_list[-1][-9:-5])
            self.info_message("Open files", "Files successfully opened")
            self.analyze_btn.configure(state='normal')
            for radio in self.radios:
                radio.configure(state='normal')

        return self.reports_indexes

    def report_create(self):
        if self.dict_values() == 1:
            # THREATS
            for path in self.urls_list_open:
                Form2.threats_objects.append(threats.ThreatsReport(path, threats.th_sheet_name, self.reports_indexes))
            # (rework)  rewrite like same as above
            for obj in range(len(Form2.threats_objects)):
                Form2.threats_objects[obj].all_samples_threats()
            self.dynamic_th.all_samples_th(Form2.threats_objects)

            # tmp = Form2.dynamic_th
            # graphics_th = graphics.Graphics(tmp, self.dict_values(), self.reports_indexes)  # graphics
            # graphics_th.all_graphics_dynamic()

        elif self.dict_values() == 2:
            # ANTIVIRUS_BASES
            for path in self.urls_list_open:
                Form2.antivirus_bases_objects.append(antivirus_bases.AntivirusBases(
                    path, antivirus_bases.ab_sheet_name, self.reports_indexes))
            # (rework) rewrite like same as above
            for obj in range(len(Form2.antivirus_bases_objects)):
                Form2.antivirus_bases_objects[obj].all_samples_antivirus_bases()
            self.dynamic_ab.all_samples_ab(Form2.antivirus_bases_objects)

            # tmp = Form2.dynamic_ab
            # graphics_ab = graphics.Graphics(tmp, self.dict_values(), self.reports_indexes)  # graphics
            # graphics_ab.all_graphics_dynamic()

        else:
            output = "Invalid selection"
            print(output)

        # mbox.showinfo("Analysis", "Analysis is done!")
        self.database_btn.configure(state='normal')
        self.skip_btn.configure(state='normal')
        self.analyze_btn.configure(state='disabled')
        for radio in self.radios:
            radio.configure(state='disabled')

    def save_files(self):
        self.folder_save = filedialog.askdirectory(title='Choose a directory')
        print(self.folder_save + self.urls_list_save[-1])

        # self.urls_list_save_word.append(self.folder_save + self.filenames_word[path])  # save word

        if self.dict_values() == 1:
            self.dynamic_th.save_result_th(self.folder_save + self.urls_list_save[-1] + '.xlsx')
            self.dynamic_th.save_result_word(self.folder_save + self.urls_list_save[-1] + '.docx')

        elif self.dict_values() == 2:
            self.dynamic_ab.save_result_ab(self.folder_save + self.urls_list_save[-1] + '.xlsx')
            self.dynamic_ab.save_result_word(self.folder_save + self.urls_list_save[-1] + '.docx')

        else:
            output = "Invalid selection"
            print(output)

        # self.info_message("Save", "Files successfully saved")
        self.clear_state()
        self.path_list.delete(0, tk.END)

    def add_to_database(self):
        if self.dict_values() == 1:
            save.MongoDumper.df_to_json(self.dynamic_th.dict,
                                        '{}_{}'.format(self.urls_list_save[0], datetime.now().strftime("/%S")))

        elif self.dict_values() == 2:
            save.MongoDumper.df_to_json(self.dynamic_ab.dict,
                                        '{}_{}'.format(self.urls_list_save[0], datetime.now().strftime("/%S")))

        else:
            output = "Invalid selection"
            print(output)

        self.skip_btn.configure(state='disabled')
        self.save_btn.configure(state='normal')

        self.info_message("Database", "Files successfully added to database")

    @staticmethod
    def info_message(title, message):
        mbox.showinfo(title, message)

    @staticmethod
    def error_message(title, message):
        mbox.showerror(title, message)


# main form
class App(tk.Tk):
    threats_objects = list()
    antivirus_bases_objects = list()
    network_attacks_objects = list()
    program_versions_objects = list()
    installed_software_objects = list()  # new

    # dynamic_th = analyze.Analyzer()
    # dynamic_ab = analyze.Analyzer()

    def __init__(self, dict_report):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Рассчитать координаты для центрирования окна
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        # Установить координаты окна
        self.geometry('{}x{}+{}+{}'.format(200, 540, x, y))

        self.dict = dict_report
        self.var = tk.IntVar()
        self.urls_list_open = list()
        self.folder_save = str
        self.filenames_list = list()  # changed urls_list_open list
        self.urls_list_save = list()  # result save list

        self.filenames_word = list()  # test word
        self.urls_list_save_word = list()  # result save word

        self.reports_indexes = list()  # graphics description

        # buttons
        self.open_btn = tk.Button(self, text="Open file(s)", command=self.get_file_names)
        self.dynamic_btn = tk.Button(self, text="Dynamic report", command=self.dynamic_report)
        self.analyze_btn = tk.Button(self, text="Analyze", command=self.report_create)
        self.analyze_btn.configure(state='disabled')
        self.save_btn = tk.Button(self, text="Save report(s)", command=self.save_files)
        self.save_btn.configure(state='disabled')
        self.database_btn = tk.Button(self, text="Upload to database", command=self.add_to_database)
        self.database_btn.configure(state='disabled')
        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.skip_btn = tk.Button(self, text="Skip upload to database", command=self.skip_step)
        self.skip_btn.configure(state='disabled')
        self.word_report_btn = tk.Button(self, text="Create .docx file", command=self.destroy)  # in work | unite all word doc into one при нижитии открывается окно, в котором можно выбрать документы и потом объединить их
        self.word_report_btn.configure(state='disabled')  # in work

        # labels
        label_1 = tk.Label(self, text="Select file(s) for analyze")
        label_2 = tk.Label(self, text="Select report type")
        self.dynamic_btn.pack(fill=X)

        # radiobutton
        self.radios = [tk.Radiobutton(self, text=key, value=value,
                                      variable=self.var, state='disabled') for key, value in self.dict.items()]

        # listbox
        self.path_list = tk.Listbox(self, height=5, selectmode=tk.EXTENDED)

        # pack
        label_1.pack(padx=10, pady=10)

        self.open_btn.pack(fill=X)
        self.path_list.pack(fill=X)  #

        label_2.pack(padx=10, pady=10)
        for radio in self.radios:
            radio.pack(padx=10, anchor=tk.CENTER)

        self.path_list.pack()  #
        self.analyze_btn.pack(fill=X)
        self.database_btn.pack(fill=X)
        self.skip_btn.pack(fill=X)
        self.save_btn.pack(fill=X)
        # self.word_report_btn.pack()
        self.close_btn.pack()

    def clear_state(self):
        self.urls_list_open.clear()
        self.filenames_list.clear()
        self.urls_list_save.clear()

        self.filenames_word.clear()  # new word
        self.urls_list_save_word.clear()  # new word

        self.reports_indexes.clear()

        self.threats_objects.clear()
        self.antivirus_bases_objects.clear()
        self.network_attacks_objects.clear()
        self.program_versions_objects.clear()
        self.installed_software_objects.clear()  # new

        self.analyze_btn.configure(state='disabled')
        self.save_btn.configure(state='disabled')
        self.database_btn.configure(state='disabled')
        self.skip_btn.configure(state='disabled')
        self.analyze_btn.configure(state='disabled')
        self.dynamic_btn.configure(state='normal')

        for radio in self.radios:
            radio.deselect()

    def skip_step(self):
        self.save_btn.configure(state='normal')
        self.database_btn.configure(state='disabled')
        self.skip_btn.configure(state='disabled')

    def dict_values(self):
        return self.var.get()

    def get_file_names(self):
        self.urls_list_open.extend(filedialog.askopenfilenames(title='Choose a file'))
        for path in range(len(self.urls_list_open)):
            el = self.urls_list_open[path].rfind('/')
            names_ = '/report_' + self.urls_list_open[path][el + 1:]
            word_str = names_[:-4] + "docx"  # word

            el_index = names_.rfind('_')
            names_index = names_[el_index + 1:-5]
            if names_index not in self.reports_indexes:
                self.reports_indexes.append(names_index)

            if names_ not in self.filenames_list:
                self.filenames_list.append(names_)

                self.path_list.insert(path, self.filenames_list[path])

            if word_str not in self.filenames_word:
                self.filenames_word.append(word_str)

        if len(self.filenames_list) == 0:
            self.error_message("Open files", "Please select a file")
        else:
            self.info_message("Open files", "Files successfully opened")
            self.analyze_btn.configure(state='normal')
            for radio in self.radios:
                radio.configure(state='normal')

    def report_create(self):
        if self.dict_values() == 1:
            # THREATS
            print(len(self.urls_list_open))
            for index, path in enumerate(self.urls_list_open):
                App.threats_objects.append(threats.ThreatsReport(path, threats.th_sheet_name, self.reports_indexes[index]))
            for obj in range(len(App.threats_objects)):
                App.threats_objects[obj].all_samples_threats()

            # tmp = copy.deepcopy(App.threats_objects)
            # graphics_th = graphics.Graphics(tmp, self.dict_values(), self.reports_indexes)  # graphics
            # graphics_th.all_graphics()

            # test new word report || can be transformed into func which create word report on button click
            # for obj in range(len(App.threats_objects)):
            #     App.threats_objects[obj].create_word_report()
            # return  # test

        elif self.dict_values() == 2:
            # PROGRAM_VERSIONS
            for path in self.urls_list_open:
                App.program_versions_objects.append(program_versions.ProgramVersions(
                    path, program_versions.pv_sheet_name))
            for obj in range(len(App.program_versions_objects)):
                App.program_versions_objects[obj].all_samples_program_versions()
            # return  # test

        elif self.dict_values() == 3:
            # ANTIVIRUS_BASES
            for index, path in enumerate(self.urls_list_open):
                App.antivirus_bases_objects.append(antivirus_bases.AntivirusBases(path, antivirus_bases.ab_sheet_name, self.reports_indexes[index]))
            for obj in range(len(App.antivirus_bases_objects)):
                App.antivirus_bases_objects[obj].all_samples_antivirus_bases()

            # tmp = copy.deepcopy(App.antivirus_bases_objects)
            # graphics_ab = graphics.Graphics(tmp, self.dict_values(), self.reports_indexes)  # graphics
            # graphics_ab.all_graphics()

            # test new word report || can be transformed into func which create word report on button click
            # for obj in range(len(App.antivirus_bases_objects)):
            #     App.antivirus_bases_objects[obj].create_word_report()
            # return  # test

        elif self.dict_values() == 4:
            # NETWORK_ATTACKS
            for path in self.urls_list_open:
                App.network_attacks_objects.append(network_attacks.NetworkAttacks(path, network_attacks.na_sheet_name))
            for obj in range(len(App.network_attacks_objects)):
                App.network_attacks_objects[obj].all_samples_network_attack()

        elif self.dict_values() == 5:  # new
            # INSTALLED_SOFTWARE
            for path in self.urls_list_open:
                App.installed_software_objects.append(installed_software.InstalledSoftware(
                    path, installed_software.is_sheet_name))
            for obj in range(len(App.installed_software_objects)):
                App.installed_software_objects[obj].all_samples_installed_software()
        else:
            output = "Invalid selection"
            print(output)

        mbox.showinfo("Analysis", "Analysis is done!")
        self.database_btn.configure(state='normal')
        self.skip_btn.configure(state='normal')
        self.analyze_btn.configure(state='disabled')
        self.dynamic_btn.configure(state='disabled')
        for radio in self.radios:
            radio.configure(state='disabled')

    def save_files(self):
        print("-----")
        print(len(App.threats_objects))
        self.folder_save = filedialog.askdirectory(title='Choose a directory')

        for path in range(len(self.filenames_list)):
            self.urls_list_save.append(self.folder_save + self.filenames_list[path])  # save excel
            self.urls_list_save_word.append(self.folder_save + self.filenames_word[path])  # save word

        if self.dict_values() == 1:
            for obj in range(len(App.threats_objects)):
                App.threats_objects[obj].save_result(self.urls_list_save[obj])
                App.threats_objects[obj].save_result_word(self.urls_list_save_word[obj])

        elif self.dict_values() == 2:
            for obj in range(len(App.program_versions_objects)):
                App.program_versions_objects[obj].save_result(self.urls_list_save[obj])
                App.program_versions_objects[obj].save_result_word(self.urls_list_save_word[obj])

        elif self.dict_values() == 3:
            for obj in range(len(App.antivirus_bases_objects)):
                App.antivirus_bases_objects[obj].save_result(self.urls_list_save[obj])
                App.antivirus_bases_objects[obj].save_result_word(self.urls_list_save_word[obj])

        elif self.dict_values() == 4:
            for obj in range(len(App.network_attacks_objects)):
                App.network_attacks_objects[obj].save_result(self.urls_list_save[obj])

        elif self.dict_values() == 5:
            for obj in range(len(App.installed_software_objects)):
                App.installed_software_objects[obj].save_result(self.urls_list_save[obj])
        else:
            output = "Invalid selection"
            print(output)

        self.info_message("Save", "Files successfully saved")
        self.clear_state()
        self.path_list.delete(0, tk.END)

    # "%Y-%m-%d/%S"
    def add_to_database(self):
        if self.dict_values() == 1:  # 1
            for obj in range(len(App.threats_objects)):
                save.MongoDumper.df_to_json(App.threats_objects[obj].dict,
                                            '{}'.format(self.filenames_list[obj][0:len(self.filenames_list[obj]) - 5])
                                            + "_" + datetime.now().strftime("/%S"))
        elif self.dict_values() == 2:  # 2
            for obj in range(len(App.program_versions_objects)):
                save.MongoDumper.df_to_json(App.program_versions_objects[obj].dict,
                                            '{}'.format(self.filenames_list[obj][0:len(self.filenames_list[obj]) - 5])
                                            + "_" + datetime.now().strftime("/%S"))
        elif self.dict_values() == 3:
            for obj in range(len(App.antivirus_bases_objects)):
                save.MongoDumper.df_to_json(App.antivirus_bases_objects[obj].dict,
                                            '{}'.format(self.filenames_list[obj][0:len(self.filenames_list[obj]) - 5])
                                            + "_" + datetime.now().strftime("/%S"))
        elif self.dict_values() == 4:
            for obj in range(len(App.network_attacks_objects)):
                save.MongoDumper.df_to_json(App.network_attacks_objects[obj].dict,
                                            '{}'.format(self.filenames_list[obj][0:len(self.filenames_list[obj]) - 5])
                                            + "_" + datetime.now().strftime("/%S"))
        elif self.dict_values() == 5:
            for obj in range(len(App.installed_software_objects)):
                save.MongoDumper.df_to_json(App.installed_software_objects[obj].dict,
                                            '{}'.format(self.filenames_list[obj][0:len(self.filenames_list[obj]) - 5])
                                            + "_" + datetime.now().strftime("/%S"))
        else:
            output = "Invalid selection"
            print(output)

        self.info_message("Database", "Files successfully added to database")
        self.skip_btn.configure(state='disabled')
        self.save_btn.configure(state='normal')

    def dynamic_report(self):
        return Form2(self, main.dynamic_dict)
        # user = dynamic_window.open()

    @staticmethod
    def info_message(title, message):
        mbox.showinfo(title, message)

    @staticmethod
    def error_message(title, message):
        mbox.showerror(title, message)
