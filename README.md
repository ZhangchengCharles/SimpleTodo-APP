# SimpleTodo

A small Windows desktop app that keeps each project's tasks in its own folder. Use **To-dos** for current tasks and **Plans** for future work.

Place a copy of `SimpleTodo.exe` in each project folder and double-click it to open that project's list. The folder path appears at the bottom of the window, so you can see which project you are working on. Separate lists keep you focused on the current project, and your tasks travel with the folder when you move or back it up.

<p align="center">
  <img src="docs/simpletodo.png" alt="SimpleTodo showing tasks for Project-A" width="385">
</p>

## Get started

### Use the portable app

If you already have `SimpleTodo.exe`, copy it into your project folder and double-click it. Repeat for any other projects you want to track.

To build the executable from this repository, download **Code → Download ZIP**, extract it, and open a terminal in the extracted folder containing `SimpleTodo.spec`. With Python 3 available, run:

```powershell
python -m pip install pyinstaller
python -m PyInstaller SimpleTodo.spec
```

Copy the resulting `dist\SimpleTodo.exe` into your project folders. The built app runs without Python installed.

### Run from source

With Python 3 and Tkinter available, open a terminal in the extracted repository folder and run:

```powershell
python todo_app\todo_app.py
```

When running from source, the list belongs to the terminal's current folder. To use another project's list, open a terminal in that project folder and run the script using its full path.

## Everyday use

- **Choose a list:** Select **To-dos** or **Plans** at the bottom.
- **Add:** Type in the top field, then press `Enter` or click **Add Todo / Add Plan**.
- **Complete:** Click an item's checkbox. Click again to mark it incomplete.
- **Edit:** Click **Edit** or double-click the text. Click **Save** or press `Ctrl+Enter` to save; press `Esc` to cancel.
- **Reorder:** Use `↑` and `↓` beside an item.
- **Delete:** Click **Delete** to remove an item immediately. There is no undo.

## Your data

Changes are saved automatically to `.simple_todos.json`. For the portable app, this file lives beside `SimpleTodo.exe`:

```text
Project-A/
├── SimpleTodo.exe
└── .simple_todos.json

Project-B/
├── SimpleTodo.exe
└── .simple_todos.json
```

Keep the app in a folder you can write to. To back up or move a project's lists, close the app and copy its `.simple_todos.json` file. Keep this file when replacing the executable with a newer version.
