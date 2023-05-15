import basic
import save
import urls
import pandas as pd


class Analyzer:
    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.dblack_list = 0
        self.res_df = 0
        self.dstatuses = 0
        self.dtypes = 0
        self.dtypes_summ = 0
        self.open_obj = save.ExcelLoader(self.path, self.sheet_name)

    def save_result_th(self, save_path):
        dict_samples = {"black_list_summed_threats": self.res_df,
                        "black_list_pv": self.dblack_list,
                        "threat_types_summ": self.dtypes_summ,
                        "threat_types_perts": self.dtypes}
        save.ExcelDumper.write_file(save_path, dict_samples)

    def save_result_ab(self, save_path):
        dict_samples = {"ab_statuses_dynamic": self.dstatuses}
        save.ExcelDumper.write_file(save_path, dict_samples)

    # start all functions
    def all_samples_th(self, report_list):
        self.open_obj.open_file()
        self.th_dblack_list(report_list)
        self.th_dblack_list_sum(report_list)
        self.th_dtypes_summ(report_list)
        self.th_dtypes_part(report_list)
        self.ab_dstatuses(report_list)

    def all_samples_ab(self, report_list):
        self.ab_dstatuses(report_list)

    # persistent_violators
    def th_dblack_list(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.black_list)
            # print(report.black_list.columns.values)  # debug
        dblack_list = pd.concat(objects_list)

        unique_count = dblack_list['Устройство'].value_counts()
        # conversion to df and assigning new column names
        df_value_counts = pd.DataFrame(unique_count)
        df_value_counts = df_value_counts.reset_index()
        df_value_counts.columns = ['Устройство', 'Количество вхождений']
        self.res_df = df_value_counts[df_value_counts['Количество вхождений'] == 4]
        # persistent_violators
        self.res_df.to_excel(urls.save_path_unique, sheet_name='unique_count')  # rework

        return self.res_df

    # summed_threats_blist
    def th_dblack_list_sum(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.black_list)
            # print(report.black_list.columns.values)  # debug
        dblack_list = pd.concat(objects_list)
        # the field by which we group
        groupby_column = 'Учетная запись'
        # name of counting field
        out_column = 'Кол-во угроз'
        # field with multiple values
        few_values = 'IP-адрес'

        dblack_list = dblack_list.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column, few_values))
        dblack_list = dblack_list.sort_values(by=[out_column], ascending=False)

        # summed threats black list
        return self.dblack_list

    def th_dtypes_summ(self, report_list):  # summ for the selected period
        objects_list = []
        for report in report_list:
            objects_list.append(report.types)
        self.dtypes_summ = pd.concat(objects_list)

        # по какому полю группируем
        groupby_column = 'Тип объекта'
        # имя подсчитываемого поля
        out_column = 'Кол-во объектов'

        self.dtypes_summ = self.dtypes_summ.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column))
        self.dtypes_summ = self.dtypes_summ.sort_values(by=[out_column], ascending=False)

        return self.dtypes_summ

    # few weeks in one sheet for diagram || should be reworked | have mistakes
    def th_dtypes_part(self, report_list):
        objects_list = []
        i = 0
        for report in report_list:
            if i == 0:
                objects_list.append(report.types)
                i += 1
            else:
                # objects_list.append(report.types_num)
                objects_list.append(report.types)

        dtypes = pd.concat(objects_list, axis=1, ignore_index=True)
        dtypes["result"] = dtypes.sum(axis=1, numeric_only=True)
        # print(test)

        return self.dtypes

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

    # few weeks in one sheet for diagram + summ for all period
    def ab_dstatuses(self, report_list):
        objects_list = []
        i = 0
        for report in report_list:
            if i == 0:
                objects_list.append(report.statuses)
                i += 1
            else:
                objects_list.append(report.statuses_num)

        dstatuses = pd.concat(objects_list, axis=1, ignore_index=True)
        dstatuses["result"] = dstatuses.sum(axis=1, numeric_only=True)

        return self.dstatuses
