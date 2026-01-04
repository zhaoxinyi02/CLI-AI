"""
Configuration file for CLI-AI terminal assistant
"""

# Command history file
HISTORY_FILE = "command_history.txt"

# Enable command history logging
ENABLE_HISTORY = True

# Dangerous command patterns (will show extra warnings)
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"dd\s+if=.*of=/dev/",
    r"mkfs\.",
    r":\(\)\{.*\};:",  # Fork bomb
    r"chmod\s+-R\s+777\s+/",
    r">.*\/dev\/sda",
]

# Maximum command history entries to keep
MAX_HISTORY_ENTRIES = 1000

# Optional: API keys for enhanced NLP (users can add their own)
# OPENAI_API_KEY = "your-api-key-here"
# ANTHROPIC_API_KEY = "your-api-key-here"
