import pandas as pd


class Basic:
    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.table = pd.DataFrame()
        self.unique = 0

    def openfile(self):
        self.table = pd.read_excel(self.path, sheet_name=self.sheet_name)
        print("openfile is done!")

    def writefile(self, filename, samples: dict):
        with pd.ExcelWriter(filename) as writer:
            for sample_name, sample in samples.items():
                sample.to_excel(writer, sheet_name=sample_name)
        print("writefile is done!")

    # create a sapmle with unique field and count it
    def unique_sample(self):
        self.unique = self.table.nunique()

        return self.unique

    # description in work
    @staticmethod
    def collapse(group, dup_name, out_column_name):
        rows_count = len(group.index)

        out = group.drop_duplicates(subset=[dup_name])
        out[out_column_name] = rows_count

        return out

    # универсальный коллапс для 2х случаев:
    # 1) когда есть поля, в которых нужно вывести несколько значений в строке (few_values),
    #    а также просуммировать значения в другой строке
    #
    # 2) когда таких полей нет и нужно просто просуммировать столбец со значениями
    @staticmethod
    def collapse_with_sum(group, dup_name, sum_column_name, few_values=None):
        summ = 0
        long_string = ''
        i = 0
        for index, row in group.iterrows():
            summ += row[sum_column_name]
            if few_values is not None:
                if i != 0:
                    long_string += '; '
                else:
                    i = 1
                long_string += row[few_values]
        out = group.drop_duplicates(subset=[dup_name])
        out[sum_column_name] = summ
        out[few_values] = long_string

        return out

