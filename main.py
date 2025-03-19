import keyparser
from tkinter.filedialog import askdirectory
import json

with open("user/settings.json") as file:
    settings = json.load(file)

if settings["dota_directory"] == None:
    settings["dota_directory"] = askdirectory()
    with open("user/settings.json", "w") as file:
        json.dump(settings, file)