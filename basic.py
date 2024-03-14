class Basic:
    def __init__(self):
        pass

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

    groupby_column = 'Тип объекта'
    out_column = 'Кол-во объектов'

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

        if few_values is not None:
            out[few_values] = long_string

        return out

