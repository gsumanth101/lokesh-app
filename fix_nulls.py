#!/usr/bin/env python3

# Fix null bytes and corrupted characters in app.py

with open('app.py', 'rb') as f:
    data = f.read()

print(f"Original file size: {len(data)} bytes")

# Count null bytes
null_count = data.count(b'\x00')
print(f"Found {null_count} null bytes")

# Replace corrupted characters
clean_data = data.replace(b'\x03e', b'>')  # Fix corrupted > character
clean_data = clean_data.replace(b'\x003c', b'<')  # Fix corrupted < character
clean_data = clean_data.replace(b'\x00', b'')  # Remove null bytes

print(f"Cleaned file size: {len(clean_data)} bytes")

# Write the cleaned file
with open('app_fixed.py', 'wb') as f:
    f.write(clean_data)

print("Fixed file saved as app_fixed.py")

# Test if the fixed file can be parsed
try:
    import ast
    with open('app_fixed.py', 'r', encoding='utf-8') as f:
        ast.parse(f.read())
    print("✓ Fixed file can be parsed successfully")
except Exception as e:
    print(f"✗ Error parsing fixed file: {e}")
