# 功能增强文档 (Features 2.2.1 - 2.2.3)

## 概述

本次更新实现了三个主要增强功能，提升了 CLI-AI 的智能化水平和用户体验。

## 2.2.1 系统环境上下文感知

### 功能描述
`context_manager.py` 模块负责收集和管理系统环境上下文信息，使 AI 能够根据当前系统环境提供更精准的命令建议。

### 收集的信息
- **当前工作目录** (`pwd`): 用户当前所在的目录路径
- **当前用户名** (`whoami`): 执行命令的用户身份
- **操作系统信息** (`uname -s`): 系统类型（Linux, Darwin, Windows等）
- **系统架构** (`uname -m`): 处理器架构（x86_64, arm64等）

### 主要方法

#### `get_context()` 
返回包含所有上下文信息的字典。

```python
from context_manager import ContextManager

manager = ContextManager()
context = manager.get_context()
# 返回: {
#     'current_directory': '/home/user/project',
#     'username': 'user',
#     'os_name': 'Linux',
#     'architecture': 'x86_64'
# }
```

#### `get_context_string()`
返回格式化的上下文信息字符串，便于人类阅读。

```python
context_str = manager.get_context_string()
# 返回:
# 当前系统环境上下文:
# - 工作目录: /home/user/project
# - 用户名: user
# - 操作系统: Linux
# - 系统架构: x86_64
```

#### `get_context_for_ai()`
返回简洁格式的上下文信息，适合传递给 AI。

```python
ai_context = manager.get_context_for_ai()
# 返回: "User: user, Dir: /home/user/project, OS: Linux, Arch: x86_64"
```

### 使用示例

```python
from context_manager import ContextManager

# 创建上下文管理器
manager = ContextManager()

# 获取完整上下文
context = manager.get_context()
print(f"当前用户: {context['username']}")
print(f"工作目录: {context['current_directory']}")

# 获取格式化字符串
print(manager.get_context_string())

# 刷新上下文（如果切换了目录）
manager.refresh_context()
```

---

## 2.2.2 智能参数提取与验证

### 功能描述
扩展了 `ai_command_parser.py`，增加了从自然语言中提取、验证参数的能力，以及路径自动补全功能。

### 主要功能

#### 1. 参数提取 (`extract_parameters`)
从用户的自然语言输入中智能提取：
- **文件名**: 带扩展名的文件（如 `test.txt`, `config.json`）
- **路径**: 包含 `/` 或 `~` 的路径
- **数字**: 数值参数（如行数、次数等）
- **选项**: 命令行选项标志（如 `-l`, `--help`）

```python
from ai_command_parser import AICommandParser

parser = AICommandParser()
params = parser.extract_parameters("复制文件 test.txt 到 backup.txt")
# 返回: {
#     'files': ['test.txt', 'backup.txt'],
#     'paths': [],
#     'numbers': [],
#     'options': []
# }
```

#### 2. 参数验证 (`validate_parameters`)
验证命令中的路径和文件参数：
- 检查文件/目录是否存在
- 区分读取操作和创建操作
- 返回验证结果和警告信息

```python
is_valid, warnings = parser.validate_parameters("cat test.txt")
# 如果 test.txt 不存在:
# is_valid = False
# warnings = ['路径不存在: test.txt']
```

#### 3. 路径自动补全 (`autocomplete_path`)
智能补全路径，支持：
- 相对路径转绝对路径
- `~` 扩展为用户主目录
- 路径规范化（去除 `.` 和 `..`）

```python
# 补全相对路径
completed = parser.autocomplete_path("./test")
# 返回: "/home/user/project/test"

# 补全 ~ 路径
completed = parser.autocomplete_path("~/documents")
# 返回: "/home/user/documents"

# 补全当前目录
completed = parser.autocomplete_path(".")
# 返回: "/home/user/project"
```

### 使用示例

```python
from ai_command_parser import AICommandParser

parser = AICommandParser()

# 提取参数
user_input = "查看文件 log.txt 的最后 20 行"
params = parser.extract_parameters(user_input)
print(f"文件: {params['files']}")    # ['log.txt']
print(f"数字: {params['numbers']}")  # ['20']

# 补全路径
relative_path = "./data/file.txt"
absolute_path = parser.autocomplete_path(relative_path)
print(f"绝对路径: {absolute_path}")

# 验证参数
command = "cat existing_file.txt"
is_valid, warnings = parser.validate_parameters(command)
if not is_valid:
    for warning in warnings:
        print(f"警告: {warning}")
```

---

## 2.2.3 场景化 Prompt 优化

### 功能描述
根据用户输入的意图，自动选择最适合的 Prompt 模板，提高命令生成的准确性。

### 支持的场景

#### 1. 文件操作场景 (`file_operations.txt`)
- **适用操作**: 创建、删除、复制、移动、重命名、查找文件
- **关键词**: 创建、删除、复制、移动、文件、目录、mkdir、rm、cp、mv等
- **示例输入**: "创建文件夹 test", "复制文件 a.txt 到 b.txt"

#### 2. 系统管理场景 (`system_management.txt`)
- **适用操作**: 进程管理、用户管理、服务管理、权限管理
- **关键词**: 进程、用户、组、服务、权限、ps、top、kill、useradd等
- **示例输入**: "查看所有进程", "创建用户 john", "启动服务"

#### 3. 网络操作场景 (`network_operations.txt`)
- **适用操作**: 下载、上传、网络诊断、SSH连接
- **关键词**: 下载、上传、网络、ping、wget、curl、ssh、ftp等
- **示例输入**: "下载文件 http://example.com/file.zip", "ping 测试"

#### 4. 文本处理场景 (`text_processing.txt`)
- **适用操作**: 查看、编辑、搜索、替换文本内容
- **关键词**: 查看、编辑、搜索、cat、grep、sed、nano、vim等
- **示例输入**: "查看文件内容", "编辑配置文件", "搜索关键词"

### 场景检测逻辑

系统使用智能算法自动检测场景：
1. **特殊规则优先**: 如检测到 URL，优先判定为网络操作
2. **上下文感知**: 结合多个关键词判断真实意图
3. **关键词评分**: 统计匹配的关键词数量
4. **冲突解决**: 当多个场景得分相同时，按优先级选择

### 主要方法

#### `_detect_scenario(user_input)`
自动检测用户输入属于哪个场景。

```python
scenario = parser._detect_scenario("创建文件夹 test")
# 返回: 'file_operations'
```

#### `get_scenario_info(user_input)`
获取场景信息，包括场景类型和对应的提示词文件。

```python
info = parser.get_scenario_info("下载文件")
# 返回: {
#     'scenario': 'network_operations',
#     'prompt_file': 'prompts/network_operations.txt'
# }
```

#### `parse_command(user_input, auto_detect_scenario=True)`
解析命令时自动检测并使用对应场景的提示词。

```python
# 自动检测场景（默认行为）
command = parser.parse_command("创建文件夹 test", auto_detect_scenario=True)

# 禁用自动检测，使用默认提示词
command = parser.parse_command("创建文件夹 test", auto_detect_scenario=False)
```

### 使用示例

```python
from ai_command_parser import AICommandParser

parser = AICommandParser()

# 示例 1: 文件操作
info = parser.get_scenario_info("删除文件 test.txt")
print(f"场景: {info['scenario']}")  # file_operations
print(f"提示词: {info['prompt_file']}")

# 示例 2: 系统管理
info = parser.get_scenario_info("查看所有进程")
print(f"场景: {info['scenario']}")  # system_management

# 示例 3: 网络操作
info = parser.get_scenario_info("下载 http://example.com/file.zip")
print(f"场景: {info['scenario']}")  # network_operations

# 示例 4: 文本处理
info = parser.get_scenario_info("编辑文件 config.txt")
print(f"场景: {info['scenario']}")  # text_processing
```

---

## 集成使用

所有功能已无缝集成到 `AICommandParser` 中：

```python
from ai_command_parser import AICommandParser

# 创建解析器（自动启用上下文感知）
parser = AICommandParser(use_context=True)

# 用户输入
user_input = "创建文件夹 my_project"

# 1. 自动检测场景
scenario_info = parser.get_scenario_info(user_input)
print(f"检测场景: {scenario_info['scenario']}")

# 2. 提取参数
params = parser.extract_parameters(user_input)
print(f"提取的参数: {params}")

# 3. 获取系统上下文
if parser.context_manager:
    context = parser.context_manager.get_context_for_ai()
    print(f"系统上下文: {context}")

# 4. 生成命令（结合以上所有信息）
# 需要配置 .env 文件
# command = parser.parse_command(user_input)
# print(f"生成的命令: {command}")
```

---

## 测试

### 运行测试

```bash
# 测试上下文管理器
python test_context_manager.py

# 测试增强的命令解析器
python test_enhanced_parser.py

# 运行演示
python demo_enhanced_features.py
```

### 测试覆盖
- ✅ 上下文信息收集和格式化
- ✅ 参数提取（文件、路径、数字、选项）
- ✅ 路径自动补全
- ✅ 参数验证
- ✅ 场景检测（4种场景）
- ✅ Prompt 选择
- ✅ 命令清洗

---

## 配置

### 启用/禁用上下文感知

```python
# 启用上下文感知（默认）
parser = AICommandParser(use_context=True)

# 禁用上下文感知
parser = AICommandParser(use_context=False)
```

### 自定义 Prompt 文件

```python
# 使用自定义 prompt 文件
parser = AICommandParser(prompt_file="prompts/custom_prompt.txt")

# 不指定 prompt 文件，完全依赖场景检测
parser = AICommandParser(prompt_file=None)
```

---

## 文件结构

```
CLI-AI/
├── context_manager.py              # 上下文管理器（新增）
├── ai_command_parser.py            # 增强的命令解析器（更新）
├── test_context_manager.py         # 上下文管理器测试（新增）
├── test_enhanced_parser.py         # 增强功能测试（新增）
├── demo_enhanced_features.py       # 功能演示（新增）
├── prompts/
│   ├── file_operations.txt         # 文件操作场景提示词（新增）
│   ├── system_management.txt       # 系统管理场景提示词（新增）
│   ├── network_operations.txt      # 网络操作场景提示词（新增）
│   ├── text_processing.txt         # 文本处理场景提示词（新增）
│   └── command_generation.txt      # 默认提示词（已存在）
└── ENHANCED_FEATURES.md            # 本文档（新增）
```

---

## 性能优化

- **上下文缓存**: `ContextManager` 会缓存上下文信息，避免重复系统调用
- **懒加载**: 只在需要时才加载和处理提示词文件
- **轻量检测**: 场景检测使用高效的关键词匹配算法

---

## 常见问题

### Q: 如何刷新系统上下文？
A: 使用 `context_manager.refresh_context()` 方法。

### Q: 如何添加新的场景？
A: 
1. 在 `prompts/` 目录下创建新的提示词文件
2. 在 `AICommandParser.SCENARIO_KEYWORDS` 中添加场景关键词
3. 在 `_select_prompt_by_scenario()` 中添加场景映射

### Q: 参数提取不准确怎么办？
A: 参数提取使用正则表达式，可能不完美。可以通过改进 `extract_parameters()` 方法中的正则模式来提高准确性。

### Q: 如何禁用场景自动检测？
A: 调用 `parse_command()` 时设置 `auto_detect_scenario=False`。

---

## 未来改进

- [ ] 支持更多场景（如数据库操作、容器管理等）
- [ ] 改进参数提取算法，使用 NLP 技术
- [ ] 添加参数类型推断和转换
- [ ] 支持用户自定义场景和关键词
- [ ] 添加场景切换的置信度评分

---

## 贡献

欢迎贡献新的场景 Prompt 模板或改进现有功能！请参考项目的 CONTRIBUTING.md 文件。

## 许可证

MIT License
