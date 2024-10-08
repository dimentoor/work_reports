import basic
import pandas as pd
import numpy as np
import save

# antivirus_bases
ab_sheet_name = 'list1'


class AntivirusBases:

    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        # self.programs = 0  # uninformative
        self.statuses = 0
        self.statuses_num = 0
        self.users_statuses = 0
        self.pvs_sample = 0
        self.unique = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}

    def save_result(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

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
            "statuses_sample": self.statuses}

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

        self.pvs_sample.name = 'Count'

        return self.pvs_sample

    def users_statuses_sample(self):
        self.users_statuses = pd.DataFrame(data=self.open_obj.table[
            ['Группа', 'Статус антивирусных баз', 'Устройство']])
        self.users_statuses = self.users_statuses.groupby([
            'Статус антивирусных баз', 'Группа'])[['Устройство']].value_counts()
        self.users_statuses.name = 'Count'

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
