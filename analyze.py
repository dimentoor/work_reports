import basic
import pandas as pd

# paths should be reworked
save_path_summed = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/debug/03_summed_threats_blist.xlsx'

save_path_unique = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/debug/03_persistent_violators.xlsx'

# save_path_types = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/types_dynamic.xlsx'
# save_path_types_1 = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/types_test.xlsx'

# errors summ
save_path_types = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/debug/03_types_dynamic.xlsx'

# errors summ + fields
save_path_types_1 = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/debug/03_types_test.xlsx'

# save_path_statuses = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/statuses_dynamic.xlsx'
save_path_statuses = '/Users/dmitrybaraboshkin/Documents/работа_ИБ/dynamic_result/debug/03_statuses_dynamic.xlsx'


class Analyzer:
    def __init__(self):
        pass

    # def save_result(self, filename):
    #     dict_samples = {"unique_sample": self.unique,
    #                     "users_sample": self.users,
    #                     "black_list_sample": self.black_list,
    #                     "threat_types_sample": self.threat_types,
    #                     "types_sample": self.types}
    #     self.writefile(filename, dict_samples)

    def th_black_list(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.black_list)
            # print(report.black_list.columns.values)  # debug
        black_list_analyzed = pd.concat(objects_list)

        # duplicates = black_list_analyzed[black_list_analyzed.duplicated(['Устройство', 'Учетная запись'])]
        # duplicates = duplicates.drop(['IP-адрес', 'Кол-во угроз'], axis=1)  # delete useless info
        # print(duplicates)

        unique_count = black_list_analyzed['Устройство'].value_counts()
        # conversion to df and assigning new column names
        df_value_counts = pd.DataFrame(unique_count)
        df_value_counts = df_value_counts.reset_index()
        df_value_counts.columns = ['Устройство', 'Количество вхождений']

        # done, but should be saved in one xlsx file in different sheets
        # persistent_violators
        df_value_counts.to_excel(save_path_unique, sheet_name='unique_count')  # rework

        # the field by which we group
        groupby_column = 'Учетная запись'
        # name of counting field
        out_column = 'Кол-во угроз'
        # field with multiple values
        few_values = 'IP-адрес'

        black_list_analyzed = black_list_analyzed.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column, few_values))
        black_list_analyzed = black_list_analyzed.sort_values(by=[out_column], ascending=False)

        # summed threats black list
        black_list_analyzed.to_excel(save_path_summed, sheet_name='black_list_analyzed')

    def th_types_summ(self, report_list):  # summ for the selected period
        objects_list = []
        for report in report_list:
            objects_list.append(report.types)
        types_analyzed = pd.concat(objects_list)

        # по какому полю группируем
        groupby_column = 'Тип объекта'
        # имя подсчитываемого поля
        out_column = 'Кол-во объектов'

        types_analyzed = types_analyzed.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column))
        types_analyzed = types_analyzed.sort_values(by=[out_column], ascending=False)

        # save analyzed dynamic
        types_analyzed.to_excel(save_path_types, sheet_name='types_dynamic')

    def th_types_parts(self, report_list):  # few weeks in one sheet for diagram
        objects_list = []
        i = 0
        for report in report_list:
            if i == 0:
                objects_list.append(report.types)
                i += 1
            else:
                # objects_list.append(report.types_num)
                objects_list.append(report.types)

        test = pd.concat(objects_list, axis=1, ignore_index=True)
        test["result"] = test.sum(axis=1, numeric_only=True)
        # print(test)

        # save analyzed dynamic
        test.to_excel(save_path_types_1, sheet_name='test')

    # def ab_statuses_summ(self, report_list):  # summ for the selected period
    #     objects_list = []
    #     for report in report_list:
    #         objects_list.append(report.statuses)
    #     statuses_analyzed = pd.concat(objects_list)
    #
    #     # по какому полю группируем
    #     groupby_column = 'Статус антивирусных баз'
    #     # имя подсчитываемого поля
    #     out_column = 'Кол-во баз'
    #
    #     statuses_analyzed = statuses_analyzed.groupby(
    #         [groupby_column], group_keys=False).apply(
    #         lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column))
    #     statuses_analyzed = statuses_analyzed.sort_values(by=[out_column], ascending=False)
    #
    #     # save analyzed dynamic
    #     statuses_analyzed.to_excel(save_path_statuses, sheet_name='statuses_dynamic')

    def ab_statuses_dynamic(self, report_list):  # few weeks in one sheet for diagram + summ for all period
        objects_list = []
        i = 0
        for report in report_list:
            if i == 0:
                objects_list.append(report.statuses)
                i += 1
            else:
                objects_list.append(report.statuses_num)

        dynamic = pd.concat(objects_list, axis=1, ignore_index=True)
        dynamic["result"] = dynamic.sum(axis=1, numeric_only=True)

        # save analyzed dynamic
        dynamic.to_excel(save_path_statuses, sheet_name='statuses_dynamic')
