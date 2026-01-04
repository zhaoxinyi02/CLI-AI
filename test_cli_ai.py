#!/usr/bin/env python3
"""
Test suite for CLI-AI
Run this to verify the installation and functionality
"""

import sys
import os
from nlp_parser import NLPParser
from command_executor import CommandExecutor
import config


def test_configuration():
    """Test configuration parameters"""
    print("=" * 70)
    print("Test 1: Configuration")
    print("=" * 70)
    
    assert hasattr(config, 'HISTORY_FILE'), "HISTORY_FILE not in config"
    assert hasattr(config, 'COMMAND_TIMEOUT'), "COMMAND_TIMEOUT not in config"
    assert hasattr(config, 'FUZZY_MATCH_THRESHOLD'), "FUZZY_MATCH_THRESHOLD not in config"
    assert hasattr(config, 'DANGEROUS_PATTERNS'), "DANGEROUS_PATTERNS not in config"
    
    print("✓ All required configuration parameters present")
    print(f"  - History file: {config.HISTORY_FILE}")
    print(f"  - Command timeout: {config.COMMAND_TIMEOUT}s")
    print(f"  - Fuzzy match threshold: {config.FUZZY_MATCH_THRESHOLD}")
    print(f"  - Dangerous patterns: {len(config.DANGEROUS_PATTERNS)} patterns")


def test_nlp_parser():
    """Test NLP parser with various inputs"""
    print("\n" + "=" * 70)
    print("Test 2: NLP Parser")
    print("=" * 70)
    
    parser = NLPParser()
    
    test_cases = [
        # Basic commands
        ("查看当前目录", "pwd"),
        ("show current directory", "pwd"),
        ("列出文件", "ls -la"),
        ("list files", "ls -la"),
        
        # Commands with parameters
        ("创建文件夹 test", "mkdir test"),
        ("create folder mydir", "mkdir mydir"),
        ("删除文件 test.txt", "rm test.txt"),
        
        # System commands
        ("查看磁盘空间", "df -h"),
        ("memory usage", "free -h"),
    ]
    
    passed = 0
    failed = 0
    
    for user_input, expected in test_cases:
        result = parser.parse(user_input)
        if result == expected:
            print(f"✓ '{user_input}' → {result}")
            passed += 1
        else:
            print(f"✗ '{user_input}' → Expected: {expected}, Got: {result}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    assert failed == 0, f"{failed} test(s) failed"


def test_command_executor():
    """Test command executor"""
    print("\n" + "=" * 70)
    print("Test 3: Command Executor")
    print("=" * 70)
    
    executor = CommandExecutor()
    
    # Test safe command execution
    result = executor.execute("echo 'CLI-AI Test'", interactive=False)
    assert result['success'], "Echo command should succeed"
    assert "CLI-AI Test" in result['output'], "Echo output should contain test string"
    print("✓ Safe command execution works")
    
    # Test dangerous command detection
    dangerous_commands = [
        "rm -rf /",
        "rm -rf *",
        "dd if=/dev/zero of=/dev/sda"
    ]
    
    for cmd in dangerous_commands:
        assert executor.is_dangerous_command(cmd), f"{cmd} should be detected as dangerous"
    print(f"✓ Dangerous command detection works ({len(dangerous_commands)} patterns)")
    
    # Test interactive command detection
    interactive_commands = [
        ("sudo su", True),
        ("nano test.txt", True),
        ("pwd", False),
        ("ls", False)
    ]
    
    for cmd, expected in interactive_commands:
        result = executor.is_interactive_command(cmd)
        assert result == expected, f"{cmd} interactive detection failed"
    print(f"✓ Interactive command detection works")


def test_integration():
    """Test end-to-end integration"""
    print("\n" + "=" * 70)
    print("Test 4: Integration Test")
    print("=" * 70)
    
    parser = NLPParser()
    executor = CommandExecutor()
    
    # Full workflow test
    user_input = "查看当前目录"
    command = parser.parse(user_input)
    
    assert command is not None, "Parser should return a command"
    print(f"✓ Parsed '{user_input}' to '{command}'")
    
    # Check if it's safe
    is_dangerous = executor.is_dangerous_command(command)
    print(f"✓ Safety check: {'DANGEROUS' if is_dangerous else 'SAFE'}")
    
    # Execute it
    result = executor.execute(command, interactive=False)
    assert result['success'], "Command execution should succeed"
    assert len(result['output']) > 0, "Command should produce output"
    print(f"✓ Executed successfully, output: {result['output'].strip()}")


def test_bilingual_support():
    """Test bilingual (Chinese/English) support"""
    print("\n" + "=" * 70)
    print("Test 5: Bilingual Support")
    print("=" * 70)
    
    parser = NLPParser()
    
    # Test that Chinese and English produce same commands
    pairs = [
        ("查看当前目录", "show current directory"),
        ("列出文件", "list files"),
        ("查看磁盘空间", "disk space"),
    ]
    
    for chinese, english in pairs:
        cmd_cn = parser.parse(chinese)
        cmd_en = parser.parse(english)
        assert cmd_cn == cmd_en, f"'{chinese}' and '{english}' should map to same command"
        print(f"✓ '{chinese}' ≡ '{english}' → {cmd_cn}")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "CLI-AI Comprehensive Test Suite" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    try:
        test_configuration()
        test_nlp_parser()
        test_command_executor()
        test_integration()
        test_bilingual_support()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nCLI-AI is working correctly. You can now run:")
        print("  python3 cli_ai.py")
        print("\nor:")
        print("  ./cli_ai.py")
        print()
        
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
