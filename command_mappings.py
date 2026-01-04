"""
Command mappings for natural language to Linux commands
Supports both Chinese and English phrases
"""

# Mapping of natural language phrases to Linux commands
COMMAND_MAPPINGS = {
    # System administration
    "切换到管理员": "sudo su",
    "switch to administrator": "sudo su",
    "become root": "sudo su",
    "切换到root": "sudo su",
    "登录root": "sudo su",
    "sudo": "sudo su",
    
    # Directory operations
    "查看当前目录": "pwd",
    "当前目录": "pwd",
    "show current directory": "pwd",
    "current directory": "pwd",
    "where am i": "pwd",
    
    "列出文件": "ls -la",
    "显示文件": "ls -la",
    "查看文件": "ls -la",
    "list files": "ls -la",
    "show files": "ls -la",
    "ls": "ls -la",
    
    "返回上一级": "cd ..",
    "上一级目录": "cd ..",
    "go back": "cd ..",
    "parent directory": "cd ..",
    
    # System information
    "查看磁盘空间": "df -h",
    "磁盘空间": "df -h",
    "disk space": "df -h",
    "show disk": "df -h",
    "df": "df -h",
    
    "查看内存使用": "free -h",
    "内存使用": "free -h",
    "memory usage": "free -h",
    "show memory": "free -h",
    "free": "free -h",
    
    "查看系统信息": "uname -a",
    "系统信息": "uname -a",
    "system information": "uname -a",
    "system info": "uname -a",
    
    "查看CPU信息": "lscpu",
    "cpu信息": "lscpu",
    "cpu info": "lscpu",
    
    # Process management
    "查看进程": "ps aux",
    "显示进程": "ps aux",
    "show processes": "ps aux",
    "list processes": "ps aux",
    "ps": "ps aux",
    
    "查看进程树": "pstree",
    "process tree": "pstree",
    
    "查看资源占用": "top",
    "系统监控": "top",
    "monitor system": "top",
    "top": "top",
    
    # Network operations
    "查看网络": "ip addr",
    "查看ip": "ip addr",
    "show ip": "ip addr",
    "network info": "ip addr",
    "ip address": "ip addr",
    
    "ping测试": "ping -c 4 8.8.8.8",
    "test network": "ping -c 4 8.8.8.8",
    "ping": "ping -c 4 8.8.8.8",
    
    "查看端口": "netstat -tuln",
    "show ports": "netstat -tuln",
    "list ports": "netstat -tuln",
    
    # File operations (templates - will be filled with actual parameters)
    "创建文件夹": "mkdir {folder}",
    "新建文件夹": "mkdir {folder}",
    "create folder": "mkdir {folder}",
    "make directory": "mkdir {folder}",
    
    "删除文件": "rm {file}",
    "remove file": "rm {file}",
    
    "删除文件夹": "rm -r {folder}",
    "remove folder": "rm -r {folder}",
    
    "复制文件": "cp {source} {dest}",
    "copy file": "cp {source} {dest}",
    
    "移动文件": "mv {source} {dest}",
    "move file": "mv {source} {dest}",
    "重命名": "mv {source} {dest}",
    "rename": "mv {source} {dest}",
    
    "查找文件": "find . -name {file}",
    "find file": "find . -name {file}",
    "search file": "find . -name {file}",
    
    "查看文件内容": "cat {file}",
    "显示文件": "cat {file}",
    "show file": "cat {file}",
    "read file": "cat {file}",
    
    "编辑文件": "nano {file}",
    "edit file": "nano {file}",
    
    # Permission operations
    "修改权限": "chmod {mode} {file}",
    "change permission": "chmod {mode} {file}",
    
    "修改所有者": "chown {owner} {file}",
    "change owner": "chown {owner} {file}",
    
    # Package management (Debian/Ubuntu)
    "更新软件": "sudo apt update",
    "update packages": "sudo apt update",
    "apt update": "sudo apt update",
    
    "升级软件": "sudo apt upgrade",
    "upgrade packages": "sudo apt upgrade",
    "apt upgrade": "sudo apt upgrade",
    
    "安装软件": "sudo apt install {package}",
    "install package": "sudo apt install {package}",
    
    "删除软件": "sudo apt remove {package}",
    "remove package": "sudo apt remove {package}",
    
    # Text processing
    "搜索内容": "grep {pattern} {file}",
    "search in file": "grep {pattern} {file}",
    
    # Compression
    "解压zip": "unzip {file}",
    "extract zip": "unzip {file}",
    
    "解压tar": "tar -xvf {file}",
    "extract tar": "tar -xvf {file}",
    
    "压缩文件": "tar -czvf {archive}.tar.gz {files}",
    "compress files": "tar -czvf {archive}.tar.gz {files}",
    
    # Other common commands
    "清屏": "clear",
    "clear screen": "clear",
    "clear": "clear",
    
    "查看历史": "history",
    "show history": "history",
    "command history": "history",
    
    "查看日期": "date",
    "show date": "date",
    "current time": "date",
    
    "重启": "sudo reboot",
    "reboot": "sudo reboot",
    "restart": "sudo reboot",
    
    "关机": "sudo shutdown -h now",
    "shutdown": "sudo shutdown -h now",
    "power off": "sudo shutdown -h now",
}

# Dangerous command keywords for extra warnings
DANGEROUS_KEYWORDS = [
    "rm -rf /",
    "rm -rf *",
    "dd if=",
    "mkfs",
    "format",
    "chmod -R 777 /",
    "> /dev/",
]
