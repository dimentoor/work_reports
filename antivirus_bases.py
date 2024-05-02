import basic
import graphics
import pandas as pd
import numpy as np
import save

# antivirus_bases
ab_sheet_name = 'list1'


class AntivirusBases(graphics.Graphics):

    def __init__(self, path, sheet_name, reports_indexes):
        super().__init__(reports_indexes)  # for parent class

        self.path = path
        self.sheet_name = sheet_name
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}
        self.dict_word = {}

        # self.programs = 0  # uninformative
        # self.programs_text = "На листе programs_sample представлены установленные на АРМ пользователей программы" \
        #                      "и их количество;"

        self.statuses = 0
        self.statuses_text = "На листе statuses_sample представлены типы статусов антивирусных баз и их количество."
        self.statuses_num = 0

        self.users_statuses = 0
        self.users_statuses_text = "На листе users_statuses_sample представлено распределение имен устройств " \
                                   "пользователей и групп, в которых они находятся по статусам антивирусных баз."

        self.pvs_sample = 0
        self.pvs_sample_text = "На листе program_version_status_sample отображена информация об установленных " \
                               "антивирусных программах (в какой группе находятся, какие статусы антивирусных баз " \
                               "имеют, количество каждой из программ)."

        self.unique = 0
        self.unique_text = "Отчет об используемых антивирусных базах \n\n На листе unique_sample представлено " \
                           "количество уникальных полей по каждому столбцу исходной таблицы."

        self.empty_df = pd.DataFrame()  # for dict_word{}
        self.pie_obj = 0  # graphics
        self.hist_obj = 0  # graphics

        self.diagram_text = "Диаграмма_"
        for entry in reports_indexes:
            self.diagram_text += entry

    def save_result(self, save_path):  # save excel
        save.ExcelDumper.write_file(save_path, self.dict)

    def save_result_word(self, save_path):  # save word
        save.WordDumper.write_file(save_path, self.dict_word)

    def all_samples_antivirus_bases(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.program_version_status_sample()
        # self.programs_sample()  # uninformative
        self.statuses_sample()
        self.users_statuses_sample()
        self.dict = {
            "unique_sample": self.unique,
            "program_version_status_sample": self.pvs_sample,
            "users_statuses_sample": self.users_statuses,
            # "programs_sample": self.programs,  # uninformative
            "statuses_sample": self.statuses
        }

        self.dict_word = {
            self.unique_text: self.unique,   # full df
            self.pvs_sample_text: self.empty_df,
            self.users_statuses_text: self.empty_df,
            self.diagram_text: self.create_pie_graphic(),  # new diagram in word
            self.statuses_text: self.statuses  # full df
        }

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique().reset_index().rename(columns={'index': 'Поля', 0: 'Количество'})
        self.unique.index = np.arange(1, len(self.unique) + 1)  # new index

        return self.unique

    # uninformative
    def program_version_status_sample(self):
        self.pvs_sample = pd.DataFrame(data=self.open_obj.table[
            ['Группа', 'Программа', 'Статус антивирусных баз']])
        self.pvs_sample = self.pvs_sample.groupby(
            ['Группа'])[['Программа', 'Статус антивирусных баз']].value_counts()

        self.pvs_sample.name = 'Количество'

        return self.pvs_sample

    def users_statuses_sample(self):
        # series
        # self.users_statuses = pd.DataFrame(data=self.open_obj.table[
        #     ['Группа', 'Статус антивирусных баз', 'Устройство']])
        # self.users_statuses = self.users_statuses.groupby([
        #     'Статус антивирусных баз', 'Группа'])[['Устройство']].value_counts()
        #
        # self.users_statuses.name = 'Количество'

        # dataframe
        self.users_statuses = pd.DataFrame(data=self.open_obj.table[
            ['Группа', 'Статус антивирусных баз', 'Устройство']])
        self.users_statuses = self.users_statuses.groupby([
            'Статус антивирусных баз', 'Группа'])[['Устройство']].value_counts().reset_index(name='Количество')

        self.users_statuses = self.users_statuses.drop(columns=['Количество'])
        return self.users_statuses

    def statuses_sample(self):
        # по каким полям смотрим
        columns_list = ['Статус антивирусных баз']
        # по какому полю группируем
        groupby_column = 'Статус антивирусных баз'
        # имя подсчитываемого поля
        out_column = 'Кол-во баз'

        out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.statuses = out
        self.statuses.index = np.arange(1, len(self.statuses) + 1)  # new index
        self.statuses_num = self.statuses.drop(columns=['Статус антивирусных баз'], axis=1)

        return self.statuses

    # uninformative
    # def programs_sample(self):
    #     # по каким полям смотрим
    #     columns_list = ['Программа']
    #     # по какому полю группируем
    #     groupby_column = 'Программа'
    #     # имя подсчитываемого поля
    #     out_column = 'Кол-во программ'
    #
    #     out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
    #         lambda x: basic.Basic.collapse(x, groupby_column, out_column))
    #
    #     self.programs = out.sort_values(by=[out_column], ascending=False)
    #     self.programs.index = np.arange(1, len(self.programs) + 1)  # new index
    #
    #     return self.programs

    # Graphics
    def create_hist_graphic(self):
        self.hist_obj = self.hist_diagram(self.statuses, "Статус антивирусных баз", "Кол-во баз")
        return self.hist_obj

    def create_pie_graphic(self):
        self.pie_obj = self.pie_diagram(self.statuses["Кол-во баз"], self.statuses["Статус антивирусных баз"])
        return self.pie_obj
