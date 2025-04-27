# -----------
# - r41ngee -
# -----------

import atexit
import json
import logging
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

import kvparser2
from config import LOGGER_LEVEL, VPK_PATH, change_dota_directory
from dotatypes import Hero, Item
from presets import Preset

# -LOGGER SETTINGS-
logging.basicConfig(
    level=LOGGER_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=".log",
    filemode="w",
)


def save_changes(herolist, itemslist):
    """Сохраняет все изменения в файлы"""
    try:
        abil_file = open("data/abilities_russian.txt", "r", encoding="utf-8")
    except OSError as e:
        logging.error(e)
        return

    kv: dict = kvparser2.parse(abil_file.readlines())
    abil_file.close()

    for i in herolist:
        kv.update(i.to_key_pair())

    for i in itemslist:
        kv.update(i.to_key_pair())

    with open("data/hero_tags.json", "w", encoding="utf-8") as f:
        json.dump([i.to_dict() for i in herolist], f, indent=4, ensure_ascii=False)

    with open("data/items_tags.json", "w", encoding="utf-8") as f:
        json.dump([i.to_dict() for i in itemslist], f, indent=4, ensure_ascii=False)

    with open("data/abilities_russian.txt", "w", encoding="utf-8") as f:
        f.write(kvparser2.unparse(kv))

    try:
        subprocess.run(
            [
                "bin/vpkeditcli.exe",
                "--remove-file",
                "resource/localization/abilities_russian.txt",
                VPK_PATH,
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        messagebox.showwarning(
            "Предупреждение",
            "Файл resource/localization/abilities_russian.txt не существует",
        )

    try:
        subprocess.run(
            [
                "bin/vpkeditcli.exe",
                "--add-file",
                "./data/abilities_russian.txt",
                "resource/localization/abilities_russian.txt",
                VPK_PATH,
            ]
        )
    except (subprocess.CalledProcessError, PermissionError):
        messagebox.showerror(
            "Ошибка",
            "Не удалось добавить файл локализации в VPK. Проверьте права доступа и повторите попытку",
        )


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DOTA 2 Localization Changer")
        self.geometry("1000x700")
        self.configure(bg="#2C2F33")

        # Настройка стилей
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#2C2F33", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#36393F",  # Более темный фон для вкладок
            foreground="white",
            padding=[10, 5],
            font=("Helvetica", 10, "bold"),  # Делаем шрифт жирным для лучшей читаемости
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#7289DA")],  # Цвет выбранной вкладки
            foreground=[("selected", "white")],  # Цвет текста выбранной вкладки
        )
        style.configure("TFrame", background="#2C2F33")
        style.configure("TButton", background="#7289DA", foreground="white", padding=10)
        style.configure("TLabel", background="#2C2F33", foreground="white")
        style.configure(
            "Treeview",
            background="#36393F",
            foreground="white",
            fieldbackground="#36393F",
        )
        style.configure(
            "Treeview.Heading",
            background="#7289DA",
            foreground="white",
            relief="flat",  # Убираем эффект нажатия
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#7289DA")],  # Убираем эффект наведения
        )

        try:
            with open("data/hero_tags.json", "r", encoding="utf-8") as f:
                self.herolist = [Hero(i) for i in json.load(f)]
        except OSError as e:
            messagebox.showerror("Ошибка", str(e))
            self.destroy()
            return

        try:
            with open("data/items_tags.json", "r", encoding="utf-8") as f:
                self.itemslist = [Item(i) for i in json.load(f)]
        except OSError as e:
            messagebox.showerror("Ошибка", str(e))
            self.destroy()
            return

        atexit.register(save_changes, self.herolist, self.itemslist)

        # Заголовок
        title_label = ttk.Label(
            self, text="DOTA 2 Localization Changer", font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Вкладка героев
        self.heroes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.heroes_frame, text="Герои")

        # Поле поиска для героев
        self.hero_search_var = tk.StringVar()
        hero_search_entry = ttk.Entry(
            self.heroes_frame,
            textvariable=self.hero_search_var,
            width=40,
            foreground="#888888",
        )
        hero_search_entry.pack(padx=10, pady=(10, 0), anchor="nw")
        hero_placeholder = "Поиск..."
        hero_search_entry.insert(0, hero_placeholder)
        hero_search_entry.config(foreground="#888888")

        def on_hero_focus_in(event):
            if hero_search_entry.get() == hero_placeholder:
                hero_search_entry.delete(0, tk.END)
                hero_search_entry.config(foreground="#ffffff")

        def on_hero_focus_out(event):
            if not hero_search_entry.get():
                hero_search_entry.insert(0, hero_placeholder)
                hero_search_entry.config(foreground="#888888")

        hero_search_entry.bind("<FocusIn>", on_hero_focus_in)
        hero_search_entry.bind("<FocusOut>", on_hero_focus_out)

        def hero_var_trace(*args):
            if self.hero_search_var.get() != hero_placeholder:
                self.filter_heroes()

        self.hero_search_var.trace_add("write", hero_var_trace)

        # Внутренний фрейм для таблицы и скроллбара
        heroes_tree_frame = ttk.Frame(self.heroes_frame)
        heroes_tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.heroes_tree = ttk.Treeview(
            heroes_tree_frame,
            columns=("name", "custom_name"),
            show="headings",
            height=20,
        )
        self.heroes_tree.heading("name", text="Имя")
        self.heroes_tree.heading("custom_name", text="Кастомное имя")
        self.heroes_tree.column("name", width=200, anchor="w")
        self.heroes_tree.column("custom_name", width=200, anchor="w")
        self.heroes_tree.pack(side="left", fill="both", expand=True)

        # Добавляем скроллбар только вертикальный, горизонтальный не используем
        heroes_scrollbar = ttk.Scrollbar(
            heroes_tree_frame, orient="vertical", command=self.heroes_tree.yview
        )
        heroes_scrollbar.pack(side="right", fill="y")
        self.heroes_tree.configure(
            yscrollcommand=heroes_scrollbar.set, xscrollcommand=""
        )

        for hero in self.herolist:
            self.heroes_tree.insert(
                "", "end", values=(hero.name, hero.username or "N/A")
            )

        # Вкладка предметов
        self.items_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.items_frame, text="Предметы")

        # Поле поиска для предметов
        self.item_search_var = tk.StringVar()
        item_search_entry = ttk.Entry(
            self.items_frame,
            textvariable=self.item_search_var,
            width=40,
            foreground="#888888",
        )
        item_search_entry.pack(padx=10, pady=(10, 0), anchor="nw")
        item_placeholder = "Поиск..."
        item_search_entry.insert(0, item_placeholder)
        item_search_entry.config(foreground="#888888")

        def on_item_focus_in(event):
            if item_search_entry.get() == item_placeholder:
                item_search_entry.delete(0, tk.END)
                item_search_entry.config(foreground="#ffffff")

        def on_item_focus_out(event):
            if not item_search_entry.get():
                item_search_entry.insert(0, item_placeholder)
                item_search_entry.config(foreground="#888888")

        item_search_entry.bind("<FocusIn>", on_item_focus_in)
        item_search_entry.bind("<FocusOut>", on_item_focus_out)

        def item_var_trace(*args):
            if self.item_search_var.get() != item_placeholder:
                self.filter_items()

        self.item_search_var.trace_add("write", item_var_trace)

        # Внутренний фрейм для таблицы и скроллбара
        items_tree_frame = ttk.Frame(self.items_frame)
        items_tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.items_tree = ttk.Treeview(
            items_tree_frame,
            columns=("name", "custom_name"),
            show="headings",
            height=20,
        )
        self.items_tree.heading("name", text="Имя")
        self.items_tree.heading("custom_name", text="Кастомное имя")
        self.items_tree.column("name", width=200, anchor="w")
        self.items_tree.column("custom_name", width=200, anchor="w")
        self.items_tree.pack(side="left", fill="both", expand=True)

        # Добавляем скроллбар только вертикальный, горизонтальный не используем
        items_scrollbar = ttk.Scrollbar(
            items_tree_frame, orient="vertical", command=self.items_tree.yview
        )
        items_scrollbar.pack(side="right", fill="y")
        self.items_tree.configure(yscrollcommand=items_scrollbar.set, xscrollcommand="")

        for item in self.itemslist:
            self.items_tree.insert(
                "", "end", values=(item.name, item.username or "N/A")
            )

        # Кнопки управления
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill="x", padx=20, pady=20)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)

        ttk.Button(
            self.button_frame, text="Загрузить пресет", command=self.load_preset
        ).grid(row=0, column=0, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Сохранить пресет", command=self.save_preset
        ).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Сбросить настройки", command=self.reset_settings
        ).grid(row=0, column=2, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Сменить путь Dota 2", command=self.change_dota_path
        ).grid(row=0, column=3, sticky="ew", padx=5)

        # Привязываем двойной клик
        self.heroes_tree.bind("<Double-1>", self.edit_hero)
        self.items_tree.bind("<Double-1>", self.edit_item)

    def edit_hero(self, event):
        item = self.heroes_tree.selection()[0]
        hero_name = self.heroes_tree.item(item)["values"][0]
        hero = next(h for h in self.herolist if h.name == hero_name)

        dialog = tk.Toplevel(self)
        dialog.title(f"Редактирование {hero.name}")
        dialog.geometry("500x700")
        dialog.configure(bg="#2C2F33")

        # Имя героя
        ttk.Label(dialog, text="Новое имя героя:", font=("Helvetica", 12)).pack(pady=10)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, hero.username or "")
        name_entry.pack(pady=5)

        # Скиллы
        ttk.Label(dialog, text="Скиллы:", font=("Helvetica", 12, "bold")).pack(pady=10)
        skills_frame = ttk.Frame(dialog)
        skills_frame.pack(fill="x", padx=20)

        skill_entries = []
        for skill in hero.skills:
            ttk.Label(skills_frame, text=skill.name, font=("Helvetica", 10)).pack(
                pady=2
            )
            entry = ttk.Entry(skills_frame, width=40)
            entry.insert(0, skill.username or "")
            entry.pack(pady=5)
            skill_entries.append((skill, entry))

        # Аспекты
        ttk.Label(dialog, text="Аспекты:", font=("Helvetica", 12, "bold")).pack(pady=10)
        facets_frame = ttk.Frame(dialog)
        facets_frame.pack(fill="x", padx=20)

        facet_entries = []
        for facet in hero.facets:
            ttk.Label(facets_frame, text=facet.name, font=("Helvetica", 10)).pack(
                pady=2
            )
            entry = ttk.Entry(facets_frame, width=40)
            entry.insert(0, facet.username or "")
            entry.pack(pady=5)
            facet_entries.append((facet, entry))

        def save():
            hero.username = name_entry.get() if name_entry.get().strip() else None

            for skill, entry in skill_entries:
                skill.username = entry.get() if entry.get().strip() else None

            for facet, entry in facet_entries:
                facet.username = entry.get() if entry.get().strip() else None

            self.heroes_tree.item(item, values=(hero.name, hero.username or "N/A"))
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)

    def edit_item(self, event):
        item_sel = self.items_tree.selection()[0]
        item_name = self.items_tree.item(item_sel)["values"][0]
        item = next(i for i in self.itemslist if i.name == item_name)

        dialog = tk.Toplevel(self)
        dialog.title(f"Редактирование {item.name}")
        dialog.geometry("400x300")
        dialog.configure(bg="#2C2F33")

        ttk.Label(dialog, text="Новое имя:", font=("Helvetica", 12)).pack(pady=20)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, item.username or "")
        name_entry.pack(pady=10)

        def save():
            item.username = name_entry.get() if name_entry.get().strip() else None
            self.items_tree.item(item_sel, values=(item.name, item.username or "N/A"))
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)

    def load_preset(self):
        preset_filenames = Preset.load_names()

        dialog = tk.Toplevel(self)
        dialog.title("Загрузка пресета")
        dialog.geometry("400x500")
        dialog.configure(bg="#2C2F33")

        ttk.Label(dialog, text="Выберите пресет:", font=("Helvetica", 12)).pack(pady=10)

        listbox = tk.Listbox(
            dialog,
            bg="#36393F",
            fg="white",
            selectmode="single",
            font=("Helvetica", 10),
        )
        listbox.pack(expand=True, fill="both", padx=20, pady=10)

        for name in preset_filenames:
            listbox.insert("end", name)

        def load():
            if not listbox.curselection():
                return
            selected = listbox.get(listbox.curselection())
            preset = Preset.load(selected)
            self.herolist = preset.heroes
            self.itemslist = preset.items
            self.refresh_trees()
            dialog.destroy()

        ttk.Button(dialog, text="Загрузить", command=load).pack(pady=20)

    def save_preset(self):
        dialog = tk.Toplevel(self)
        dialog.title("Сохранение пресета")
        dialog.geometry("400x200")
        dialog.configure(bg="#2C2F33")

        ttk.Label(dialog, text="Имя пресета:", font=("Helvetica", 12)).pack(pady=20)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=10)

        def save():
            name = name_entry.get()
            if not name:
                return
            preset = Preset(
                name,
                heroes=[i.to_dict() for i in self.herolist],
                items=[j.to_dict() for j in self.itemslist],
            )
            preset.save()
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)

    def reset_settings(self):
        if not messagebox.askyesno(
            "Подтверждение", "Вы уверены что хотите сбросить все настройки?"
        ):
            return

        for hero in self.herolist:
            hero.username = None
            for skill in hero.skills:
                skill.username = None
            for facet in hero.facets:
                facet.username = None

        for item in self.itemslist:
            item.username = None

        self.refresh_trees()

    def refresh_trees(self):
        self.filter_heroes()
        self.filter_items()

    def filter_heroes(self):
        """Фильтрация героев по поисковому запросу"""
        query = self.hero_search_var.get().lower()
        if query == "поиск...":
            query = ""
        self.heroes_tree.delete(*self.heroes_tree.get_children())
        for hero in self.herolist:
            if query in hero.name.lower() or (
                hero.username and query in hero.username.lower()
            ):
                self.heroes_tree.insert(
                    "", "end", values=(hero.name, hero.username or "N/A")
                )

    def filter_items(self):
        """Фильтрация предметов по поисковому запросу"""
        query = self.item_search_var.get().lower()
        if query == "поиск...":
            query = ""
        self.items_tree.delete(*self.items_tree.get_children())
        for item in self.itemslist:
            if query in item.name.lower() or (
                item.username and query in item.username.lower()
            ):
                self.items_tree.insert(
                    "", "end", values=(item.name, item.username or "N/A")
                )

    def change_dota_path(self):
        """Смена пути установки Dota 2"""
        if change_dota_directory():
            messagebox.showinfo(
                "Успех",
                "Путь к Dota 2 успешно изменен. Изменения вступят в силу после перезапуска программы.",
            )
        else:
            messagebox.showwarning("Предупреждение", "Смена пути отменена")


if __name__ == "__main__":
    app = App()
    app.mainloop()
