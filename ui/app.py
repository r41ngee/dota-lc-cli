import tkinter as tk
import pygubu

class ChangerApp:
    def __init__(self):
        # Загрузка интерфейса из файла .ui
        self.builder = pygubu.Builder()
        self.builder.add_from_file('index.ui')

        # Получение главного окна
        self.mainwindow = self.builder.get_object('mainwindow')

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = ChangerApp()
    app.run()