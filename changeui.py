import pygubu
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "locale.ui"

class ChangerApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object('mainwindow', master)

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = ChangerApp()
    app.run()