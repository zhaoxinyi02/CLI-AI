# CLI-AI: Terminal AI Assistant

一个帮助 Linux 初学者通过自然语言执行 Linux 命令的终端 AI 助手。

A terminal AI assistant that helps Linux beginners execute Linux commands using natural language.

## 功能特点 | Features

- 🌐 **双语支持**: 支持中文和英文自然语言输入
- 🛡️ **安全执行**: 在执行命令前进行确认，危险命令额外警告
- 📝 **命令历史**: 自动记录所有执行的命令
- 🔄 **交互式支持**: 支持需要用户输入的交互式命令（如 `sudo su`, `nano` 等）
- 🎨 **友好界面**: 彩色终端输出，清晰易读
- 🔧 **可扩展**: 支持自定义命令映射

## 安装 | Installation

### 前置要求

- Python 3.6+
- Linux 操作系统（或 macOS）

### 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/zhaoxinyi02/CLI-AI.git
cd CLI-AI
```

2. 安装依赖（可选，用于彩色输出）：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python3 cli_ai.py
```

或者直接运行：
```bash
./cli_ai.py
```

## 使用方法 | Usage

启动程序后，你可以用自然语言描述你想执行的操作：

```
CLI-AI> 查看当前目录
我将执行命令: pwd
是否继续？(y/n): y
执行成功:
/home/user

CLI-AI> 列出文件
我将执行命令: ls -la
是否继续？(y/n): y
执行成功:
total 48
drwxr-xr-x 2 user user 4096 Jan  4 10:00 .
...

CLI-AI> 创建文件夹 test
我将执行命令: mkdir test
是否继续？(y/n): y
执行成功
```

### 特殊命令

- `help` 或 `帮助`: 显示帮助信息和常用命令示例
- `history` 或 `历史`: 查看命令执行历史
- `exit` 或 `quit` 或 `退出`: 退出程序

## 支持的命令 | Supported Commands

### 系统管理

| 自然语言 | Linux 命令 |
|---------|-----------|
| 切换到管理员 / switch to administrator | `sudo su` |
| 查看当前目录 / show current directory | `pwd` |
| 列出文件 / list files | `ls -la` |
| 查看磁盘空间 / disk space | `df -h` |
| 查看内存使用 / memory usage | `free -h` |
| 查看系统信息 / system info | `uname -a` |

### 文件操作

| 自然语言 | Linux 命令 |
|---------|-----------|
| 创建文件夹 test / create folder test | `mkdir test` |
| 删除文件 test.txt / remove file test.txt | `rm test.txt` |
| 删除文件夹 test / remove folder test | `rm -r test` |
| 查找文件 test.txt / find file test.txt | `find . -name test.txt` |
| 查看文件内容 test.txt / show file test.txt | `cat test.txt` |
| 编辑文件 test.txt / edit file test.txt | `nano test.txt` |
| 复制文件 a.txt b.txt / copy file a.txt b.txt | `cp a.txt b.txt` |
| 移动文件 a.txt b.txt / move file a.txt b.txt | `mv a.txt b.txt` |

### 进程管理

| 自然语言 | Linux 命令 |
|---------|-----------|
| 查看进程 / show processes | `ps aux` |
| 系统监控 / monitor system | `top` |
| 查看进程树 / process tree | `pstree` |

### 网络操作

| 自然语言 | Linux 命令 |
|---------|-----------|
| 查看网络 / show ip | `ip addr` |
| ping测试 / test network | `ping -c 4 8.8.8.8` |
| 查看端口 / show ports | `netstat -tuln` |

### 软件包管理

| 自然语言 | Linux 命令 |
|---------|-----------|
| 更新软件 / update packages | `sudo apt update` |
| 升级软件 / upgrade packages | `sudo apt upgrade` |
| 安装软件 vim / install package vim | `sudo apt install vim` |
| 删除软件 vim / remove package vim | `sudo apt remove vim` |

### 其他常用命令

| 自然语言 | Linux 命令 |
|---------|-----------|
| 清屏 / clear screen | `clear` |
| 查看历史 / command history | `history` |
| 查看日期 / show date | `date` |
| 重启 / reboot | `sudo reboot` |
| 关机 / shutdown | `sudo shutdown -h now` |

## 安全特性 | Safety Features

1. **执行前确认**: 所有命令在执行前都需要用户确认
2. **危险命令警告**: 对可能造成数据丢失或系统损坏的命令进行额外警告
3. **命令历史记录**: 自动记录所有执行的命令到 `command_history.txt`
4. **取消选项**: 用户可以随时取消命令执行

### 危险命令检测

程序会检测以下危险模式并给予额外警告：
- `rm -rf /`
- `rm -rf *`
- `dd if=...of=/dev/`
- `mkfs.*`
- `chmod -R 777 /`
- 等等

## 项目结构 | Project Structure

```
CLI-AI/
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖
├── .gitignore            # Git 忽略文件
├── .env.example          # 环境变量配置示例
├── cli_ai.py             # 主程序入口
├── nlp_parser.py         # 自然语言解析模块
├── command_executor.py   # 命令执行模块
├── command_mappings.py   # 命令映射规则
├── config.py             # 配置文件
├── ai_provider.py        # AI 提供商抽象层
└── test_ai_provider.py   # AI 集成测试
```

## 配置 | Configuration

你可以在 `config.py` 中修改配置：

- `HISTORY_FILE`: 命令历史文件路径
- `ENABLE_HISTORY`: 是否启用命令历史记录
- `MAX_HISTORY_ENTRIES`: 最大历史记录条数
- `DANGEROUS_PATTERNS`: 危险命令模式列表

## AI 配置 | AI Configuration

CLI-AI v2.0 支持使用真实的 AI 模型进行智能命令识别。

### 配置步骤

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API 密钥：
   - 使用 OpenAI：设置 `AI_PROVIDER=openai` 和 `OPENAI_API_KEY`
   - 使用 DeepSeek：设置 `AI_PROVIDER=deepseek` 和 `DEEPSEEK_API_KEY`

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 测试 AI 集成：
   ```bash
   python test_ai_provider.py
   ```

### 支持的 AI 提供商

- **OpenAI**：GPT-4, GPT-3.5-turbo 等
- **DeepSeek**：deepseek-chat, deepseek-coder 等

## 扩展功能 | Extensions

### 添加自定义命令映射

你可以在 `command_mappings.py` 中添加自己的命令映射：

```python
COMMAND_MAPPINGS = {
    "我的自定义命令": "linux command",
    # ... 更多映射
}
```

## 常见问题 | FAQ

**Q: 为什么有些命令执行后没有输出？**

A: 某些交互式命令（如 `sudo su`, `nano`）会直接在终端中运行，不会显示在程序输出中。

**Q: 如何查看命令历史？**

A: 在程序中输入 `history` 或 `历史`，或直接查看 `command_history.txt` 文件。

**Q: 程序不理解我的命令怎么办？**

A: 输入 `help` 查看支持的命令示例，或者在 `command_mappings.py` 中添加自定义映射。

**Q: 如何贡献新的命令映射？**

A: 欢迎提交 Pull Request 添加新的命令映射到 `command_mappings.py`！

## 注意事项 | Notes

- 本工具仅用于学习和辅助目的
- 请谨慎执行任何命令，特别是涉及系统文件的命令
- 建议在测试环境中先熟悉程序功能
- 对于生产环境，请确保理解每个命令的作用

## 许可证 | License

MIT License

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

## 作者 | Author

zhaoxinyi02

## 更新日志 | Changelog

### v1.0.0 (2026-01-04)
- 初始版本发布
- 支持中英文自然语言输入
- 实现基础命令映射和执行
- 添加安全检查和命令历史
