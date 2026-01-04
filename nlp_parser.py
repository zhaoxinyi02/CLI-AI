"""
Natural Language Parser for CLI-AI
Converts natural language to Linux commands
"""

import re
from command_mappings import COMMAND_MAPPINGS


class NLPParser:
    """Parse natural language input and convert to Linux commands"""
    
    def __init__(self):
        self.mappings = COMMAND_MAPPINGS
    
    def parse(self, user_input):
        """
        Parse natural language input and return corresponding Linux command
        
        Args:
            user_input (str): User's natural language input
            
        Returns:
            str: Linux command or None if no match found
        """
        # Normalize input: strip whitespace and convert to lowercase
        normalized_input = user_input.strip().lower()
        
        # First, try exact match
        if normalized_input in self.mappings:
            return self.mappings[normalized_input]
        
        # Try to match commands with parameters
        command = self._parse_with_parameters(normalized_input)
        if command:
            return command
        
        # Try fuzzy matching for similar phrases
        command = self._fuzzy_match(normalized_input)
        if command:
            return command
        
        return None
    
    def _parse_with_parameters(self, user_input):
        """Parse commands that require parameters"""
        
        # Create folder/directory: "创建文件夹 test" -> "mkdir test"
        if any(phrase in user_input for phrase in ["创建文件夹", "新建文件夹", "create folder", "make directory", "mkdir"]):
            match = re.search(r'(?:创建文件夹|新建文件夹|create folder|make directory|mkdir)\s+(\S+)', user_input)
            if match:
                folder_name = match.group(1)
                return f"mkdir {folder_name}"
        
        # Delete file: "删除文件 test.txt" -> "rm test.txt"
        if any(phrase in user_input for phrase in ["删除文件", "remove file"]) and "文件夹" not in user_input and "folder" not in user_input:
            match = re.search(r'(?:删除文件|remove file)\s+(\S+)', user_input)
            if match:
                file_name = match.group(1)
                return f"rm {file_name}"
        
        # Delete folder: "删除文件夹 test" -> "rm -r test"
        if any(phrase in user_input for phrase in ["删除文件夹", "remove folder", "delete folder"]):
            match = re.search(r'(?:删除文件夹|remove folder|delete folder)\s+(\S+)', user_input)
            if match:
                folder_name = match.group(1)
                return f"rm -r {folder_name}"
        
        # Find file: "查找文件 test.txt" -> "find . -name test.txt"
        if any(phrase in user_input for phrase in ["查找文件", "find file", "search file"]):
            match = re.search(r'(?:查找文件|find file|search file)\s+(\S+)', user_input)
            if match:
                file_name = match.group(1)
                return f"find . -name {file_name}"
        
        # Show file content: "查看文件内容 test.txt" -> "cat test.txt"
        if any(phrase in user_input for phrase in ["查看文件内容", "show file", "read file", "cat"]):
            match = re.search(r'(?:查看文件内容|show file|read file|cat)\s+(\S+)', user_input)
            if match:
                file_name = match.group(1)
                return f"cat {file_name}"
        
        # Edit file: "编辑文件 test.txt" -> "nano test.txt"
        if any(phrase in user_input for phrase in ["编辑文件", "edit file"]):
            match = re.search(r'(?:编辑文件|edit file)\s+(\S+)', user_input)
            if match:
                file_name = match.group(1)
                return f"nano {file_name}"
        
        # Copy file: "复制文件 a.txt b.txt" -> "cp a.txt b.txt"
        if any(phrase in user_input for phrase in ["复制文件", "copy file"]):
            match = re.search(r'(?:复制文件|copy file)\s+(\S+)\s+(?:到|to)?\s*(\S+)', user_input)
            if match:
                source = match.group(1)
                dest = match.group(2)
                return f"cp {source} {dest}"
        
        # Move/rename file: "移动文件 a.txt b.txt" -> "mv a.txt b.txt"
        if any(phrase in user_input for phrase in ["移动文件", "move file", "重命名", "rename"]):
            match = re.search(r'(?:移动文件|move file|重命名|rename)\s+(\S+)\s+(?:到|to)?\s*(\S+)', user_input)
            if match:
                source = match.group(1)
                dest = match.group(2)
                return f"mv {source} {dest}"
        
        # Change directory: "切换到 /home" -> "cd /home", "进入 test" -> "cd test"
        if any(phrase in user_input for phrase in ["切换到", "进入", "cd ", "go to", "change to"]):
            match = re.search(r'(?:切换到|进入|cd|go to|change to)\s+(\S+)', user_input)
            if match:
                path = match.group(1)
                # Skip if it's "切换到管理员" (handled separately)
                if path not in ["管理员", "administrator", "root"]:
                    return f"cd {path}"
        
        # Install package: "安装软件 vim" -> "sudo apt install vim"
        if any(phrase in user_input for phrase in ["安装软件", "install package", "install"]):
            match = re.search(r'(?:安装软件|install package|install)\s+(\S+)', user_input)
            if match:
                package = match.group(1)
                return f"sudo apt install {package}"
        
        # Remove package: "删除软件 vim" -> "sudo apt remove vim"
        if any(phrase in user_input for phrase in ["删除软件", "remove package", "uninstall"]):
            match = re.search(r'(?:删除软件|remove package|uninstall)\s+(\S+)', user_input)
            if match:
                package = match.group(1)
                return f"sudo apt remove {package}"
        
        # Change permission: "修改权限 755 test.txt" -> "chmod 755 test.txt"
        if any(phrase in user_input for phrase in ["修改权限", "change permission", "chmod"]):
            match = re.search(r'(?:修改权限|change permission|chmod)\s+(\S+)\s+(\S+)', user_input)
            if match:
                mode = match.group(1)
                file = match.group(2)
                return f"chmod {mode} {file}"
        
        # Search in file: "搜索内容 pattern file.txt" -> "grep pattern file.txt"
        if any(phrase in user_input for phrase in ["搜索内容", "search in file", "grep"]):
            match = re.search(r'(?:搜索内容|search in file|grep)\s+(\S+)\s+(\S+)', user_input)
            if match:
                pattern = match.group(1)
                file = match.group(2)
                return f"grep {pattern} {file}"
        
        return None
    
    def _fuzzy_match(self, user_input):
        """Try fuzzy matching for similar phrases"""
        
        # Check if any mapping key is a substring or superset of input
        for phrase, command in self.mappings.items():
            # Skip template commands (containing {})
            if '{' in command:
                continue
            
            # Check if phrase is in user input or user input is in phrase
            if phrase in user_input or user_input in phrase:
                # Additional check to avoid false positives
                # Make sure it's a reasonable match (at least 70% of the phrase)
                if len(user_input) >= len(phrase) * 0.5:
                    return command
        
        return None
    
    def get_all_commands(self):
        """Return all available command mappings"""
        return self.mappings
    
    def add_custom_mapping(self, phrase, command):
        """
        Add a custom mapping for user-specific commands
        
        Args:
            phrase (str): Natural language phrase
            command (str): Corresponding Linux command
        """
        self.mappings[phrase.lower()] = command
