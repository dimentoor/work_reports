import basic
import pandas as pd
import numpy as np

# sheet_name_ = 'list1'
#
# path_all = [
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/input_reports/attack_1_0207.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0130/input_reports/attack_1_0130.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/input_reports/attack_1_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/input_reports/attack_2_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/input_reports/attack_1_1227.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/input_reports/attack_2_1227.xlsx']
#
# save_path_all = [
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0207/output_reports/REPORT_attack_1_0207.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0130/output_reports/REPORT_attack_1_0130.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/output_reports/REPORT_attack_1_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_0125/output_reports/REPORT_attack_2_0125.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/output_reports/REPORT_attack_1_1227.xlsx',
#     '/Users/dmitrybaraboshkin/Documents/работа_ИБ/for_analysis_1227/output_reports/REPORT_attack_2_1227.xlsx']


class NetworkAttacks(basic.Basic):

    def __init__(self, path, sheet_name):
        self.attacker_victim_1 = 0
        self.attacker_victim_2 = 0
        self.attacks = 0
        self.date_time_attack = 0
        self.date_attack = 0
        super().__init__(path, sheet_name)

    def save_result(self, filename):
        dict_unique = {"unique_sample": self.unique,
                       "attacks_sample": self.attacks,
                       "attacker_victim_sample_1": self.attacker_victim_1,
                       "attacker_victim_sample_2": self.attacker_victim_2,
                       "date_time_attack_sample": self.date_time_attack,
                       "date_attack_sample": self.date_attack}
        self.writefile(filename, dict_unique)

    def all_samples_network_attack(self):
        self.openfile()
        self.unique_sample()
        self.attacks_sample()
        self.attacker_victim_sample_1()
        self.attacker_victim_sample_2()
        self.date_time_attacks_sample()
        self.date_attacks_sample()

    def attacker_victim_sample_1(self):
        self.attacker_victim_1 = pd.DataFrame(data=self.table[
            ['Атакующий адрес', 'Атака', 'IP-адрес']].value_counts().to_frame())

        return self.attacker_victim_1

    def attacker_victim_sample_2(self):  # if this sample has differences with "1" above should rework it (collapse)
        # по каким полям смотрим
        columns_list = ['Атакующий адрес', 'Атака', 'IP-адрес']
        # по какому полю группируем
        groupby_column = 'Атакующий адрес'
        # имя подсчитываемого поля
        out_column = 'Кол-во атак'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.attacker_victim_2 = out.sort_values(by=[out_column], ascending=False)
        self.attacker_victim_2.index = np.arange(1, len(self.attacker_victim_2) + 1)  # new index

        return self.attacker_victim_2

    def attacks_sample(self):
        # по каким полям смотрим
        columns_list = ['Атака']
        # по какому полю группируем
        groupby_column = 'Атака'
        # имя подсчитываемого поля
        out_column = 'Кол-во атак'

        out = self.table[columns_list].groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.attacks = out.sort_values(by=[out_column], ascending=False)
        self.attacks.index = np.arange(1, len(self.attacks) + 1)  # new index

        return self.attacks

    def date_time_attacks_sample(self):
        # can be rework
        self.date_time_attack = pd.DataFrame(data=self.table
            ['Время атаки'])

        # new data frame with split value columns
        divide_1 = self.date_time_attack["Время атаки"].str.split(".", n=1, expand=True)
        # making separate first name column from new data frame
        self.date_time_attack["Day"] = divide_1[0]
        # making separate last name column from new data frame
        self.date_time_attack["Time1"] = divide_1[1]
        # Dropping old Name columns
        self.date_time_attack.drop(columns=["Время атаки"], inplace=True)

        divide_2 = self.date_time_attack["Time1"].str.split(":", n=2, expand=True)
        self.date_time_attack["time"] = divide_2[0].astype(float)
        self.date_time_attack["2"] = divide_2[1]
        self.date_time_attack["3"] = divide_2[2]

        self.date_time_attack.drop(columns=["Time1"], inplace=True)
        self.date_time_attack.drop(columns=["2"], inplace=True)
        self.date_time_attack.drop(columns=["3"], inplace=True)

        self.date_time_attack = self.date_time_attack.groupby([
            'Day'])[['time']].value_counts()

        return self.date_time_attack

    def date_attacks_sample(self):
        # can be rework
        self.date_attack = pd.DataFrame(data=self.table
            ['Время атаки'])

        # new data frame with split value columns
        divide_1 = self.date_attack["Время атаки"].str.split(".", n=1, expand=True)
        # making separate first name column from new data frame
        self.date_attack["Day"] = divide_1[0]
        # making separate last name column from new data frame
        self.date_attack["Time1"] = divide_1[1]
        # Dropping old Name columns
        self.date_attack.drop(columns=["Время атаки"], inplace=True)
        self.date_attack.drop(columns=["Time1"], inplace=True)

        # по какому полю группируем
        groupby_column = 'Day'
        # имя подсчитываемого поля
        out_column = 'Кол-во атак'

        out = self.date_attack.groupby([groupby_column], group_keys=False).apply(
            lambda x: basic.Basic.collapse(x, groupby_column, out_column))

        self.date_attack = out.sort_values(by=[out_column], ascending=False)
        self.date_attack.index = np.arange(1, len(self.date_attack) + 1)  # new index

        return self.date_attack

