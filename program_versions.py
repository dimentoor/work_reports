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
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}
        self.dict_word = {}

        self.program_versions = 0
        self.program_versions_text = "На листе program_versions_sample представлено количество установленных " \
                                     "обновлений, распределенное по номерам версий программ."

        self.alive = 0
        self.alive_text = "На листе alive_sample представлены имена устройств и их последнее появление в сети."

        self.filtered_df = 0
        self.filtered_df_text = "На листе filtered_alive представлены имена устройств и их последнее появление в " \
                                "сети, отличающиеся от даты произведения анализа отчета на 7 или более дней."
        # self.updates = 0
        self.unique = 0
        self.unique_text = "На листе unique_sample представлено количество уникальных полей по каждому столбцу таблицы."

        self.empty_df = pd.DataFrame()  # for dict_word{}

    def save_result(self, save_path):  # save excel
        save.ExcelDumper.write_file(save_path, self.dict)

    def save_result_word(self, save_path):  # save word
        save.WordDumper.write_file(save_path, self.dict_word)

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
            "filtered_alive": self.filtered_df
        }

        self.dict_word = {
            self.unique_text: self.unique,  # full df
            self.program_versions_text: self.empty_df,  # incorrect display
            self.alive_text: self.empty_df,
            self.filtered_df_text: self.empty_df
        }

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique().reset_index().rename(columns={'index': 'Поля', 0: 'Количество'})
        self.unique.index = np.arange(1, len(self.unique) + 1)  # new index

        return self.unique

    def program_versions_sample(self):
        self.program_versions = pd.DataFrame(data=self.open_obj.table[
            ['Программа', 'Номер версии']])
        self.program_versions = self.program_versions.groupby([
            'Программа'])[['Номер версии']].value_counts()

        self.program_versions.name = 'Количество'

        return self.program_versions

    def alive_sample(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        self.alive = pd.DataFrame(data=self.open_obj.table[
            ['Группа', 'Устройство', 'Последнее появление в сети']])

        self.alive['time'] = self.alive[
            'Последнее появление в сети'].apply(lambda x: datetime.strptime(x, '%d %B %Y г. %H:%M:%S'))
        self.alive = self.alive.drop('Последнее появление в сети', axis=1)

        self.alive = self.alive.sort_values(by='time')
        self.alive.index = np.arange(1, len(self.alive) + 1)  # new index

        # check info
        # current_date = datetime.now()
        # self.alive['test'] = (current_date - self.alive['time']).dt.days

        current_date = datetime.now()

        self.filtered_df = self.alive[(current_date - self.alive['time']).dt.days >= 7]  # >=7 days?
        self.filtered_df.index = np.arange(1, len(self.filtered_df) + 1)  # new index

        return self.filtered_df
