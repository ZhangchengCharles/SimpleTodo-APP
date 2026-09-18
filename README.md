# SimpleTodo

SimpleTodo 是一个轻量的 Windows 桌面待办工具，可以分别管理当前任务（To-dos）和未来计划（Plans）。数据只保存在本机，关闭程序后仍会保留。

![SimpleTodo 界面预览](docs/simpletodo.png)

## 安装与启动

SimpleTodo 不需要传统安装，也不需要额外的 Python 软件包。

### 1. 安装 Python

如果电脑尚未安装 Python：

1. 前往 [Python 官网](https://www.python.org/downloads/windows/) 下载 Python 3。
2. 运行安装程序时，勾选 **Add python.exe to PATH**。
3. 安装完成后，重新打开 PowerShell，运行以下命令确认安装成功：

```powershell
python --version
```

看到 `Python 3.x.x` 即表示可以继续。如果使用 Miniconda 或 Anaconda，已有的 Python 3 也可以直接使用。

### 2. 下载 SimpleTodo

1. 在本仓库页面点击 **Code** → **Download ZIP**。
2. 解压下载的 ZIP 文件。
3. 打开解压后的 `SimpleTodo-APP` 文件夹。

也可以使用 Git：

```powershell
git clone https://github.com/ZhangchengCharles/SimpleTodo-APP.git
cd SimpleTodo-APP
```

### 3. 启动应用

在 `SimpleTodo-APP` 文件夹空白处右键，选择 **在终端中打开**，然后运行：

```powershell
python todo_app\todo_app.py
```

如果系统使用 Python Launcher，也可以运行：

```powershell
py todo_app\todo_app.py
```

## 如何使用

- **切换列表**：点击窗口底部的 **To-dos** 或 **Plans**。
- **添加**：在顶部输入内容，按 `Enter` 或点击 **Add Todo / Add Plan**。
- **标记完成**：点击条目前的复选框；再次点击可恢复为未完成。
- **编辑**：点击 **Edit** 或双击条目文字。点击 **Save** 保存，也可以按 `Ctrl+Enter`；按 `Esc` 取消。
- **调整顺序**：点击条目右侧的 `↑` 或 `↓`。
- **删除**：点击 **Delete**，条目会立即删除。

## 数据保存与备份

每次修改都会自动保存到 `.simple_todos.json`：

- 使用 Python 启动时，文件位于运行命令时所在的文件夹。
- 使用打包后的程序时，文件位于 `SimpleTodo.exe` 所在的文件夹。

备份或迁移数据时，先关闭 SimpleTodo，再复制 `.simple_todos.json` 即可。

## 构建 Windows 程序

需要生成独立的 `.exe` 时，安装 PyInstaller 并使用仓库中的配置：

```powershell
python -m pip install pyinstaller
pyinstaller SimpleTodo.spec
```

生成的程序位于 `dist\SimpleTodo.exe`。
