# -----------
# - r41ngee -
# -----------

import atexit
import json
import logging
import os
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
        self.geometry("1200x800")
        self.configure(bg="#2C2F33")

        # Настройка стилей
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#2C2F33", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#36393F",
            foreground="white",
            padding=[10, 5],
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#7289DA")],
            foreground=[("selected", "white")],
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
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#7289DA")],
            foreground=[("selected", "white")],
        )
        style.configure("Treeview.Cell", background="#36393F")
        style.map("Treeview.Cell", background=[("selected", "#7289DA")])

        # Загрузка данных
        self.load_data()

        # Создание интерфейса
        self.create_interface()

    def load_data(self):
        """Загрузка данных из файлов"""
        try:
            with open("data/hero_tags.json", "r", encoding="utf-8") as f:
                self.herolist = [Hero(i) for i in json.load(f)]
            with open("data/items_tags.json", "r", encoding="utf-8") as f:
                self.itemslist = [Item(i) for i in json.load(f)]
        except OSError as e:
            messagebox.showerror("Ошибка", str(e))
            self.destroy()
            return

        atexit.register(save_changes, self.herolist, self.itemslist)

    def create_interface(self):
        """Создание элементов интерфейса"""
        # Заголовок
        title_label = ttk.Label(
            self, text="DOTA 2 Localization Changer", font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        # Создание вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Вкладка героев
        self.create_heroes_tab()
        # Вкладка предметов
        self.create_items_tab()
        # Кнопки управления
        self.create_control_buttons()

    def create_search_entry(self, parent, var, placeholder, on_change):
        """Создание поля поиска"""
        entry = ttk.Entry(parent, textvariable=var, width=40, foreground="#888888")
        entry.pack(padx=10, pady=(10, 0), anchor="nw")
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground="#ffffff")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="#888888")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        var.trace_add(
            "write", lambda *args: on_change() if var.get() != placeholder else None
        )
        return entry

    def create_treeview(self, parent, columns, show_headings=True):
        """Создание таблицы"""
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings" if show_headings else "",
            height=20,
            selectmode="none",
        )
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="w")
        return tree

    def create_heroes_tab(self):
        """Создание вкладки героев"""
        self.heroes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.heroes_frame, text="Герои")

        # Поле поиска
        self.hero_search_var = tk.StringVar()
        self.create_search_entry(
            self.heroes_frame, self.hero_search_var, "Поиск...", self.filter_heroes
        )

        # Таблица героев
        heroes_tree_frame = ttk.Frame(self.heroes_frame)
        heroes_tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.heroes_tree = self.create_treeview(
            heroes_tree_frame, [f"col{i}" for i in range(1, 5)], show_headings=False
        )
        self.heroes_tree.pack(side="left", fill="both", expand=True)

        # Скроллбар
        heroes_scrollbar = ttk.Scrollbar(
            heroes_tree_frame, orient="vertical", command=self.heroes_tree.yview
        )
        heroes_scrollbar.pack(side="right", fill="y")
        self.heroes_tree.configure(yscrollcommand=heroes_scrollbar.set)

        # Привязка событий
        self.heroes_tree.bind("<Double-1>", self.edit_hero)
        self.heroes_tree.bind("<Button-1>", self.on_click)
        self.heroes_tree.bind("<Motion>", self.on_mouse_motion)

        self.refresh_heroes_tree()

    def create_items_tab(self):
        """Создание вкладки предметов"""
        self.items_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.items_frame, text="Предметы")

        # Поле поиска
        self.item_search_var = tk.StringVar()
        self.create_search_entry(
            self.items_frame, self.item_search_var, "Поиск...", self.filter_items
        )

        # Таблица предметов
        items_tree_frame = ttk.Frame(self.items_frame)
        items_tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.items_tree = self.create_treeview(
            items_tree_frame, ["Имя", "Кастомное имя"]
        )
        self.items_tree.pack(side="left", fill="both", expand=True)

        # Скроллбар
        items_scrollbar = ttk.Scrollbar(
            items_tree_frame, orient="vertical", command=self.items_tree.yview
        )
        items_scrollbar.pack(side="right", fill="y")
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

        # Привязка событий
        self.items_tree.bind("<Double-1>", self.edit_item)

        # Заполнение таблицы
        for item in self.itemslist:
            self.items_tree.insert(
                "", "end", values=(item.name, item.username or "N/A")
            )

    def create_control_buttons(self):
        """Создание кнопок управления"""
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill="x", padx=20, pady=20)

        buttons = [
            ("Сохранить пресет", self.save_preset),
            ("Загрузить пресет", self.load_preset),
            ("Открыть папку пресетов", self.open_presets_folder),
            ("Сменить путь Dota 2", self.change_dota_path),
            ("Сбросить настройки", self.reset_settings),
        ]

        for i, (text, command) in enumerate(buttons):
            self.button_frame.columnconfigure(i, weight=1)
            ttk.Button(self.button_frame, text=text, command=command).grid(
                row=0, column=i, sticky="ew", padx=5
            )

    def refresh_heroes_tree(self):
        """Обновляет отображение героев в таблице"""
        self.heroes_tree.delete(*self.heroes_tree.get_children())

        # Распределяем героев по строкам и колонкам
        heroes_per_row = 4
        for i in range(0, len(self.herolist), heroes_per_row):
            row_heroes = self.herolist[i : i + heroes_per_row]
            values = [hero.name for hero in row_heroes]
            # Дополняем строку пустыми значениями, если героев меньше 4
            while len(values) < 4:
                values.append("")
            self.heroes_tree.insert("", "end", values=values)

    def on_click(self, event):
        """Обработчик клика для выделения ячейки"""
        # Определяем текущую ячейку
        region = self.heroes_tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.heroes_tree.identify_row(event.y)
            column = self.heroes_tree.identify_column(event.x)
            if item and column:
                # Снимаем выделение со всех ячеек
                for i in self.heroes_tree.get_children():
                    self.heroes_tree.item(i, tags=())

                # Выделяем текущую ячейку
                self.heroes_tree.item(item, tags=("selected",))
                self.heroes_tree.selection_set(item)

    def on_mouse_motion(self, event):
        """Обработчик движения мыши для подсветки ячейки"""
        # Определяем текущую ячейку
        region = self.heroes_tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.heroes_tree.identify_row(event.y)
            column = self.heroes_tree.identify_column(event.x)
            if item and column:
                # Подсвечиваем текущую ячейку
                self.heroes_tree.item(item, tags=("hover",))
            else:
                # Снимаем подсветку
                for i in self.heroes_tree.get_children():
                    if "hover" in self.heroes_tree.item(i, "tags"):
                        self.heroes_tree.item(i, tags=())
        else:
            # Снимаем подсветку
            for i in self.heroes_tree.get_children():
                if "hover" in self.heroes_tree.item(i, "tags"):
                    self.heroes_tree.item(i, tags=())

    def create_edit_dialog(self, title, item, on_save):
        """Создание диалога редактирования"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Редактирование {title}")
        dialog.geometry("400x200")
        dialog.configure(bg="#2C2F33")

        ttk.Label(dialog, text="Новое имя:", font=("Helvetica", 12)).pack(pady=20)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, item.username or "")
        name_entry.pack(pady=10)

        def save():
            on_save(name_entry.get())
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)
        return dialog

    def edit_hero(self, event):
        """Обработчик двойного клика по герою"""
        region = self.heroes_tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.heroes_tree.identify_row(event.y)
            column = self.heroes_tree.identify_column(event.x)
            if item and column:
                column_index = int(column[1:]) - 1
                hero_name = self.heroes_tree.item(item)["values"][column_index]
                if hero_name:  # Проверяем, что клик был по герою, а не по пустой ячейке
                    hero = next(h for h in self.herolist if h.name == hero_name)
                    self.show_hero_edit_dialog(hero)

    def edit_item(self, event):
        """Обработчик двойного клика по предмету"""
        item_sel = self.items_tree.selection()[0]
        item_name = self.items_tree.item(item_sel)["values"][0]
        item = next(i for i in self.itemslist if i.name == item_name)

        def on_save(new_name):
            item.username = new_name if new_name.strip() else None
            self.items_tree.item(item_sel, values=(item.name, item.username or "N/A"))

        self.create_edit_dialog(item.name, item, on_save)

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
            self.refresh_heroes_tree()
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
                heroes=self.herolist,
                items=self.itemslist,
            )
            preset.save()
            dialog.destroy()
            # Диалоговое окно с вопросом
            preset_path = os.path.abspath(os.path.join("presets", f"{name}.json"))
            if messagebox.askyesno(
                "Открыть проводник?", "Открыть проводник с выделенным файлом пресета?"
            ):
                try:
                    subprocess.run(["explorer", "/select,", preset_path])
                except Exception as e:
                    messagebox.showwarning(
                        "Внимание", f"Не удалось открыть Проводник: {e}"
                    )

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

        self.refresh_heroes_tree()

    def filter_heroes(self):
        """Фильтрация героев по поисковому запросу"""
        query = self.hero_search_var.get().lower()
        if query == "поиск...":
            query = ""

        self.heroes_tree.delete(*self.heroes_tree.get_children())
        filtered_heroes = [h for h in self.herolist if query in h.name.lower()]

        # Распределяем отфильтрованных героев по строкам
        heroes_per_row = 4
        for i in range(0, len(filtered_heroes), heroes_per_row):
            row_heroes = filtered_heroes[i : i + heroes_per_row]
            values = [hero.name for hero in row_heroes]
            # Дополняем строку пустыми значениями, если героев меньше 4
            while len(values) < 4:
                values.append("")
            self.heroes_tree.insert("", "end", values=values)

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

    def open_presets_folder(self):
        """Открывает папку с пресетами в проводнике"""
        presets_path = os.path.abspath("presets")
        try:
            subprocess.run(["explorer", presets_path])
        except Exception as e:
            messagebox.showwarning(
                "Внимание", f"Не удалось открыть папку пресетов: {e}"
            )

    def show_hero_edit_dialog(self, hero):
        """Показывает диалог редактирования героя"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Редактирование {hero.name}")
        dialog.geometry("900x500")
        dialog.configure(bg="#2C2F33")

        main_frame = ttk.Frame(dialog)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=2)

        # 1 столбец: имя героя
        name_frame = ttk.Frame(main_frame)
        name_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(name_frame, text="Имя героя:").pack(anchor="w")
        name_entry = ttk.Entry(name_frame, width=25)
        name_entry.insert(0, hero.username or "")
        name_entry.pack(anchor="w", pady=5)

        # 2 столбец: таблица скиллов
        skills_frame = ttk.Frame(main_frame)
        skills_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ttk.Label(skills_frame, text="Способности").pack(anchor="w")
        skills_tree = self.create_treeview(
            skills_frame, ["Способность", "Кастомное имя"]
        )
        skills_tree.pack(side="left", fill="both", expand=True)
        skills_scroll = ttk.Scrollbar(
            skills_frame, orient="vertical", command=skills_tree.yview
        )
        skills_tree.configure(yscrollcommand=skills_scroll.set)
        skills_scroll.pack(side="right", fill="y")

        # 3 столбец: таблица аспектов
        facets_frame = ttk.Frame(main_frame)
        facets_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ttk.Label(facets_frame, text="Аспекты").pack(anchor="w")
        facets_tree = self.create_treeview(facets_frame, ["Аспект", "Кастомное имя"])
        facets_tree.pack(side="left", fill="both", expand=True)
        facets_scroll = ttk.Scrollbar(
            facets_frame, orient="vertical", command=facets_tree.yview
        )
        facets_tree.configure(yscrollcommand=facets_scroll.set)
        facets_scroll.pack(side="right", fill="y")

        # Заполняем таблицы
        for i, skill in enumerate(hero.skills):
            skills_tree.insert(
                "", "end", iid=i, values=(skill.name, skill.username or "N/A")
            )
        for i, facet in enumerate(hero.facets):
            facets_tree.insert(
                "", "end", iid=i, values=(facet.name, facet.username or "N/A")
            )

        def save_changes():
            hero.username = name_entry.get() if name_entry.get().strip() else None
            for i, skill in enumerate(hero.skills):
                val = skills_tree.item(i)["values"][1]
                skill.username = None if not val or val == "N/A" else val
            for i, facet in enumerate(hero.facets):
                val = facets_tree.item(i)["values"][1]
                facet.username = None if not val or val == "N/A" else val
            self.refresh_heroes_tree()
            dialog.destroy()

        # Редактирование кастомных имён по двойному клику
        def edit_tree_cell(tree, iid, col):
            x, y, width, height = tree.bbox(iid, col)
            value = tree.set(iid, col)
            entry = ttk.Entry(tree)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, value)
            entry.focus()

            def on_enter(event=None):
                tree.set(iid, col, entry.get())
                entry.destroy()

            entry.bind("<Return>", on_enter)
            entry.bind("<FocusOut>", lambda e: entry.destroy())

        def on_skill_double(event):
            region = skills_tree.identify("region", event.x, event.y)
            if region == "cell":
                row = skills_tree.identify_row(event.y)
                col = skills_tree.identify_column(event.x)
                if col == "#2":
                    edit_tree_cell(skills_tree, row, "Кастомное имя")

        def on_facet_double(event):
            region = facets_tree.identify("region", event.x, event.y)
            if region == "cell":
                row = facets_tree.identify_row(event.y)
                col = facets_tree.identify_column(event.x)
                if col == "#2":
                    edit_tree_cell(facets_tree, row, "Кастомное имя")

        skills_tree.bind("<Double-1>", on_skill_double)
        facets_tree.bind("<Double-1>", on_facet_double)

        ttk.Button(dialog, text="Сохранить", command=save_changes).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", save_changes)


if __name__ == "__main__":
    app = App()
    app.mainloop()
