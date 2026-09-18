# SimpleTodo

SimpleTodo 是一个简洁的桌面待办工具，用来分别管理近期任务和未来计划。数据保存在本地，关闭应用后不会丢失。

## 启动应用

需要安装 Python 3，程序使用 Python 自带的 Tkinter，无需安装其他运行依赖。

1. 下载或克隆本仓库。
2. 在仓库目录打开 PowerShell。
3. 运行：

```powershell
python todo_app\todo_app.py
```

## 如何使用

窗口底部有两个列表：

- **To-dos**：记录当前需要完成的任务。
- **Plans**：记录之后要做的计划。

选择列表后，可以进行以下操作：

- **添加**：在顶部输入内容，按 `Enter` 或点击 **Add Todo / Add Plan**。
- **标记完成**：点击条目前的复选框；再次点击可以恢复为未完成。
- **编辑**：点击 **Edit**，或双击条目文字。修改后点击 **Save**；也可以按 `Ctrl+Enter` 保存、按 `Esc` 取消。
- **调整顺序**：点击条目右侧的 `↑` 或 `↓`。
- **删除**：点击 **Delete**。删除会立即生效。
- **切换列表**：点击窗口底部的 **To-dos** 或 **Plans**。

## 数据保存

每次修改都会自动保存到 `.simple_todos.json`：

- 使用 Python 启动时，文件位于运行命令时所在的目录。
- 使用打包后的程序时，文件位于 `SimpleTodo.exe` 所在的目录。

如需备份或迁移数据，关闭应用后复制该文件即可。

## 构建 Windows 程序

开发者可以使用仓库中的 PyInstaller 配置生成独立的 Windows 应用：

```powershell
python -m pip install pyinstaller
pyinstaller SimpleTodo.spec
```

生成文件位于 `dist\SimpleTodo.exe`。
