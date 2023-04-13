import basic
import pandas as pd
import numpy as np


# sheet_name_ = 'list1'
#
# path_all = [
#             '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/input_reports/threats_0207.xlsx',
#             '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/input_reports/threats_0125.xlsx',
#             '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/input_reports/threats_1227.xlsx']
#
# save_path_all = [
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/output_reports/REPORT_threats_0207.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/output_reports/REPORT_threats_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/output_reports/REPORT_threats_1227.xlsx']
#
# multiple nasledovanie
class ThreatsReport(basic.Basic):

    def __init__(self, path, sheet_name):
        self.black_list = 0
        self.users = 0
        self.threat_types = 0
        self.types = 0
        self.types_num = 0
        super().__init__(path, sheet_name)

    def save_result(self, filename):
        dict_samples = {"unique_sample": self.unique,
                        "users_sample": self.users,
                        "black_list_sample": self.black_list,
                        "threat_types_sample": self.threat_types,
                        "types_sample": self.types}
        self.writefile(filename, dict_samples)

    # start all functions
    def all_samples_threats(self):
        self.openfile()
        self.unique_sample()
        self.users_sample()
        self.black_list_sample()
        self.threat_types_sample()
        self.types_sample()

    # count  Кол-во угроз for each user (how does it work? or not)
    def black_list_sample(self):
        # по каким полям смотрим
        columns_list = ['Устройство', 'Учетная запись', 'IP-адрес']
        # по какому полю группируем
        groupby_column = 'Учетная запись'
        # имя подсчитываемого поля
        out_column = 'Кол-во угроз'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.black_list = out.sort_values(by=[out_column], ascending=False)
        self.black_list.index = np.arange(1, len(self.black_list) + 1)  # new index

        return self.black_list

    def users_sample(self):
        self.users = pd.DataFrame(data=self.table[
            ['Устройство', 'Учетная запись', 'IP-адрес',
             'Обнаруженный объект', 'Тип объекта']])
        self.users = self.users.groupby(
            ['Устройство', 'Учетная запись'])[
            ['IP-адрес', 'Обнаруженный объект', 'Тип объекта']].value_counts()

        return self.users

    def threat_types_sample(self):
        self.threat_types = pd.DataFrame(data=self.table[
            ['Тип объекта', 'Обнаруженный объект']])
        self.threat_types = self.threat_types.groupby([
            'Тип объекта'])[['Обнаруженный объект']].value_counts()

        return self.threat_types

    def types_sample(self):
        # по каким полям смотрим
        columns_list = ['Тип объекта']
        # по какому полю группируем
        groupby_column = 'Тип объекта'
        # имя подсчитываемого поля
        out_column = 'Кол-во объектов'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.types = out.sort_values(by=[out_column], ascending=False)
        self.types.index = np.arange(1, len(self.types) + 1)  # new index
        # self.types_num = self.types.drop(columns=['Тип объекта'], axis=1)

        return self.types
