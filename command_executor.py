"""
Command Executor for CLI-AI
Safely executes Linux commands with proper error handling
"""

import subprocess
import os
import re
from datetime import datetime
import config


class CommandExecutor:
    """Execute Linux commands safely with logging and error handling"""
    
    def __init__(self):
        self.history = []
        self.history_file = config.HISTORY_FILE
        self.enable_history = config.ENABLE_HISTORY
        
    def is_dangerous_command(self, command):
        """
        Check if a command is potentially dangerous
        
        Args:
            command (str): Command to check
            
        Returns:
            bool: True if command is dangerous
        """
        for pattern in config.DANGEROUS_PATTERNS:
            if re.search(pattern, command):
                return True
        return False
    
    def execute(self, command, interactive=False):
        """
        Execute a Linux command
        
        Args:
            command (str): Command to execute
            interactive (bool): Whether to run in interactive mode
            
        Returns:
            dict: Dictionary with 'success', 'output', 'error', 'return_code'
        """
        result = {
            'success': False,
            'output': '',
            'error': '',
            'return_code': -1,
            'command': command
        }
        
        try:
            # Log command to history
            self._log_command(command)
            
            if interactive:
                # For interactive commands, use os.system
                # This maintains the interactive nature (e.g., for sudo su, nano, etc.)
                return_code = os.system(command)
                result['return_code'] = return_code
                result['success'] = (return_code == 0)
                result['output'] = f"Interactive command executed (return code: {return_code})"
            else:
                # For non-interactive commands, use subprocess
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(timeout=config.COMMAND_TIMEOUT)
                
                result['return_code'] = process.returncode
                result['output'] = stdout
                result['error'] = stderr
                result['success'] = (process.returncode == 0)
            
            # Add to history
            self.history.append(result)
            
        except subprocess.TimeoutExpired:
            result['error'] = f"Command execution timeout ({config.COMMAND_TIMEOUT} seconds)"
        except Exception as e:
            result['error'] = f"Execution error: {str(e)}"
        
        return result
    
    def is_interactive_command(self, command):
        """
        Check if a command requires interactive mode
        
        Args:
            command (str): Command to check
            
        Returns:
            bool: True if command needs interactive mode
        """
        interactive_commands = [
            'sudo su',
            'su ',
            'nano ',
            'vi ',
            'vim ',
            'top',
            'htop',
            'less ',
            'more ',
            'man ',
            'ssh ',
            'mysql',
            'python',
            'python3',
            'node',
            'redis-cli',
            'mongo',
        ]
        
        for ic in interactive_commands:
            if command.startswith(ic) or f' {ic}' in command:
                return True
        return False
    
    def _log_command(self, command):
        """Log command to history file"""
        if not self.enable_history:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {command}\n"
            
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            # Keep history file size manageable
            self._trim_history_file()
        except Exception as e:
            # Don't fail if logging fails
            pass
    
    def _trim_history_file(self):
        """Keep history file to a reasonable size"""
        try:
            if not os.path.exists(self.history_file):
                return
            
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) > config.MAX_HISTORY_ENTRIES:
                # Keep only the last MAX_HISTORY_ENTRIES
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines[-config.MAX_HISTORY_ENTRIES:])
        except Exception:
            pass
    
    def get_history(self, limit=10):
        """
        Get recent command history
        
        Args:
            limit (int): Number of recent commands to return
            
        Returns:
            list: List of recent commands
        """
        return self.history[-limit:]
    
    def get_history_from_file(self, limit=10):
        """
        Get command history from file
        
        Args:
            limit (int): Number of recent commands to return
            
        Returns:
            list: List of recent commands from file
        """
        try:
            if not os.path.exists(self.history_file):
                return []
            
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            return lines[-limit:] if lines else []
        except Exception:
            return []
