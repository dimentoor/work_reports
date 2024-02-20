import matplotlib.pyplot as plt


class Graphics:

    def __init__(self, report_list, check_point, reports_indexes):
        self.check_point = check_point  # dict_values, check type of report
        self.report_list = report_list  # list of indexes of opened reports

        self.reports_indexes = reports_indexes

    def clear_state(self):
        self.report_list.clear()

    def all_graphics(self):
        self.create_graphics()
        self.clear_state()

    def create_graphics(self):
        for report in self.report_list:
            if self.check_point == 1:
                # THREATS
                self.pie_diagram(report.types["Кол-во объектов"], report.types["Тип объекта"])
                self.hist_diagram(report.types, "Тип объекта", "Кол-во объектов")

            elif self.check_point == 3:
                # ANTIVIRUS_BASES
                self.pie_diagram(report.statuses["Кол-во баз"], report.statuses["Статус антивирусных баз"])
                self.hist_diagram(report.statuses, "Статус антивирусных баз", "Кол-во баз")

    @staticmethod
    def pie_diagram(data, labels):
        plt.pie(data, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title("Pie_diagram")
        plt.show()

    @staticmethod
    def hist_diagram(df, labels, data):
        df.plot(kind='bar', x=labels, y=data)
        plt.title("Hist_diagram")
        plt.show()

    def all_graphics_dynamic(self):
        self.create_graphics_dynamic()
        # self.clear_state()

    def create_graphics_dynamic(self):
        if self.check_point == 1:
            # THREATS
            # dynamic pie diagram
            self.pie_diagram(self.report_list.dtypes_summ["Кол-во объектов"],
                             self.report_list.dtypes_summ["Тип объекта"])
            # dynamic hist diagram
            self.hist_diagram(self.report_list.dtypes_summ, 'Тип объекта', 'Кол-во объектов')

            # dynamic bar diagram
            self.report_list.dtypes = self.df_index_conversion(self.report_list.dtypes, 'Тип объекта')
            self.dynamic_bar_diagram(self.report_list.dtypes)

            # dynamic plot diagram
            self.dynamic_plot_diagram(self.report_list.dtypes)

        elif self.check_point == 2:
            # ANTIVIRUS_BASES
            # dynamic pie diagram
            self.pie_diagram(self.report_list.dstatuses_sum['Кол-во баз'],
                             self.report_list.dstatuses_sum['Статус антивирусных баз'])
            # dynamic hist diagram
            self.hist_diagram(self.report_list.dstatuses_sum, 'Статус антивирусных баз', 'Кол-во баз')

            # dynamic bar diagram
            self.report_list.dstatuses = self.df_index_conversion(self.report_list.dstatuses, 'Статус антивирусных баз')
            self.dynamic_bar_diagram(self.report_list.dstatuses)

            # dynamic plot diagram
            self.dynamic_plot_diagram(self.report_list.dstatuses)

    @staticmethod
    def dynamic_bar_diagram(df):
        df.plot.bar()
        plt.show()

    @staticmethod
    def dynamic_plot_diagram(df):
        df = df.transpose()
        df.plot()
        plt.legend(fontsize=7, bbox_to_anchor=(1, 0.6))
        # plt.xticks(rotation=90)
        plt.show()

    # преобразует df из analyze. Меняем индексы на полученные из имен открытых отчетов
    # добавляем их в df, а также меняем 0 индекс на имя столбца текстовых данных из первичных(не динамических) отчетов
    # в итоге получаем df, где вместо индексов - 1 столбец таблицы из analyze
    # + подписанные столбцы из имен открытх отчетов
    def df_index_conversion(self, df, col_name):
        index_list = df.columns.tolist()
        key_list = df.columns.tolist()
        for item in range(len(index_list)):
            if item > 0:
                index_list[item] = self.reports_indexes[item - 1]
            else:
                index_list[item] = col_name

        index_dict = dict(map(lambda i, j: (i, j), key_list, index_list))
        df.rename(columns=index_dict, inplace=True)
        df = df.set_index(df[col_name])
        df = df.drop(columns=[col_name], axis=1)

        return df

