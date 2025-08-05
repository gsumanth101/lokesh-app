#!/usr/bin/env python3

import os
import ast

print("Checking all Python files for null byte corruption...")

corrupted_files = []

for filename in os.listdir('.'):
    if filename.endswith('.py'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print(f"✓ {filename}")
        except ValueError as e:
            if "null bytes" in str(e):
                corrupted_files.append(filename)
                print(f"✗ {filename} - contains null bytes")
        except Exception as e:
            print(f"? {filename} - other error: {e}")

if corrupted_files:
    print(f"\nFound {len(corrupted_files)} corrupted files:")
    for f in corrupted_files:
        print(f"  - {f}")
else:
    print("\n✓ All Python files are clean!")
