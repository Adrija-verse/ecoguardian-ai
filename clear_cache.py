import os
import shutil
from pathlib import Path

# Remove all __pycache__ directories
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        print(f"Removing: {cache_path}")
        shutil.rmtree(cache_path, ignore_errors=True)

# Remove .pyc files
for pyc in Path('.').rglob('*.pyc'):
    print(f"Removing: {pyc}")
    pyc.unlink()

print("\n✅ Cache cleared! Now run: python main.py")