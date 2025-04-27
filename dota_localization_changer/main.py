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
        self.button_frame.columnconfigure(4, weight=1)

        ttk.Button(
            self.button_frame, text="Сохранить пресет", command=self.save_preset
        ).grid(row=0, column=0, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Загрузить пресет", command=self.load_preset
        ).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame,
            text="Открыть папку пресетов",
            command=self.open_presets_folder,
        ).grid(row=0, column=2, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Сменить путь Dota 2", command=self.change_dota_path
        ).grid(row=0, column=3, sticky="ew", padx=5)
        ttk.Button(
            self.button_frame, text="Сбросить настройки", command=self.reset_settings
        ).grid(row=0, column=4, sticky="ew", padx=5)

        # Привязываем двойной клик
        self.heroes_tree.bind("<Double-1>", self.edit_hero)
        self.items_tree.bind("<Double-1>", self.edit_item)

    def edit_hero(self, event):
        item = self.heroes_tree.selection()[0]
        hero_name = self.heroes_tree.item(item)["values"][0]
        hero = next(h for h in self.herolist if h.name == hero_name)

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
        ttk.Label(skills_frame, text="Скиллы").pack(anchor="w")
        skills_tree = ttk.Treeview(
            skills_frame, columns=("skill", "custom"), show="headings", height=10
        )
        skills_tree.heading("skill", text="Скилл")
        skills_tree.heading("custom", text="Кастомное имя")
        skills_tree.column("skill", width=150, anchor="w")
        skills_tree.column("custom", width=150, anchor="w")
        skills_tree.pack(side="left", fill="both", expand=True)
        skills_scroll = ttk.Scrollbar(
            skills_frame, orient="vertical", command=skills_tree.yview
        )
        skills_tree.configure(yscrollcommand=skills_scroll.set)
        skills_scroll.pack(side="right", fill="y")
        for i, skill in enumerate(hero.skills):
            display_value = skill.username if skill.username else "N/A"
            skills_tree.insert("", "end", iid=i, values=(skill.name, display_value))

        # 3 столбец: таблица аспектов
        facets_frame = ttk.Frame(main_frame)
        facets_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ttk.Label(facets_frame, text="Аспекты").pack(anchor="w")
        facets_tree = ttk.Treeview(
            facets_frame, columns=("facet", "custom"), show="headings", height=10
        )
        facets_tree.heading("facet", text="Аспект")
        facets_tree.heading("custom", text="Кастомное имя")
        facets_tree.column("facet", width=150, anchor="w")
        facets_tree.column("custom", width=150, anchor="w")
        facets_tree.pack(side="left", fill="both", expand=True)
        facets_scroll = ttk.Scrollbar(
            facets_frame, orient="vertical", command=facets_tree.yview
        )
        facets_tree.configure(yscrollcommand=facets_scroll.set)
        facets_scroll.pack(side="right", fill="y")
        for i, facet in enumerate(hero.facets):
            display_value = facet.username if facet.username else "N/A"
            facets_tree.insert("", "end", iid=i, values=(facet.name, display_value))

        # Сохранение изменений
        def save_changes():
            hero.username = name_entry.get() if name_entry.get().strip() else None
            for i, skill in enumerate(hero.skills):
                val = skills_tree.item(i)["values"][1]
                if not val or val == "N/A":
                    skill.username = None
                else:
                    skill.username = val
            for i, facet in enumerate(hero.facets):
                val = facets_tree.item(i)["values"][1]
                if not val or val == "N/A":
                    facet.username = None
                else:
                    facet.username = val
            self.heroes_tree.item(item, values=(hero.name, hero.username or "N/A"))
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
                    edit_tree_cell(skills_tree, row, "custom")

        skills_tree.bind("<Double-1>", on_skill_double)

        def on_facet_double(event):
            region = facets_tree.identify("region", event.x, event.y)
            if region == "cell":
                row = facets_tree.identify_row(event.y)
                col = facets_tree.identify_column(event.x)
                if col == "#2":
                    edit_tree_cell(facets_tree, row, "custom")

        facets_tree.bind("<Double-1>", on_facet_double)

        # Кнопка сохранить
        save_btn = ttk.Button(dialog, text="Сохранить", command=save_changes)
        save_btn.pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", save_changes)

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

    def open_presets_folder(self):
        """Открывает папку с пресетами в проводнике"""
        presets_path = os.path.abspath("presets")
        try:
            subprocess.run(["explorer", presets_path])
        except Exception as e:
            messagebox.showwarning(
                "Внимание", f"Не удалось открыть папку пресетов: {e}"
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
