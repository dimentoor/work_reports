import pandas as pd


class ExcelLoader:
    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.table = pd.DataFrame()

    # open file
    def openfile(self):
        self.table = pd.read_excel(self.path, sheet_name=self.sheet_name)
        print("openfile is done!")

    # read file


class ExcelDumper:
    def __init__(self, path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
        self.table = pd.DataFrame()

    # write file
    def writefile(self, filename, samples: dict):
        with pd.ExcelWriter(filename) as writer:
            for sample_name, sample in samples.items():
                sample.to_excel(writer, sheet_name=sample_name)
        print("writefile is done!")







