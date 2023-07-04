class DataFrameViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Frame Viewer")
        self.geometry('1200x600')  # Установка размера окна

        self.dataframe = None

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.LEFT, anchor=tk.N, pady=20)

        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(side=tk.BOTTOM, anchor=tk.E)

        self.progress_bar = Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')

        self.load_button = ttk.Button(self.button_frame, text="Загрузить данные", command=self.s_load_data)
        self.load_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.drop_button = ttk.Button(self.button_frame, text="Удалить пропуски", command=self.s_drop_na)
        self.drop_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.prep_button = ttk.Button(self.button_frame, text="Подготовить к обучению", command=self.s_preparation)
        self.prep_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.learn_button = ttk.Button(self.button_frame, text="Начать обучение")
        self.learn_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.table = Table(self.table_frame, showtoolbar=True, showstatusbar=True)

    def s_load_data(self):
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=10)
        self.progress_bar.start()
        self.after(2000, self.s_load_data_complete)

    def s_load_data_complete(self):
        # Функция загрузки данных
        self.dataframe = data_edit.csv_read()

        self.table.model = TableModel(dataframe=self.dataframe)
        self.table.show()

        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def s_drop_na(self):
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=10)
        self.progress_bar.start()
        self.after(2000, self.s_drop_na_complete)

    def s_drop_na_complete(self):
        # Функция удаления пропущенных значений
        self.dataframe = data_edit.drop_na(self.dataframe)

        self.table.model = TableModel(dataframe=self.dataframe)
        self.table.show()

        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def s_preparation(self):
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=10)
        self.progress_bar.start()
        self.after(2000, self.s_preparation_complete)

    def s_preparation_complete(self):
        # Функция подготовки данных к обучению
        self.dataframe = data_edit.preparation(self.dataframe)

        self.table.model = TableModel(dataframe=self.dataframe)
        self.table.show()

        self.progress_bar.stop()
        self.progress_bar.pack_forget()


app = DataFrameViewer()
app.mainloop()
