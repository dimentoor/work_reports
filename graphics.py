import matplotlib.pyplot as plt
from io import BytesIO


class Graphics:
    def __init__(self, reports_indexes):
        self.reports_indexes = reports_indexes

    @staticmethod
    def pie_diagram(data, labels):
        plt.pie(data, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title("Pie_diagram")  # add name of report
        plt.tight_layout()  # Adjust the layout to fit all elements
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        # plt.show()
        return buffer

    @staticmethod
    def hist_diagram(df, labels, data):
        df.plot(kind='bar', x=labels, y=data)
        plt.title("Hist_diagram")
        plt.tight_layout()  # Adjust the layout to fit all elements
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        # plt.show()
        return buffer

    @staticmethod
    def dynamic_bar_diagram(df):
        df.plot.bar()
        plt.show()
        plt.title("Bar_diagram")
        plt.tight_layout()  # Adjust the layout to fit all elements
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        # plt.show()
        return buffer

    @staticmethod
    def dynamic_plot_diagram(df):
        df = df.transpose()
        df.plot()
        plt.legend(fontsize=7, bbox_to_anchor=(1, 0.6))
        # plt.xticks(rotation=90)
        plt.show()
        plt.title("Plot_diagram")
        plt.tight_layout()  # Adjust the layout to fit all elements
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        # plt.show()
        return buffer

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
