# CLI-AI Quick Start Guide

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/zhaoxinyi02/CLI-AI.git
cd CLI-AI
```

### Step 2: Install dependencies (optional)
```bash
pip install -r requirements.txt
```
Note: The only dependency is `colorama` for colored terminal output, which is optional.

### Step 3: Run CLI-AI
```bash
python3 cli_ai.py
```

Or make it executable and run directly:
```bash
chmod +x cli_ai.py
./cli_ai.py
```

## First Commands

Once CLI-AI starts, try these commands:

### Chinese Examples
```
CLI-AI> help
CLI-AI> 查看当前目录
CLI-AI> 列出文件
CLI-AI> 创建文件夹 test
CLI-AI> 查看磁盘空间
CLI-AI> 查看内存使用
```

### English Examples
```
CLI-AI> help
CLI-AI> show current directory
CLI-AI> list files
CLI-AI> create folder test
CLI-AI> disk space
CLI-AI> memory usage
```

## Understanding the Workflow

1. **Input**: Type your command in natural language (Chinese or English)
2. **Parse**: CLI-AI converts it to a Linux command
3. **Confirm**: CLI-AI shows the command and asks for confirmation
4. **Execute**: After you confirm (type 'y'), the command is executed
5. **Result**: CLI-AI displays the command output or error

## Example Session

```
CLI-AI> 查看当前目录

我将执行命令: pwd
是否继续？(y/n): y
执行成功:
/home/user/CLI-AI

CLI-AI> 创建文件夹 myproject

我将执行命令: mkdir myproject
是否继续？(y/n): y
执行成功

CLI-AI> 列出文件

我将执行命令: ls -la
是否继续？(y/n): y
执行成功:
total 48
drwxr-xr-x 2 user user 4096 Jan  4 10:00 .
drwxr-xr-x 3 user user 4096 Jan  4 09:00 ..
drwxr-xr-x 2 user user 4096 Jan  4 10:00 myproject
...

CLI-AI> exit
再见！
```

## Safety Features

CLI-AI includes several safety features:

1. **Confirmation Required**: All commands require user confirmation before execution
2. **Dangerous Command Warning**: Commands that could cause data loss trigger extra warnings
3. **Command History**: All executed commands are logged to `command_history.txt`
4. **Cancel Option**: You can always cancel by typing 'n' when asked for confirmation

## Special Commands

- `help` or `帮助`: Show help and common command examples
- `history` or `历史`: View recent command history
- `exit` or `quit` or `退出`: Exit CLI-AI

## Advanced Usage

### Running Examples
See `examples.py` for programmatic usage:
```bash
python3 examples.py
```

### Customizing Commands
Edit `command_mappings.py` to add your own natural language to command mappings.

### Configuration
Edit `config.py` to customize:
- History file location
- Maximum history entries
- Dangerous command patterns

## Troubleshooting

### "Command not recognized"
If CLI-AI doesn't understand your input:
1. Type `help` to see supported commands
2. Try rephrasing your input
3. Add custom mappings in `command_mappings.py`

### "Permission denied"
Some commands require sudo privileges. Make sure you have the necessary permissions.

### Interactive commands
Commands like `sudo su`, `nano`, or `top` will run interactively. Your terminal will switch to that program until you exit it.

## Tips

1. Be specific with file/folder names when using commands with parameters
2. Use quotes for file names with spaces (though it's better to avoid spaces)
3. Check command history with `history` to see what you've executed
4. Always read the command that CLI-AI will execute before confirming

## Next Steps

- Explore more commands with `help`
- Read the full documentation in `README.md`
- Try the examples in `examples.py`
- Customize command mappings for your workflow
