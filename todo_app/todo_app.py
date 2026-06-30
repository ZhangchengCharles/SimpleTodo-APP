import ctypes
import json
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


def get_current_folder():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd().resolve()


CURRENT_FOLDER = get_current_folder()
APP_NAME = "SimpleTodo"
DATA_FILE = CURRENT_FOLDER / ".simple_todos.json"
UP_ARROW = "\u2191"
DOWN_ARROW = "\u2193"


def clear_hidden_attribute(path):
    if os.name != "nt" or not path.exists():
        return

    hidden = 0x2
    invalid = 0xFFFFFFFF
    kernel32 = ctypes.windll.kernel32
    attrs = kernel32.GetFileAttributesW(str(path))
    if attrs != invalid and attrs & hidden:
        kernel32.SetFileAttributesW(str(path), attrs & ~hidden)


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("588x749")
        self.minsize(340, 504)
        self.configure(bg="#f5f5f5")

        self.todos, self.plans = self.load_data()
        self.active_section = "todos"
        self.rows = []
        self.check_vars = []

        self.build_ui()
        self.render_active_section()

    def build_ui(self):
        header = tk.Frame(self, bg="#f5f5f5")
        header.pack(fill="x", padx=14, pady=(14, 8))

        self.entry = tk.Entry(header, font=("Segoe UI", 11), relief="solid", bd=1)
        self.entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.entry.bind("<Return>", lambda _event: self.add_item())

        self.add_button = tk.Button(
            header,
            text="Add",
            command=self.add_item,
            font=("Segoe UI", 10),
            width=8,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
        )
        self.add_button.pack(side="left", padx=(8, 0), ipady=3)

        self.list_container = tk.Frame(self, bg="#f5f5f5")
        self.list_container.pack(fill="both", expand=True, padx=14, pady=(2, 14))

        self.list_canvas = tk.Canvas(
            self.list_container,
            bg="#f5f5f5",
            bd=0,
            highlightthickness=0,
        )
        self.scrollbar = tk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.list_canvas.yview,
        )
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.list_canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self.list_canvas, bg="#f5f5f5")
        self.list_window = self.list_canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw",
        )
        self.list_frame.bind("<Configure>", self.update_scroll_region)
        self.list_canvas.bind("<Configure>", self.resize_list_window)
        self.bind_all("<MouseWheel>", self.on_mousewheel)

        self.folder_label = tk.Label(
            self,
            text=str(CURRENT_FOLDER),
            font=("Segoe UI", 8),
            bg="#f5f5f5",
            fg="#777777",
            anchor="w",
        )
        self.folder_label.pack(fill="x", padx=14, pady=(0, 6))

        self.tab_bar = tk.Frame(self, bg="#f5f5f5")
        self.tab_bar.pack(fill="x", padx=14, pady=(0, 14))

        self.todo_tab = tk.Button(
            self.tab_bar,
            text="To-dos",
            command=lambda: self.switch_section("todos"),
            font=("Segoe UI", 10),
            relief="flat",
            bd=0,
        )
        self.todo_tab.pack(side="left", fill="x", expand=True, ipady=7)

        self.plan_tab = tk.Button(
            self.tab_bar,
            text="Plans",
            command=lambda: self.switch_section("plans"),
            font=("Segoe UI", 10),
            relief="flat",
            bd=0,
        )
        self.plan_tab.pack(side="left", fill="x", expand=True, ipady=7, padx=(8, 0))
        self.update_tabs()

    def update_scroll_region(self, _event=None):
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def resize_list_window(self, event):
        self.list_canvas.itemconfigure(self.list_window, width=event.width)

    def on_mousewheel(self, event):
        first, last = self.list_canvas.yview()
        if first == 0.0 and last == 1.0:
            return None

        direction = -1 if event.delta > 0 else 1
        self.list_canvas.yview_scroll(direction, "units")
        return "break"

    def load_data(self):
        try:
            if DATA_FILE.exists():
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, list):
                    return self.clean_todos(data), []
                if isinstance(data, dict):
                    return (
                        self.clean_todos(data.get("todos", [])),
                        self.clean_plans(data.get("plans", [])),
                    )
        except (OSError, json.JSONDecodeError):
            messagebox.showwarning(
                APP_NAME,
                "Could not read saved data. Starting with empty sections.",
            )
        return [], []

    def clean_todos(self, items):
        if not isinstance(items, list):
            return []

        clean_items = []
        for item in items:
            if not isinstance(item, dict):
                continue

            text = str(item.get("text", "")).strip()
            if text:
                clean_items.append(
                    {
                        "text": text,
                        "done": bool(item.get("done", False)),
                    }
                )
        return clean_items

    def clean_plans(self, items):
        if not isinstance(items, list):
            return []

        clean_items = []
        for item in items:
            if isinstance(item, dict):
                text = str(item.get("text", "")).strip()
                done = bool(item.get("done", False))
            else:
                text = str(item).strip()
                done = False

            if text:
                clean_items.append(
                    {
                        "text": text,
                        "done": done,
                    }
                )
        return clean_items

    def save_data(self):
        clear_hidden_attribute(DATA_FILE)
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                {
                    "todos": self.todos,
                    "plans": self.plans,
                },
                file,
                ensure_ascii=False,
                indent=2,
            )

    def switch_section(self, section):
        if section not in {"todos", "plans"}:
            return

        if section == self.active_section:
            return

        self.active_section = section
        self.entry.delete(0, tk.END)
        self.update_tabs()
        self.render_active_section()

    def update_tabs(self):
        active_style = {
            "bg": "#2563eb",
            "fg": "white",
            "activebackground": "#1d4ed8",
            "activeforeground": "white",
        }
        inactive_style = {
            "bg": "#e5e7eb",
            "fg": "#374151",
            "activebackground": "#d1d5db",
            "activeforeground": "#111827",
        }

        self.todo_tab.configure(**(active_style if self.active_section == "todos" else inactive_style))
        self.plan_tab.configure(**(active_style if self.active_section == "plans" else inactive_style))
        self.add_button.configure(
            text="Add Todo" if self.active_section == "todos" else "Add Plan"
        )

    def add_item(self):
        if self.active_section == "todos":
            self.add_todo()
        else:
            self.add_plan()

    def add_todo(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.todos.append({"text": text, "done": False})
        self.entry.delete(0, tk.END)
        self.save_data()
        self.render_active_section()

    def add_plan(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.plans.append({"text": text, "done": False})
        self.entry.delete(0, tk.END)
        self.save_data()
        self.render_active_section()

    def toggle_todo(self, index):
        self.todos[index]["done"] = not self.todos[index]["done"]
        self.save_data()
        self.render_active_section()

    def toggle_plan(self, index):
        self.plans[index]["done"] = not self.plans[index]["done"]
        self.save_data()
        self.render_active_section()

    def delete_todo(self, index):
        del self.todos[index]
        self.save_data()
        self.render_active_section()

    def delete_plan(self, index):
        del self.plans[index]
        self.save_data()
        self.render_active_section()

    def edit_todo(self, index, new_text):
        text = new_text.strip()
        if not text:
            return False

        self.todos[index]["text"] = text
        self.save_data()
        self.render_active_section()
        return True

    def edit_plan(self, index, new_text):
        text = new_text.strip()
        if not text:
            return False

        self.plans[index]["text"] = text
        self.save_data()
        self.render_active_section()
        return True

    def open_edit_dialog(self, section, index):
        title = "Edit Todo" if section == "todos" else "Edit Plan"
        current_text = (
            self.todos[index]["text"]
            if section == "todos"
            else self.plans[index]["text"]
        )

        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.configure(bg="#f5f5f5")
        dialog.geometry("380x210")
        dialog.minsize(300, 170)
        dialog.transient(self)
        dialog.grab_set()

        editor = tk.Text(
            dialog,
            font=("Segoe UI", 11),
            wrap="word",
            relief="solid",
            bd=1,
            height=5,
        )
        editor.pack(fill="both", expand=True, padx=12, pady=(12, 8))
        editor.insert("1.0", current_text)
        editor.focus_set()
        editor.tag_add("sel", "1.0", "end-1c")

        actions = tk.Frame(dialog, bg="#f5f5f5")
        actions.pack(fill="x", padx=12, pady=(0, 12))

        def save_edit():
            value = editor.get("1.0", "end-1c")
            saved = (
                self.edit_todo(index, value)
                if section == "todos"
                else self.edit_plan(index, value)
            )
            if saved:
                dialog.destroy()
            else:
                dialog.bell()
                editor.focus_set()

        cancel_button = tk.Button(
            actions,
            text="Cancel",
            command=dialog.destroy,
            font=("Segoe UI", 9),
            bg="#eeeeee",
            relief="flat",
            width=8,
        )
        cancel_button.pack(side="right")

        save_button = tk.Button(
            actions,
            text="Save",
            command=save_edit,
            font=("Segoe UI", 9),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            width=8,
        )
        save_button.pack(side="right", padx=(0, 8))

        dialog.bind("<Escape>", lambda _event: dialog.destroy())
        dialog.bind("<Control-Return>", lambda _event: save_edit())
        self.center_dialog(dialog)

    def center_dialog(self, dialog):
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{max(0, x)}+{max(0, y)}")

    def move_todo_up(self, index):
        if index >= len(self.todos) - 1:
            return
        self.todos[index], self.todos[index + 1] = (
            self.todos[index + 1],
            self.todos[index],
        )
        self.save_data()
        self.render_active_section()

    def move_todo_down(self, index):
        if index <= 0:
            return
        self.todos[index], self.todos[index - 1] = (
            self.todos[index - 1],
            self.todos[index],
        )
        self.save_data()
        self.render_active_section()

    def move_plan_up(self, index):
        if index >= len(self.plans) - 1:
            return
        self.plans[index], self.plans[index + 1] = (
            self.plans[index + 1],
            self.plans[index],
        )
        self.save_data()
        self.render_active_section()

    def move_plan_down(self, index):
        if index <= 0:
            return
        self.plans[index], self.plans[index - 1] = (
            self.plans[index - 1],
            self.plans[index],
        )
        self.save_data()
        self.render_active_section()

    def render_active_section(self):
        if self.active_section == "todos":
            self.render_todos()
        else:
            self.render_plans()

    def render_todos(self):
        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.check_vars.clear()

        if not self.todos:
            empty = tk.Label(
                self.list_frame,
                text="No todos yet",
                font=("Segoe UI", 11),
                bg="#f5f5f5",
                fg="#777777",
            )
            empty.pack(fill="x", pady=28)
            self.rows.append(empty)
            self.update_idletasks()
            self.update_scroll_region()
            return

        for index, todo in reversed(list(enumerate(self.todos))):
            row = tk.Frame(self.list_frame, bg="#ffffff", highlightthickness=1)
            row.configure(highlightbackground="#dddddd", highlightcolor="#dddddd")
            row.grid_columnconfigure(1, weight=1, minsize=80)
            row.pack(fill="x", pady=4)

            done_var = tk.IntVar(value=1 if todo["done"] else 0)
            self.check_vars.append(done_var)
            check = tk.Checkbutton(
                row,
                variable=done_var,
                onvalue=1,
                offvalue=0,
                command=lambda i=index: self.toggle_todo(i),
                bg="#ffffff",
                activebackground="#ffffff",
                selectcolor="#ffffff",
                indicatoron=True,
                width=2,
            )
            check.grid(row=0, column=0, padx=(8, 4), pady=8, sticky="nw")

            label = tk.Label(
                row,
                text=todo["text"],
                anchor="w",
                font=("Segoe UI", 11, "overstrike" if todo["done"] else "normal"),
                bg="#ffffff",
                fg="#9ca3af" if todo["done"] else "#111827",
                wraplength=270,
                justify="left",
            )
            label.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="ew")
            label.bind(
                "<Double-Button-1>",
                lambda _event, i=index: self.open_edit_dialog("todos", i),
            )

            order_frame = tk.Frame(row, bg="#ffffff")
            order_frame.grid(row=0, column=2, padx=(0, 6), pady=7, sticky="ne")

            up_button = tk.Button(
                order_frame,
                text=UP_ARROW,
                command=lambda i=index: self.move_todo_up(i),
                font=("Segoe UI Symbol", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                disabledforeground="#c7c7c7",
                relief="flat",
                width=2,
                state="normal" if index < len(self.todos) - 1 else "disabled",
            )
            up_button.pack(side="left", padx=(0, 2), ipady=1)

            down_button = tk.Button(
                order_frame,
                text=DOWN_ARROW,
                command=lambda i=index: self.move_todo_down(i),
                font=("Segoe UI Symbol", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                disabledforeground="#c7c7c7",
                relief="flat",
                width=2,
                state="normal" if index > 0 else "disabled",
            )
            down_button.pack(side="left", ipady=1)

            edit_button = tk.Button(
                row,
                text="Edit",
                command=lambda i=index: self.open_edit_dialog("todos", i),
                font=("Segoe UI", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                relief="flat",
                width=5,
            )
            edit_button.grid(row=0, column=3, padx=(0, 6), pady=8, sticky="ne")

            delete_button = tk.Button(
                row,
                text="Delete",
                command=lambda i=index: self.delete_todo(i),
                font=("Segoe UI", 9),
                bg="#eeeeee",
                relief="flat",
                width=6,
            )
            delete_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="ne")

            row.bind(
                "<Configure>",
                lambda event, item_label=label: item_label.configure(
                    wraplength=max(70, event.width - 230)
                ),
            )

            self.rows.append(row)

        self.update_idletasks()
        self.update_scroll_region()

    def render_plans(self):
        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.check_vars.clear()

        if not self.plans:
            empty = tk.Label(
                self.list_frame,
                text="No plans yet",
                font=("Segoe UI", 11),
                bg="#f5f5f5",
                fg="#777777",
            )
            empty.pack(fill="x", pady=28)
            self.rows.append(empty)
            self.update_idletasks()
            self.update_scroll_region()
            return

        for index, plan in reversed(list(enumerate(self.plans))):
            row = tk.Frame(self.list_frame, bg="#ffffff", highlightthickness=1)
            row.configure(highlightbackground="#dddddd", highlightcolor="#dddddd")
            row.grid_columnconfigure(1, weight=1, minsize=80)
            row.pack(fill="x", pady=4)

            done_var = tk.IntVar(value=1 if plan["done"] else 0)
            self.check_vars.append(done_var)
            check = tk.Checkbutton(
                row,
                variable=done_var,
                onvalue=1,
                offvalue=0,
                command=lambda i=index: self.toggle_plan(i),
                bg="#ffffff",
                activebackground="#ffffff",
                selectcolor="#ffffff",
                indicatoron=True,
                width=2,
            )
            check.grid(row=0, column=0, padx=(8, 4), pady=8, sticky="nw")

            label = tk.Label(
                row,
                text=plan["text"],
                anchor="w",
                font=("Segoe UI", 11, "overstrike" if plan["done"] else "normal"),
                bg="#ffffff",
                fg="#9ca3af" if plan["done"] else "#111827",
                wraplength=270,
                justify="left",
            )
            label.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="ew")
            label.bind(
                "<Double-Button-1>",
                lambda _event, i=index: self.open_edit_dialog("plans", i),
            )

            order_frame = tk.Frame(row, bg="#ffffff")
            order_frame.grid(row=0, column=2, padx=(0, 6), pady=7, sticky="ne")

            up_button = tk.Button(
                order_frame,
                text=UP_ARROW,
                command=lambda i=index: self.move_plan_up(i),
                font=("Segoe UI Symbol", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                disabledforeground="#c7c7c7",
                relief="flat",
                width=2,
                state="normal" if index < len(self.plans) - 1 else "disabled",
            )
            up_button.pack(side="left", padx=(0, 2), ipady=1)

            down_button = tk.Button(
                order_frame,
                text=DOWN_ARROW,
                command=lambda i=index: self.move_plan_down(i),
                font=("Segoe UI Symbol", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                disabledforeground="#c7c7c7",
                relief="flat",
                width=2,
                state="normal" if index > 0 else "disabled",
            )
            down_button.pack(side="left", ipady=1)

            edit_button = tk.Button(
                row,
                text="Edit",
                command=lambda i=index: self.open_edit_dialog("plans", i),
                font=("Segoe UI", 9),
                bg="#f3f4f6",
                activebackground="#e5e7eb",
                fg="#374151",
                relief="flat",
                width=5,
            )
            edit_button.grid(row=0, column=3, padx=(0, 6), pady=8, sticky="ne")

            delete_button = tk.Button(
                row,
                text="Delete",
                command=lambda i=index: self.delete_plan(i),
                font=("Segoe UI", 9),
                bg="#eeeeee",
                relief="flat",
                width=6,
            )
            delete_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="ne")

            row.bind(
                "<Configure>",
                lambda event, item_label=label: item_label.configure(
                    wraplength=max(70, event.width - 230)
                ),
            )

            self.rows.append(row)

        self.update_idletasks()
        self.update_scroll_region()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
