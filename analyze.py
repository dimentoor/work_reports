import basic
import graphics
import save
import pandas as pd
import numpy as np

# Динамика изменений количества типов угроз за период 02.02 – 03.01
# Динамика изменений статусов антивирусных баз за период 02.02 – 03.01


class Analyzer(graphics.Graphics):

    def __init__(self, reports_indexes):
        super().__init__(reports_indexes)  # for parent class
        # self.samples_list = list()
        self.dict = {}
        self.dict_word = {}
# THREATS
        # self.dblack_list_parts = 0
        self.res_df = 0
        self.res_df_text = "На листе black_list_pv представлен список сотрудников, учетные записи которых " \
                           "фигурировали в каждом из ранее обработанных отчетов Касперского за февраль."

        self.dblack_list = 0
        self.dblack_list_text = "На листе black_list_summed_threats представлен список нарушителей за февраль (по " \
                                "обработанным ранее отчетам) с указанием суммы полученных “балов” в результате " \
                                "вычисления следующей формулы: количество угроз* вес типа угрозы."
        self.dblack_list_word = 0

        self.dtypes = 0
        self.dtypes_text = "На листе threat_types_parts представлена таблица типов полученных угроз за февраль (по " \
                           "обработанным ранее отчетам), а также ее графическое отображение."

        self.dtypes_summ = 0
        self.dtypes_summ_text = "На листе threat_types_summ представлена таблица суммы типов полученных угроз за " \
                                "февраль (по обработанным ранее отчетам)."
# ANTIVIRUS BASES
        self.dstatuses = 0
        self.dstatuses_text = "На листе ab_statuses_parts представлена таблица по статусам антивирусных баз за февраль (по обработанным ранее отчетам), а также ее графическое отображение."

        self.dstatuses_sum = 0
        self.dstatuses_sum_text = "На листе ab_statuses_sum представлена сокращенная таблица по статусам антивирусных баз за февраль (по обработанным ранее отчетам)."

        self.empty_df = pd.DataFrame()  # for dict_word{}
        self.diagram_text = "Диаграмма_", reports_indexes
        self.dynamic_plot_text = "Диаграмма_plot", reports_indexes
        self.dynamic_bar_text = "Диаграмма_bar", reports_indexes

    def save_result_word(self, save_path):  # save word
        save.WordDumper.write_file(save_path, self.dict_word)

    def save_result_th(self, save_path):
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
            "threat_types_parts": self.dtypes
        }

        self.dict_word = {
            self.res_df_text: self.empty_df,  # full df
            self.dblack_list_text: self.dblack_list_word,  # 5 rows
            self.diagram_text: self.th_create_pie_graphic(),
            self.dtypes_summ_text: self.dtypes_summ,  # full df
            self.dynamic_bar_text: self.th_create_bar_graphic(),
            self.dtypes_text: self.dtypes,  # full df
            self.dynamic_plot_text: self.th_create_plot_graphic()
        }

    # def list_of_reports(self):
    #     self.samples_list = [self.res_df, self.dblack_list, self.dtypes_summ, self.dtypes]
    #     # print(dir(self.samples_list))
    #     return self.samples_list

# THREATS

    # persistent_violators
    def th_dblack_list(self, report_list):
        objects_list = []
        report_counts = 0  # rework
        for report in report_list:
            report_counts += 1
            objects_list.append(report.weighted_users)  # new
            # print(report.black_list.columns.values)  # debug
        self.dblack_list = pd.concat(objects_list)
        self.dblack_list_word = self.dblack_list.iloc[:5]  # df for word report (5 rows)

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

# Graphics
    def th_create_hist_graphic(self):
        return self.hist_diagram(self.dtypes_summ, 'Тип объекта', 'Кол-во объектов')

    def th_create_pie_graphic(self):
        return self.pie_diagram(self.dtypes_summ["Кол-во объектов"],
                                self.dtypes_summ["Тип объекта"])

    def th_create_bar_graphic(self):
        self.dtypes = self.df_index_conversion(self.dtypes, 'Тип объекта')
        return self.dynamic_bar_diagram(self.dtypes)

    def th_create_plot_graphic(self):
        return self.dynamic_plot_diagram(self.dtypes)

# ANTIVIRUS_BASES

    def save_result_ab(self, save_path):
        save.ExcelDumper.write_file(save_path, self.dict)

    def all_samples_ab(self, report_list):
        self.ab_dstatuses_summ(report_list)
        self.ab_dstatuses_part(report_list)

        self.dict = {"ab_statuses_sum": self.dstatuses_sum,
                     "ab_statuses_parts": self.dstatuses
                     }

        self.dict_word = {
            self.diagram_text: self.ab_create_pie_graphic(),
            self.dstatuses_sum_text: self.dstatuses_sum,  # full df
            self.dstatuses_text: self.dstatuses,  # full df
            self.dynamic_plot_text: self.ab_create_plot_graphic()
        }

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

# Graphics
    def ab_create_hist_graphic(self):
        return self.hist_diagram(self.dstatuses_sum, 'Статус антивирусных баз', 'Кол-во баз')

    def ab_create_pie_graphic(self):
        return self.pie_diagram(self.dstatuses_sum['Кол-во баз'],
                                self.dstatuses_sum['Статус антивирусных баз'])

    def ab_create_bar_graphic(self):
        self.dstatuses = self.df_index_conversion(self.dstatuses, 'Статус антивирусных баз')
        return self.dynamic_bar_diagram(self.dstatuses)

    def ab_create_plot_graphic(self):
        return self.dynamic_plot_diagram(self.dstatuses)
