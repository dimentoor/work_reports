import basic
import graphics
import save
import pandas as pd
import numpy as np

# threats
th_sheet_name = 'list1'

threats_weight = {
    "Вредоносная ссылка": 30,
    "вредоносные утилиты": 20,
    "червь": 50,
    "вирус": 50,
    "Рекламная программа": 10,
    "Троянская программа": 40,
    "Фишинговая ссылка": 40,
    "другая программа": 20,
    "Опасное поведение": 40,
    "неизвестно": 20}


class ThreatsReport(graphics.Graphics):
    def __init__(self, path, sheet_name, reports_indexes):
        super().__init__(reports_indexes)  # for parent class

        self.path = path
        self.sheet_name = sheet_name
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}
        self.dict_word = {}

        self.black_list = 0
        self.black_list_text = "На листе black_list_sample представлена информация о пользователе (имя учетной " \
                               "записи, IP-адрес) вместе с количеством зафиксированных антивирусным программным " \
                               "обеспечением нарушений."

        self.users = 0
        self.users_text = "На листе users_sample представлена информация о пользователе (имя устройства, IP-адрес, " \
                          "имя учетной записи), а также обнаруженные у них вредоносные объекты, их тип и количество."

        self.threat_types = 0
        self.threat_types_text = "На листе threat_types_sample представлены выявленные вредоносные объекты с " \
                                 "указанием их количества, распределенные по типам."
        self.types = 0
        self.types_text = "На листе types_sample представлены типы вредоносных объектов и их количество."
        self.types_num = 0

        self.unique = 0
        self.unique_text = "Отчет об угрозах \n\n На листе unique_sample представлено количество уникальных полей по " \
                           "каждому столбцу исходной таблицы."

        # self.black_list_parts = 0

        self.weighted_users = 0
        self.weighted_users_word = 0  # only for cut df
        self.weighted_users_text = "На листе weighted_users_sample представлена информация о пользователе (имя " \
                                   "учетной записи, IP-адрес) и условное число “штрафных баллов”, полученных в " \
                                   "результате вычисления произведения количества угроз на вес типа угрозы."

        self.empty_df = pd.DataFrame()  # for dict_word{}
        # self.pie_obj = 0  # graphics
        # self.hist_obj = 0  # graphics

        self.diagram_text = "Диаграмма_"
        for entry in reports_indexes:
            self.diagram_text += entry

    def save_result(self, save_path):  # save excel
        save.ExcelDumper.write_file(save_path, self.dict)

    def save_result_word(self, save_path):  # save word
        save.WordDumper.write_file(save_path, self.dict_word)

    # start all functions
    def all_samples_threats(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.users_sample()
        self.black_list_sample()
        self.threat_types_sample()
        self.types_sample()
        self.dict = {
            "unique_sample": self.unique,
            "users_sample": self.users,
            "weighted_users_sample": self.weighted_users,
            "black_list_sample": self.black_list,
            "types_sample": self.types,
            "threat_types_sample": self.threat_types
        }

        self.dict_word = {
            self.unique_text: self.unique,  # full df
            self.users_text: self.empty_df,
            self.weighted_users_text: self.weighted_users_word,  # 5-10 rows
            self.black_list_text: self.empty_df,
            self.diagram_text: self.create_hist_graphic(),  # new diagram in word
            self.types_text: self.types,  # full df
            self.threat_types_text: self.empty_df
        }

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique().reset_index().rename(columns={'index': 'Поля', 0: 'Количество'})
        self.unique.index = np.arange(1, len(self.unique) + 1)  # new index

        return self.unique

    # can be disabled because of weighted_users_sample -> (threats_count x threats_weight)
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
        # self.black_list_parts = self.black_list.drop(columns=['Учетная запись', 'IP-адрес'], axis=1)

        return self.black_list

    def users_sample(self):  # without 'Обнаруженный объект'
        # all data
        self.users = pd.DataFrame(data=self.open_obj.table[
            ['Устройство', 'Учетная запись', 'IP-адрес',
             'Обнаруженный объект', 'Тип объекта']])
        self.users = self.users.groupby(['Учетная запись', 'Устройство'])[
            ['IP-адрес', 'Обнаруженный объект', 'Тип объекта']].value_counts()  # type - series
        # .reset_index(name='Count')  # type - dataframe
        self.users.name = 'Количество'

        # Total_Weighted_Count
        self.weighted_users = pd.DataFrame(data=self.open_obj.table[
            ['Учетная запись', 'IP-адрес', 'Тип объекта']])
        self.weighted_users = self.weighted_users.groupby(
            ['Учетная запись', 'IP-адрес', 'Тип объекта']).size().reset_index(name='Count')
        # Добавляем веса угроз
        self.weighted_users['Threat_Weight'] = self.weighted_users['Тип объекта'].map(threats_weight)
        self.weighted_users['Weighted_Count'] = self.weighted_users['Count'] * self.weighted_users['Threat_Weight']
        # Группируем по учетной записи и устройству и суммируем взвешенные счетчики
        self.weighted_users = self.weighted_users.groupby(['Учетная запись', 'IP-адрес', ])[
            'Weighted_Count'].sum().reset_index(
            name='Total_Weighted_Count')
        self.weighted_users = self.weighted_users.sort_values(by='Total_Weighted_Count', ascending=False)
        self.weighted_users.index = np.arange(1, len(self.weighted_users) + 1)  # new index

        self.weighted_users_word = self.weighted_users.iloc[:10]  # df for word report (10 rows)
        return self.weighted_users

    def threat_types_sample(self):
        self.threat_types = pd.DataFrame(data=self.open_obj.table[
            ['Тип объекта', 'Обнаруженный объект']])
        self.threat_types = self.threat_types.groupby([
            'Тип объекта'])[['Обнаруженный объект']].value_counts()
        self.threat_types.name = 'Количество'

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

        # self.types = out.sort_values(by=[out_column], ascending=False)
        self.types = out
        self.types.index = np.arange(1, len(self.types) + 1)  # new index
        # self.types = self.types.set_index('Тип объекта')
        # print(self.types)
        self.types_num = self.types.drop(columns=['Тип объекта'], axis=1)

        return self.types

# Graphics
    def create_hist_graphic(self):
        # self.hist_obj = self.hist_diagram(self.types, "Тип объекта", "Кол-во объектов")
        # return self.hist_obj
        return self.hist_diagram(self.types, "Тип объекта", "Кол-во объектов")

    def create_pie_graphic(self):
        return self.pie_diagram(self.types["Кол-во объектов"], self.types["Тип объекта"])

