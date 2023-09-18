import basic
import pandas as pd
import numpy as np
import save

# program_versions
pv_sheet_name = 'list1'


class ProgramVersions:

    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.program_versions = 0
        self.updates = 0
        self.unique = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}

    def save_result(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    def all_samples_program_versions(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.program_versions_sample()
        self.updates_sample()
        self.dict = {
            "unique_sample": self.unique,
            "program_versions_sample": self.program_versions,
            "updates_sample": self.updates}

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique()

        return self.unique

    def program_versions_sample(self):
        self.program_versions = pd.DataFrame(data=self.open_obj.table[
            ['Программа', 'Номер версии', 'Установленные обновления']])
        self.program_versions = self.program_versions.groupby([
            'Программа'])[['Номер версии', 'Установленные обновления']].value_counts()

        return self.program_versions

    def updates_sample(self):
        # self.updates = pd.DataFrame(data=self.table[
        #     ['Установленные обновления']].value_counts().to_frame())

        # по каким полям смотрим
        columns_list = ['Установленные обновления']
        # по какому полю группируем
        groupby_column = 'Установленные обновления'
        # имя подсчитываемого поля
        out_column = 'Кол-во установленных обновлений'

        out = self.open_obj.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.updates = out.sort_values(by=[out_column], ascending=False)
        self.updates.index = np.arange(1, len(self.updates) + 1)  # new index

        return self.updates
