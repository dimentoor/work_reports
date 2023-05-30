import basic
import save
import pandas as pd
import numpy as np


class ThreatsReport:
    col_name = 'threats_collection'

    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.black_list = 0
        self.users = 0
        self.threat_types = 0
        self.types = 0
        self.types_num = 0
        self.unique = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}

    def save_result(self, save_path):
        self.dict = {
            "unique_sample": self.unique,
            "users_sample": self.users,
            "black_list_sample": self.black_list,
            "threat_types_sample": self.threat_types,
            "types_sample": self.types}
        save.ExcelDumper.write_file(save_path, self.dict)

    # start all functions
    def all_samples_threats(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.users_sample()
        self.black_list_sample()
        self.threat_types_sample()
        self.types_sample()

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique()

        return self.unique

    # count  Кол-во угроз for each user (how does it work? or not)
    # select ONLY ONE groupby column in all functions
    def black_list_sample(self):
        # по каким полям смотрим
        columns_list = ['Учетная запись', 'IP-адрес']
        # по какому полю группируем
        groupby_column = 'Учетная запись'
        # имя подсчитываемого поля
        out_column = 'Кол-во угроз'

        out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.black_list = out.sort_values(by=[out_column], ascending=False)
        self.black_list.index = np.arange(1, len(self.black_list) + 1)  # new index

        return self.black_list

    # select ONLY ONE groupby column in all functions
    def users_sample(self):
        self.users = pd.DataFrame(data=self.open_obj.table[
            ['Устройство', 'Учетная запись', 'IP-адрес',
             'Обнаруженный объект', 'Тип объекта']])
        self.users = self.users.groupby(
            ['Учетная запись', 'Устройство'])[
            ['IP-адрес', 'Обнаруженный объект', 'Тип объекта']].value_counts()

        return self.users

    def threat_types_sample(self):
        self.threat_types = pd.DataFrame(data=self.open_obj.table[
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

        out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.types = out.sort_values(by=[out_column], ascending=False)
        self.types.index = np.arange(1, len(self.types) + 1)  # new index
        # self.types_num = self.types.drop(columns=['Тип объекта'], axis=1)

        return self.types
