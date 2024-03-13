import basic
import gui
import save
import pandas as pd
import numpy as np


class Analyzer:

    def __init__(self):
        self.dblack_list = 0
        # self.dblack_list_parts = 0
        self.res_df = 0
        self.dstatuses = 0
        self.dstatuses_sum = 0
        self.dtypes = 0
        self.dtypes_summ = 0
        self.dict = {}
        self.samples_list = list()

    def save_result_th(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    def save_result_ab(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    # start all functions
    def all_samples_th(self, report_list):
        self.th_dblack_list(report_list)
        self.th_dblack_list_sum(report_list)
        # self.th_dblack_list_parts(report_list)
        self.th_dtypes_summ(report_list)
        self.th_dtypes_part(report_list)
        self.dict = {
            "black_list_pv": self.res_df,
            "black_list_sum_threats": self.dblack_list,
            # "black_list_sum_parts": self.dblack_list_parts,
            "threat_types_summ": self.dtypes_summ,
            "threat_types_parts": self.dtypes}

    # def list_of_reports(self):
    #     self.samples_list = [self.res_df, self.dblack_list, self.dtypes_summ, self.dtypes]
    #     # print(dir(self.samples_list))
    #     return self.samples_list

    def all_samples_ab(self, report_list):
        self.ab_dstatuses_summ(report_list)
        self.ab_dstatuses_part(report_list)
        self.dict = {"ab_statuses_sum": self.dstatuses_sum,
                     "ab_statuses_parts": self.dstatuses}

    # persistent_violators
    def th_dblack_list(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.weighted_users)  # new
            # print(report.black_list.columns.values)  # debug
        self.dblack_list = pd.concat(objects_list)

        unique_count = self.dblack_list['Учетная запись'].value_counts()
        # conversion to df and assigning new column names
        df_value_counts = pd.DataFrame(unique_count)
        df_value_counts = df_value_counts.reset_index()
        df_value_counts.columns = ['Учетная запись', 'Количество вхождений']
        self.res_df = df_value_counts[df_value_counts['Количество вхождений'] >= 4]
        self.res_df.index = np.arange(1, len(self.res_df) + 1)  # new index

        return self.res_df

    # summed_threats_blist
    def th_dblack_list_sum(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.weighted_users)  # new
            # print(report.black_list.columns.values)  # debug
        self.dblack_list = pd.concat(objects_list)
        # the field by which we group
        groupby_column = 'Учетная запись'
        # name of counting field
        # out_column = 'Кол-во угроз'
        out_column = 'Total_Weighted_Count'

        # field with multiple values
        few_values = 'IP-адрес'

        self.dblack_list = self.dblack_list.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column, few_values))
        self.dblack_list = self.dblack_list.sort_values(by=[out_column], ascending=False)
        self.dblack_list.index = np.arange(1, len(self.dblack_list) + 1)  # new index

        return self.dblack_list

    # def th_dblack_list_parts(self, report_list):
    #     objects_list = []
    #     i = 0
    #     for report in report_list:
    #         if i == 0:
    #             objects_list.append(report.black_list)
    #             i += 1
    #         else:
    #             objects_list.append(report.black_list_parts)
    #
    #     self.dblack_list_parts = pd.concat(objects_list, axis=1, ignore_index=True)
    #     self.dblack_list_parts["result"] = self.dblack_list_parts.sum(axis=1, numeric_only=True)
    #     return self.dblack_list_parts

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
        self.dtypes_summ.index = np.arange(1, len(self.dtypes_summ) + 1)  # new index
        return self.dtypes_summ

    def th_dtypes_part(self, report_list):
        i = 0
        merged_df = report_list[0].types
        for report in report_list[1:]:
            merged_df = pd.merge(merged_df, report.types, on='Тип объекта', how='outer', suffixes=('_x', f'_y{i}'))
            # suffixes=[index for index in gui.Form2.reports_indexes])
        merged_df = merged_df.fillna(0)
        self.dtypes = merged_df
        self.dtypes.index = np.arange(1, len(self.dtypes) + 1)  # new index

        return self.dtypes

    def ab_dstatuses_summ(self, report_list):  # summ for the selected period
        objects_list = []
        for report in report_list:
            objects_list.append(report.statuses)
        self.dstatuses_sum = pd.concat(objects_list)

        # по какому полю группируем
        groupby_column = 'Статус антивирусных баз'
        # имя подсчитываемого поля
        out_column = 'Кол-во баз'

        self.dstatuses_sum = self.dstatuses_sum.groupby(
            [groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse_with_sum(x, groupby_column, out_column))
        self.dstatuses_sum = self.dstatuses_sum.sort_values(by=[out_column], ascending=False)
        self.dstatuses_sum.index = np.arange(1, len(self.dstatuses_sum) + 1)  # new index
        return self.dstatuses_sum

    def ab_dstatuses_part(self, report_list):
        objects_list = []
        i = 0
        for report in report_list:
            if i == 0:
                objects_list.append(report.statuses)
                i += 1
            else:
                objects_list.append(report.statuses_num)

        self.dstatuses = pd.concat(objects_list, axis=1, ignore_index=True)
        # self.dstatuses["result"] = self.dstatuses.sum(axis=1, numeric_only=True)  # column "result"
        return self.dstatuses
