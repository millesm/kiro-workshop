#!/usr/bin/env python3
"""
Setup verification script for Shopping Assistant Chatbot Service.

This script checks that all required files exist and have valid syntax.
"""

import os
import sys
import py_compile
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {filepath}")
        return True
    else:
        print(f"✗ {filepath} - MISSING")
        return False

def check_python_syntax(filepath):
    """Check Python file syntax."""
    try:
        py_compile.compile(filepath, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ {filepath} - SYNTAX ERROR: {e}")
        return False

def main():
    """Main verification function."""
    print("=" * 60)
    print("Shopping Assistant Chatbot - Setup Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check Python files
    print("Checking Python files...")
    python_files = [
        'chatbot/__init__.py',
        'chatbot/config.py',
        'chatbot/tools.py',
        'chatbot/agent.py',
        'chatbot/server.py',
        'chatbot/__main__.py'
    ]
    
    for filepath in python_files:
        if check_file_exists(filepath):
            if not check_python_syntax(filepath):
                all_checks_passed = False
        else:
            all_checks_passed = False
    
    print()
    
    # Check configuration files
    print("Checking configuration files...")
    config_files = [
        'chatbot/requirements.txt',
        '.env.example',
        'chatbot/README.md'
    ]
    
    for filepath in config_files:
        if not check_file_exists(filepath):
            all_checks_passed = False
    
    print()
    
    # Check deployment files
    print("Checking deployment files...")
    deployment_files = [
        'Dockerfile',
        'docker-compose.yml',
        'DEPLOYMENT.md'
    ]
    
    for filepath in deployment_files:
        if not check_file_exists(filepath):
            all_checks_passed = False
    
    print()
    
    # Check frontend files
    print("Checking frontend files...")
    frontend_files = [
        'client/src/components/Chatbot.js',
        'client/src/components/Chatbot.css'
    ]
    
    for filepath in frontend_files:
        if not check_file_exists(filepath):
            all_checks_passed = False
    
    print()
    print("=" * 60)
    
    if all_checks_passed:
        print("✓ All checks passed!")
        print()
        print("Next steps:")
        print("1. Copy .env.example to .env and add your AWS credentials")
        print("2. Install dependencies: pip install -r chatbot/requirements.txt")
        print("3. Initialize database: npm run init-db")
        print("4. Start backend: npm run server")
        print("5. Start chatbot: python -m chatbot")
        print("6. Start frontend: npm run client")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
