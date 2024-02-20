import basic
import pandas as pd
import numpy as np
import save
import locale
from datetime import datetime, timedelta

# program_versions
pv_sheet_name = 'list1'


class ProgramVersions:

    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.program_versions = 0
        self.alive = 0  # new
        self.filtered_df = 0  # new
        # self.updates = 0
        self.unique = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}

    def save_result(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    def all_samples_program_versions(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.program_versions_sample()
        # self.updates_sample()
        self.alive_sample()
        self.dict = {
            "unique_sample": self.unique,
            "program_versions_sample": self.program_versions,
            "alive_sample": self.alive,
            "filtered_alive": self.filtered_df}

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique()

        return self.unique

    def program_versions_sample(self):
        self.program_versions = pd.DataFrame(data=self.open_obj.table[
            ['Программа', 'Номер версии']])
        self.program_versions = self.program_versions.groupby([
            'Программа'])[['Номер версии']].value_counts()  # how to delete column " " created by value_counts()?

        return self.program_versions

    def alive_sample(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        self.alive = pd.DataFrame(data=self.open_obj.table[
            ['Группа', 'Устройство', 'Последнее появление в сети']])

        self.alive['time'] = self.alive[
            'Последнее появление в сети'].apply(lambda x: datetime.strptime(x, '%d %B %Y г. %H:%M:%S'))
        self.alive = self.alive.drop('Последнее появление в сети', axis=1)

        self.alive = self.alive.sort_values(by='time')  # rename column "time"
        self.alive.index = np.arange(1, len(self.alive) + 1)  # new index

        # check info
        # current_date = datetime.now()
        # self.alive['test'] = (current_date - self.alive['time']).dt.days

        current_date = datetime.now()

        self.filtered_df = self.alive[(current_date - self.alive['time']).dt.days >= 7]  # >=7 days?
        self.filtered_df.index = np.arange(1, len(self.filtered_df) + 1)  # new index

        return self.filtered_df

    # def updates_sample(self):
    #     # self.updates = pd.DataFrame(data=self.table[
    #     #     ['Установленные обновления']].value_counts().to_frame())
    #
    #     # по каким полям смотрим
    #     columns_list = ['Установленные обновления']
    #     # по какому полю группируем
    #     groupby_column = 'Установленные обновления'
    #     # имя подсчитываемого поля
    #     out_column = 'Кол-во установленных обновлений'
    #
    #     out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
    #         lambda x: basic.Basic.collapse(x, groupby_column, out_column))
    #
    #     self.updates = out.sort_values(by=[out_column], ascending=False)
    #     self.updates.index = np.arange(1, len(self.updates) + 1)  # new index
    #
    #     return self.updates

