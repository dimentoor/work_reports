import pandas as pd
import numpy as np
import save
from fuzzywuzzy import fuzz

# installed_software
is_sheet_name = 'list1'

# (содержит 2 листа в .xlsx файле)
# 1.	На листе unique_sample представлено количество уникальных полей по каждому столбцу исходной таблицы;
# 2.	На листе filtered_software представлены названия установленных на устройствах пользователей программ, их количество и поставщик.
#
# До обработки, в исходном отчете: “Программа” – 735 - количество уникальных записей.
# После обработки: “Программа” – 348 - количество уникальных записей.
# (Способ сокращения количества программ – вычисление "отношения схожести" между двумя строками. Однако результат, представленный в прикрепленных отчетах может потребовать ручной проверки и дообработки.)


class InstalledSoftware:

    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.software = 0
        self.unique = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)
        self.dict = {}

    def save_result(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    def all_samples_installed_software(self):
        self.open_obj.open_file()
        self.unique_sample()
        self.filtered_software()
        self.dict = {
            "unique_sample": self.unique,
            "filtered_software": self.software}

    def unique_sample(self):
        self.unique = self.open_obj.table.nunique().reset_index().rename(columns={'index': 'Поля', 0: 'Количество'})
        self.unique.index = np.arange(1, len(self.unique) + 1)  # new index

        return self.unique

    def filtered_software(self):
        self.software = pd.DataFrame(data=self.open_obj.table[
            ['Программа', 'Поставщик', 'Количество устройств']])

        test_df = self.software

        print(test_df.count())  # check
        # print(test_df)

        test_df['Программа'] = test_df['Программа'].astype(str)

        indexes_to_remove = set()  # Используем set для уникальности индексов

        for index_i, row_i in test_df.iterrows():
            for index_j, row_j in test_df.iterrows():
                if index_i < index_j:  # Чтобы не сравнивать строку с самой собой и избежать парных проверок
                    similarity = fuzz.ratio(row_i['Программа'], row_j['Программа'])
                    if similarity >= 75:  # ???
                        # print(row_i['Программа'], row_j['Программа'])
                        # print(index_i, index_j)
                        # print(similarity)
                        # print("//")
                        indexes_to_remove.add(index_j)
                        index_i += 1
                        index_j += 1

        test_df = test_df.drop(indexes_to_remove).reset_index(drop=True)

        # print(test_df.count())
        self.software = test_df
        self.software.index = np.arange(1, len(self.software) + 1)  # new index

        # print(self.software.count())  # check

        return self.software



