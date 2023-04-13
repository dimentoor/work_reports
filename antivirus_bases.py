import basic
import pandas as pd
import numpy as np
# sheet_name_ = 'list1'
#
# path_all = [
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/input_reports/antivirus_bases_0207.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/input_reports/antivirus_bases_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/input_reports/antivirus_bases_1227.xlsx']
#
# save_path_all = [
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/output_reports/REPORT_antivirus_bases_0207.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/output_reports/REPORT_antivirus_bases_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/output_reports/REPORT_antivirus_bases_1227.xlsx']


class AntivirusBases(basic.Basic):

    def __init__(self, path, sheet_name):
        self.programs = 0
        self.statuses = 0
        self.statuses_num = 0
        self.users_statuses = 0
        self.pvs_sample = 0
        super().__init__(path, sheet_name)

    def save_result(self, filename):
        dict_unique = {"unique_sample": self.unique,
                       "program_version_status_sample": self.pvs_sample,
                       "users_statuses_sample": self.users_statuses,
                       "programs_sample": self.programs,
                       "statuses_sample": self.statuses}
        self.writefile(filename, dict_unique)

    def all_samples_antivirus_bases(self):
        self.openfile()
        self.unique_sample()
        self.program_version_status_sample()
        self.programs_sample()
        self.statuses_sample()
        self.users_statuses_sample()

    def program_version_status_sample(self):
        self.pvs_sample = pd.DataFrame(data=self.table[
            ['Программа', 'Номер версии', 'Статус антивирусных баз']])
        self.pvs_sample = self.pvs_sample.groupby(
            ['Программа'])[['Номер версии', 'Статус антивирусных баз']].value_counts()

        return self.pvs_sample

    def users_statuses_sample(self):
        self.users_statuses = pd.DataFrame(data=self.table[
            ['Статус антивирусных баз', 'Устройство']])
        self.users_statuses = self.users_statuses.groupby([
            'Статус антивирусных баз'])[['Устройство']].value_counts()

        return self.users_statuses

    def programs_sample(self):
        # по каким полям смотрим
        columns_list = ['Программа']
        # по какому полю группируем
        groupby_column = 'Программа'
        # имя подсчитываемого поля
        out_column = 'Кол-во программ'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.programs = out.sort_values(by=[out_column], ascending=False)
        self.programs.index = np.arange(1, len(self.programs) + 1)  # new index

        return self.programs

    def statuses_sample(self):
        # по каким полям смотрим
        columns_list = ['Статус антивирусных баз']
        # по какому полю группируем
        groupby_column = 'Статус антивирусных баз'
        # имя подсчитываемого поля
        out_column = 'Кол-во баз'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.statuses = out
        self.statuses.index = np.arange(1, len(self.statuses) + 1)  # new index
        self.statuses_num = self.statuses.drop(columns=['Статус антивирусных баз'], axis=1)

        return self.statuses



