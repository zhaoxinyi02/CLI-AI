# CLI-AI 使用示例 | Usage Examples

本文档提供 CLI-AI v2.2 的详细使用示例，包括 AI 功能的实际应用场景。

## 目录

1. [基础使用](#基础使用)
2. [AI 智能命令解析](#ai-智能命令解析)
3. [AI 错误分析与修复](#ai-错误分析与修复)
4. [智能命令建议](#智能命令建议)
5. [配置示例](#配置示例)

---

## 基础使用

### 启动程序

```bash
python3 cli_ai.py
```

### 基本命令交互

```
CLI-AI> 查看当前目录
我将执行命令: pwd
是否继续？(y/n): y
执行成功:
/home/user/CLI-AI

CLI-AI> 列出所有文件
我将执行命令: ls -la
是否继续？(y/n): y
执行成功:
total 48
drwxr-xr-x 2 user user 4096 Jan  5 10:00 .
...
```

---

## AI 智能命令解析

### 功能说明

当 `USE_AI_PARSING = True` 时（默认启用），CLI-AI 使用 AI 模型理解自然语言并生成命令。

### 中文输入示例

#### 简单命令

```
CLI-AI> 查看磁盘使用情况
🤖 AI 解析
我将执行命令: df -h
是否继续？(y/n): y
执行成功:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   30G   18G  63% /
...
```

#### 复杂描述

```
CLI-AI> 查找当前目录下所有的 Python 文件
🤖 AI 解析
我将执行命令: find . -name "*.py"
是否继续？(y/n): y
执行成功:
./cli_ai.py
./config.py
./ai_provider.py
...
```

#### 带参数的操作

```
CLI-AI> 创建一个名为 myproject 的文件夹并设置权限为 755
🤖 AI 解析
我将执行命令: mkdir myproject && chmod 755 myproject
是否继续？(y/n): y
执行成功
```

### 英文输入示例

```
CLI-AI> show me all running processes
🤖 AI 解析
我将执行命令: ps aux
是否继续？(y/n): y
执行成功:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  77616  8984 ?        Ss   Jan05   0:01 /sbin/init
...
```

```
CLI-AI> check network connectivity to google
🤖 AI 解析
我将执行命令: ping -c 4 google.com
是否继续？(y/n): y
执行成功:
PING google.com (142.250.185.46): 56 data bytes
64 bytes from 142.250.185.46: icmp_seq=0 ttl=117 time=12.3 ms
...
```

### AI 解析的优势

- **更自然的表达**：不需要记忆固定短语
- **上下文理解**：能理解复杂的描述
- **多种表达方式**：同一意图可用不同方式表达
- **智能参数识别**：自动识别并处理参数

---

## AI 错误分析与修复

### 功能说明

当 `AI_ERROR_ANALYSIS = True` 时（默认启用），命令执行失败后会自动分析错误并提供修复建议。

### 权限错误示例

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
是否执行建议的命令？(y/n): y

我将执行命令: sudo cat /root/secret.txt
[sudo] password for user:
执行成功:
[文件内容]
```

### 命令不存在示例

```
CLI-AI> htop
我将执行命令: htop
是否继续？(y/n): y

执行失败:
bash: htop: command not found
返回码: 127

🔍 分析错误...
原因: 命令未找到
建议: 请检查命令是否正确，或需要安装相应软件包

建议的替代命令: sudo apt install htop
是否执行建议的命令？(y/n): y
```

### 文件不存在示例

```
CLI-AI> 删除文件 nonexistent.txt
我将执行命令: rm nonexistent.txt
是否继续？(y/n): y

执行失败:
rm: cannot remove 'nonexistent.txt': No such file or directory
返回码: 1

🔍 分析错误...
原因: 文件或目录不存在
建议: 请检查文件路径是否正确
```

### 错误分析功能特点

- **智能诊断**：自动识别错误类型
- **具体建议**：提供可操作的解决方案
- **一键修复**：生成替代命令并询问是否执行
- **学习价值**：帮助理解错误原因

---

## 智能命令建议

### 功能说明

当 `AUTO_CONTINUE_MODE = True` 时，AI 会在命令成功执行后建议下一步操作。

**注意**：此功能默认关闭，可在 `config.py` 中启用。

### 文件夹创建后的建议

```
CLI-AI> mkdir myproject
我将执行命令: mkdir myproject
是否继续？(y/n): y
执行成功

💡 建议: 进入刚创建的目录
是否执行？(y/n): y

🤖 AI 解析
我将执行命令: cd myproject
是否继续？(y/n): y
执行成功
```

### 查看文件后的建议

```
CLI-AI> ls -la
我将执行命令: ls -la
是否继续？(y/n): y
执行成功:
total 48
-rw-r--r-- 1 user user 1234 Jan  5 config.py
-rw-r--r-- 1 user user 5678 Jan  5 cli_ai.py
...

💡 建议: 查看 config.py 文件的内容
是否执行？(y/n): y

🤖 AI 解析
我将执行命令: cat config.py
是否继续？(y/n): y
```

### 磁盘空间不足的建议

```
CLI-AI> df -h
我将执行命令: df -h
是否继续？(y/n): y
执行成功:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   48G   2.0G  96% /

💡 建议: 磁盘使用率很高，建议查找大文件或清理空间
是否执行？(y/n): y

🤖 AI 解析
我将执行命令: du -sh /* | sort -rh | head -10
是否继续？(y/n): y
```

### 自动建议的特点

- **情境感知**：基于当前操作和输出
- **工作流延续**：自然衔接多个操作
- **学习友好**：帮助新手了解常见操作流程
- **可控性**：所有建议都需要用户确认

---

## 配置示例

### 配置文件位置

- **主配置**：`config.py`
- **API 密钥**：`.env`

### config.py 完整配置示例

```python
# 命令历史配置
HISTORY_FILE = "command_history.txt"
ENABLE_HISTORY = True
MAX_HISTORY_ENTRIES = 1000

# 危险命令模式
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    # ... 更多模式
]

# AI 功能配置
USE_AI_PARSING = True           # 启用 AI 智能解析
AI_ERROR_ANALYSIS = True        # 启用 AI 错误分析
AUTO_CONTINUE_MODE = False      # 自动建议模式（按需启用）

# 其他配置
COMMAND_TIMEOUT = 30
FUZZY_MATCH_THRESHOLD = 0.5
```

### .env 配置示例

#### 使用 OpenAI

```bash
# OpenAI 配置
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

#### 使用 DeepSeek

```bash
# DeepSeek 配置
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-actual-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

### 快速配置步骤

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env 文件
nano .env
# 或
vim .env

# 3. 填入你的 API 密钥
# 选择 OpenAI 或 DeepSeek，修改对应的配置

# 4. 测试配置
python3 test_ai_provider.py

# 5. 启动程序
python3 cli_ai.py
```

---

## 最佳实践

### 1. 逐步启用 AI 功能

```python
# 第一步：先体验 AI 命令解析
USE_AI_PARSING = True
AI_ERROR_ANALYSIS = False
AUTO_CONTINUE_MODE = False

# 第二步：启用错误分析
USE_AI_PARSING = True
AI_ERROR_ANALYSIS = True
AUTO_CONTINUE_MODE = False

# 第三步：根据需要启用自动建议
USE_AI_PARSING = True
AI_ERROR_ANALYSIS = True
AUTO_CONTINUE_MODE = True  # 适合学习者
```

### 2. 选择合适的 AI 提供商

- **OpenAI (GPT-4)**：理解能力强，响应准确
- **DeepSeek**：性价比高，中文支持好

### 3. 安全使用建议

- 始终仔细阅读 AI 生成的命令
- 对危险操作保持警惕
- 利用确认机制避免误操作
- 定期查看命令历史

### 4. 学习建议

- 观察 AI 如何理解你的描述
- 注意错误分析中的建议
- 尝试不同的表达方式
- 从自动建议中学习常见操作流程

---

## 故障排除

### AI 功能不可用

**症状**：显示 "⚠️ AI 命令解析初始化失败"

**解决方案**：
1. 检查 `.env` 文件是否存在
2. 确认 API 密钥配置正确
3. 测试网络连接
4. 运行 `python3 test_ai_provider.py` 诊断

### 降级到规则匹配模式

如果 AI 功能不可用，程序会自动降级：

```python
# 在 config.py 中禁用 AI
USE_AI_PARSING = False
AI_ERROR_ANALYSIS = False
AUTO_CONTINUE_MODE = False
```

程序将使用传统的规则匹配模式，仍可正常工作。

---

## 更多资源

- **完整文档**：[README.md](README.md)
- **快速开始**：[QUICKSTART.md](QUICKSTART.md)
- **功能演示**：运行 `python3 demo_features.py`
- **测试套件**：
  - `python3 test_ai_command_parser.py`
  - `python3 test_ai_error_analyzer.py`
  - `python3 test_ai_provider.py`

---

## 反馈与贡献

遇到问题或有改进建议？欢迎：
- 提交 Issue
- 发起 Pull Request
- 分享你的使用经验
