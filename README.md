# SimpleTodo

一个使用 Python Tkinter 编写的轻量桌面待办应用，无需安装第三方运行时依赖。

## 功能

- 分别管理 To-dos 和 Plans
- 添加、完成、编辑和删除条目
- 调整条目顺序
- 自动保存数据到程序所在目录的 `.simple_todos.json`

## 运行

需要 Python 3，并确保 Python 安装包含 Tkinter。

```powershell
python todo_app\todo_app.py
```

## 打包 Windows 应用

安装 PyInstaller 后，使用仓库中的配置文件构建：

```powershell
python -m pip install pyinstaller
pyinstaller SimpleTodo.spec
```

生成的应用位于 `dist\SimpleTodo.exe`。应用数据会保存在可执行文件所在目录。
