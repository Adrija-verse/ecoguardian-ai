# diagnose_imports.py
import os
from pathlib import Path

print("🔍 Searching for settings files...\n")

for root, dirs, files in os.walk('.'):
    for file in files:
        if 'settings' in file.lower() and file.endswith('.py'):
            full_path = os.path.join(root, file)
            print(f"Found: {full_path}")
            
            # Check file size
            size = os.path.getsize(full_path)
            print(f"  Size: {size} bytes")
            
            # Read first few lines
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    first_lines = [next(f) for _ in range(5)]
                    print("  First lines:")
                    for line in first_lines:
                        print(f"    {line.strip()}")
            except:
                pass
            print()

print("\n🔍 Checking for __pycache__ directories...")
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        print(f"  Found cache: {os.path.join(root, '__pycache__')}")