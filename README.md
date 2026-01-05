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
- `config`: 查看和管理配置（详见下方配置管理章节）
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
├── README.md                   # 项目说明文档
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略文件
├── .env.example                # 环境变量配置示例
├── cli_ai.py                   # 主程序入口
├── nlp_parser.py               # 自然语言解析模块（规则匹配）
├── command_executor.py         # 命令执行模块
├── command_mappings.py         # 命令映射规则
├── config.py                   # 配置文件
├── config_manager.py           # 配置管理模块 (v2.3)
├── ai_provider.py              # AI 提供商抽象层 (v2.0)
├── ai_command_parser.py        # AI 命令解析器 (v2.1)
├── ai_error_analyzer.py        # AI 错误分析器 (v2.2)
├── test_ai_provider.py         # AI 集成测试
├── test_ai_command_parser.py   # AI 命令解析器测试 (v2.1)
├── test_ai_error_analyzer.py   # AI 错误分析器测试 (v2.2)
├── test_config_and_env.py      # 配置和环境变量测试 (v2.3)
└── prompts/                    # AI 提示词模板目录 (v2.1)
    ├── .gitkeep
    └── command_generation.txt  # 命令生成提示词
```

## 配置 | Configuration

你可以在 `config.py` 中修改配置：

**基础配置**：
- `HISTORY_FILE`: 命令历史文件路径
- `ENABLE_HISTORY`: 是否启用命令历史记录
- `MAX_HISTORY_ENTRIES`: 最大历史记录条数
- `DANGEROUS_PATTERNS`: 危险命令模式列表

**AI 功能配置** (v2.2)：
- `USE_AI_PARSING`: 启用 AI 智能命令解析（默认：True）
- `AI_ERROR_ANALYSIS`: 启用 AI 错误分析（默认：True）
- `AUTO_CONTINUE_MODE`: 启用自动建议模式（默认：False）

## 配置管理命令 | Config Command (v2.3)

CLI-AI v2.3 新增了 `config` 命令，可以直接从终端查看和编辑配置文件。

### 配置命令用法

```bash
# 显示当前配置
config

# 显示配置（包含完整的敏感信息）
config show --secrets

# 初始化配置文件（从 .env.example 创建 .env）
config init

# 设置配置项
config set AI_PROVIDER openai
config set OPENAI_API_KEY sk-your-key-here

# 使用编辑器编辑配置文件
config edit

# 显示配置命令帮助
config help
```

### 配置示例

在 CLI-AI 中使用配置命令：

```
CLI-AI> config init
✓ 已创建配置文件: .env

CLI-AI> config set AI_PROVIDER openai
✓ 已更新配置: AI_PROVIDER=openai

CLI-AI> config set OPENAI_API_KEY sk-xxx...
✓ 已更新配置: OPENAI_API_KEY=sk-xxx...

CLI-AI> config show
当前配置:
==================================================
  AI_PROVIDER: openai
  OPENAI_API_KEY: sk-x****xxx...
  OPENAI_BASE_URL: https://api.openai.com/v1
  OPENAI_MODEL: gpt-4
==================================================
```

### 安全特性

- **敏感信息保护**: 默认情况下，API 密钥等敏感信息会被部分隐藏
- **完整显示**: 使用 `config show --secrets` 查看完整信息
- **文件权限**: 建议将 .env 文件权限设置为 600（仅所有者可读写）

```bash
chmod 600 .env
```

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

### 代理配置 | Proxy Configuration (v2.3)

CLI-AI v2.3 支持通过代理服务器访问 AI API，支持 HTTP 和 SOCKS5 代理。

#### 配置代理

在 `.env` 文件中添加代理配置：

```bash
# HTTP 代理
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080

# SOCKS5 代理
HTTP_PROXY=socks5://127.0.0.1:1080
HTTPS_PROXY=socks5://127.0.0.1:1080

# 带认证的代理
HTTP_PROXY=http://username:password@proxy.example.com:8080
HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

#### SOCKS5 代理依赖

如果使用 SOCKS5 代理，需要安装额外依赖：

```bash
pip install httpx[socks]
```

如果没有安装此依赖，程序会显示警告并自动禁用 SOCKS5 代理。

#### 系统代理

代理配置也可以通过系统环境变量设置：

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
python3 cli_ai.py
```

#### 代理故障排除

如果代理配置无效，程序会：
1. 显示警告信息
2. 说明支持的代理格式
3. 继续运行但不使用代理

支持的代理格式：
- `http://...`
- `https://...`
- `socks5://...`
- `socks5h://...`（DNS 解析通过代理）

## AI 命令解析器 | AI Command Parser (v2.1)

CLI-AI v2.1 引入了智能命令解析模块，能够将自然语言直接转换为 Linux 命令。

### 功能特性

- **智能解析**：使用 AI 模型理解自然语言并生成准确的命令
- **双语支持**：支持中文和英文输入
- **命令清洗**：自动去除 AI 返回的代码块标记和解释文字
- **单轮对话**：每次调用独立处理，专注于命令生成
- **错误处理**：完善的输入验证和错误处理机制

### 使用示例

```python
from ai_command_parser import AICommandParser

# 创建解析器
parser = AICommandParser()

# 中文输入
command = parser.parse_command("列出所有文件")
print(command)  # 输出: ls -la

# 英文输入
command = parser.parse_command("show disk usage")
print(command)  # 输出: df -h
```

### 测试命令解析器

运行测试文件验证功能：

```bash
# 测试 AI 命令解析
python test_ai_command_parser.py
```

测试包括：
- 命令清洗功能测试（不需要 API）
- 解析器初始化测试（不需要 API）
- 真实 API 调用测试（需要配置 .env）

### 模块架构

```
prompts/
├── .gitkeep
└── command_generation.txt    # AI 提示词模板

ai_command_parser.py          # AI 命令解析器
test_ai_command_parser.py     # 测试文件
```

## AI 功能详解 | AI Features (v2.2)

### 智能命令解析

CLI-AI v2.2 默认启用 AI 智能命令解析，可以理解更复杂的自然语言输入。

**配置方式**：
- 在 `config.py` 中设置 `USE_AI_PARSING = True`（默认启用）
- 需要配置 `.env` 文件中的 API 密钥

**功能特点**：
- 🧠 **智能理解**：使用 AI 模型深度理解自然语言意图
- 🌐 **更强的语言支持**：支持各种表达方式和复杂描述
- 🔄 **自动降级**：如果 AI 不可用，自动切换到规则匹配模式
- ⚡ **实时解析**：每次输入独立处理，响应迅速

### AI 错误分析

当命令执行失败时，AI 会自动分析错误原因并提供解决方案。

**配置方式**：
- 在 `config.py` 中设置 `AI_ERROR_ANALYSIS = True`（默认启用）

**功能特点**：
- 🔍 **智能诊断**：AI 分析错误输出，识别问题根源
- 💡 **解决建议**：提供具体的修复步骤
- 🔧 **替代命令**：自动生成修复命令，用户确认后执行
- 🛡️ **安全降级**：AI 不可用时使用基础模式识别常见错误

**使用示例**：
```
CLI-AI> cat /root/secret.txt
我将执行命令: cat /root/secret.txt
是否继续？(y/n): y

执行失败:
cat: /root/secret.txt: Permission denied
返回码: 1

🔍 分析错误...
原因: 权限不足
建议: 尝试使用 sudo 运行命令

建议的替代命令: sudo cat /root/secret.txt
是否执行建议的命令？(y/n): 
```

### 智能命令建议（自动模式）

命令执行成功后，AI 可以建议下一步的合理操作。

**配置方式**：
- 在 `config.py` 中设置 `AUTO_CONTINUE_MODE = True`（默认关闭）

**功能特点**：
- 🤖 **智能预测**：根据当前操作预测下一步需求
- 🔄 **工作流延续**：自然衔接多个相关操作
- 👤 **用户控制**：所有建议都需要用户确认
- 💭 **情境感知**：基于命令输出和执行结果做出判断

**使用示例**：
```
CLI-AI> 创建文件夹 myproject
我将执行命令: mkdir myproject
是否继续？(y/n): y
执行成功

💡 建议: 进入刚创建的目录
是否执行？(y/n): y

我将执行命令: cd myproject
...
```

### 配置参数说明

在 `config.py` 中可配置的 AI 功能参数：

```python
# AI 智能解析（推荐启用）
USE_AI_PARSING = True          # 使用 AI 解析自然语言

# AI 错误分析（推荐启用）
AI_ERROR_ANALYSIS = True       # 使用 AI 分析错误并提供建议

# 自动建议模式（可选）
AUTO_CONTINUE_MODE = False     # AI 建议下一步操作
```

### 测试 AI 功能

```bash
# 测试 AI 命令解析器
python test_ai_command_parser.py

# 测试 AI 错误分析器
python test_ai_error_analyzer.py

# 测试完整的 AI 集成
python test_ai_provider.py
```

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

## 故障排除 | Troubleshooting (v2.3)

### .env 文件相关问题

**问题: 程序提示 ".env 文件未找到"**

解决方案：
```bash
# 方案 1: 使用 config 命令初始化（推荐）
python3 cli_ai.py
# 在程序中输入: config init

# 方案 2: 手动复制示例文件
cp .env.example .env
# 然后编辑 .env 文件，填入你的 API 密钥
```

**问题: "API 密钥未配置"**

解决方案：
```bash
# 方案 1: 使用 config 命令设置
# 在 CLI-AI 中运行:
config set AI_PROVIDER openai
config set OPENAI_API_KEY sk-your-key-here

# 方案 2: 直接编辑 .env 文件
nano .env
# 添加或修改:
# AI_PROVIDER=openai
# OPENAI_API_KEY=sk-your-key-here
```

**问题: 修改了 .env 但没有生效**

解决方案：
- 重启 CLI-AI 程序
- 确保 .env 文件在当前工作目录
- 检查环境变量格式是否正确（没有多余空格）

### 代理相关问题

**问题: "代理 URL 格式无效"**

解决方案：
```bash
# 正确的代理格式示例
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=https://proxy.example.com:8080
HTTP_PROXY=socks5://127.0.0.1:1080

# 错误的格式
HTTP_PROXY=proxy.example.com:8080  # 缺少协议
HTTP_PROXY=ftp://proxy.com:8080    # 不支持的协议
```

**问题: "SOCKS5 代理需要安装额外依赖"**

解决方案：
```bash
pip install httpx[socks]
# 或者改用 HTTP 代理
```

**问题: 代理连接超时或失败**

排查步骤：
1. 检查代理服务器是否正常运行
2. 验证代理地址和端口是否正确
3. 如果代理需要认证，确保在 URL 中包含用户名和密码
4. 尝试在浏览器中使用相同的代理设置
5. 临时禁用代理测试是否是代理问题

### AI 功能相关问题

**问题: AI 命令解析初始化失败**

可能原因和解决方案：
1. **API 密钥未配置**: 使用 `config` 命令设置 API 密钥
2. **网络问题**: 检查网络连接，如在中国大陆可能需要配置代理
3. **API 额度用尽**: 检查你的 API 账户额度
4. **API 密钥无效**: 验证 API 密钥是否正确

程序会自动降级到规则匹配模式，不影响基础功能。

**问题: "AI 调用失败"**

解决方案：
```bash
# 1. 检查配置
config show

# 2. 验证网络连接
ping api.openai.com
# 或
ping api.deepseek.com

# 3. 检查代理设置（如果使用）
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 4. 查看详细错误信息
# 程序会显示具体的错误原因
```

### 权限相关问题

**问题: "Permission denied" 执行命令**

解决方案：
- 某些命令需要管理员权限，使用 `sudo` 前缀
- 或者在 CLI-AI 中输入 "切换到管理员" 进入 sudo 模式

**问题: 无法编辑 .env 文件**

解决方案：
```bash
# 检查文件权限
ls -l .env

# 修改文件权限（如果需要）
chmod 600 .env

# 或使用 sudo 编辑
sudo nano .env
```

### 获取更多帮助

如果以上方法都无法解决问题：

1. **查看日志**: 程序会输出详细的错误信息
2. **检查依赖**: `pip list | grep -E "openai|httpx|python-dotenv"`
3. **提交 Issue**: 在 GitHub 上提交问题，包含：
   - 错误信息的完整输出
   - 使用的操作系统和 Python 版本
   - .env 配置（隐藏敏感信息）
   - 复现步骤

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

### v2.3.0 (2026-01-05)
- ✨ 新增 `config` 命令用于配置管理
- 🔧 修复 .env 文件加载问题，添加文件存在性验证
- 🌐 新增代理支持（HTTP 和 SOCKS5）
- 🛡️ 增强错误处理和用户友好的错误消息
- 💡 改进 API 密钥和代理配置的错误提示
- 📚 添加详细的故障排除文档
- ✅ 新增配置和环境变量测试套件
- 🔐 配置显示时自动隐藏敏感信息
- 📦 代理配置支持自动降级和故障恢复

### v2.2.0 (2026-01-05)
- ✨ 集成 AI 智能命令解析到主程序流程
- 🔍 新增 AI 错误分析功能 (`ai_error_analyzer.py`)
- 💡 新增智能命令建议功能（自动建议下一步操作）
- ⚙️ 新增配置选项：`USE_AI_PARSING`、`AI_ERROR_ANALYSIS`、`AUTO_CONTINUE_MODE`
- 🧪 添加错误分析器测试套件 (`test_ai_error_analyzer.py`)
- 🛡️ AI 模块初始化失败时自动降级到规则匹配模式
- 📚 完善 AI 功能文档和配置说明

### v2.1.0 (2026-01-05)
- ✨ 新增 AI 命令解析器模块 (`ai_command_parser.py`)
- ✨ 实现自然语言到 Linux 命令的智能转换
- 📝 创建提示词模板系统 (`prompts/command_generation.txt`)
- 🧪 添加命令解析器测试套件 (`test_ai_command_parser.py`)
- 🛡️ 实现命令清洗和格式验证功能
- 📚 更新文档，添加 AI 命令解析器使用说明

### v2.0.0 (2026-01-04)
- 集成 AI 模型支持 (OpenAI, DeepSeek)
- 添加 AI 提供商抽象层
- 支持通过环境变量配置 AI 模型

### v1.0.0 (2026-01-04)
- 初始版本发布
- 支持中英文自然语言输入
- 实现基础命令映射和执行
- 添加安全检查和命令历史
