"""
Configuration file for CLI-AI terminal assistant
"""

# Version
VERSION = "2.3.0"

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

# Command execution timeout in seconds
COMMAND_TIMEOUT = 30

# Fuzzy matching threshold for NLP parser (0.0 to 1.0)
# Lower values are more lenient, higher values require closer matches
FUZZY_MATCH_THRESHOLD = 0.5

# AI-based command parsing (v2.2)
# Set to True to use AI for command parsing instead of rule-based matching
# Requires AI_PROVIDER configuration in .env file
USE_AI_PARSING = True

# Auto-continuation mode (v2.2)
# When enabled, AI will suggest next commands after successful execution
AUTO_CONTINUE_MODE = False

# Error analysis mode (v2.2)
# When enabled, AI will analyze error messages and suggest fixes
AI_ERROR_ANALYSIS = True

# Optional: API keys for enhanced NLP (users can add their own)
# OPENAI_API_KEY = "your-api-key-here"
# ANTHROPIC_API_KEY = "your-api-key-here"
