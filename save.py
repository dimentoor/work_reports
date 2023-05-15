import pandas as pd


class ExcelLoader:
    def __init__(self, open_path, sheet_name):
        self.open_path = open_path
        self.sheet_name = sheet_name
        self.table = pd.DataFrame()

    # open file
    def open_file(self):
        self.table = pd.read_excel(self.open_path, sheet_name=self.sheet_name)
        print("Opened {}.".format(self.open_path))

    # read file


class ExcelDumper:
    def __init__(self, save_path):
        self.save_path = save_path

    # write file
    @staticmethod
    def write_file(filename, samples: dict):
        with pd.ExcelWriter(filename) as writer:
            for sample_name, sample in samples.items():
                sample.to_excel(writer, sheet_name=sample_name)
        print("Wrote to {}.".format(filename))


class MongoLoader:
    loadfrommongo(collection)
        берем докусенты
    читаем их
переводим в фреймы
засовываем их в обхекты классов тредрепорт

class mongoDumper:
    берет объект класса()
    threats_objects[obj] засовываем то в дампер
    берем из него датафреймы
    делаем документы из них
    засовываем в коллекцию

    @staticmethhod
    def func():
        pass






