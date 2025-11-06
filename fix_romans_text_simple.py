#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

def fix_inappropriate_spaces(text):
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    for _ in range(5):
        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    return text

def mark_inline_scriptures(text):
    lines = text.split('\n')
    processed_lines = []
    scripture_pattern = r'\(([^)]*?)(\d+):(\d+[-\d,:]*)\)'
    
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\([^)]+\d+:\d+[-\d,:]*\)$', stripped):
            processed_lines.append(line)
            continue
        
        if re.search(scripture_pattern, line):
            def replace_inline(match):
                return f'{{{{inline-scripture}}}}{match.group(0)}{{{{/inline-scripture}}}}'
            line = re.sub(scripture_pattern, replace_inline, line)
        
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

input_file = 'BooksofRoman/romans_content.txt'
output_file = 'BooksofRoman/romans_content_fixed.txt'

print(f"Reading: {input_file}")
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

original_length = len(content)
print(f"Original length: {original_length}")

print("\nStep 1: Remove inappropriate spaces...")
content = fix_inappropriate_spaces(content)
after_space = len(content)
print(f"  Removed {original_length - after_space} spaces")

print("\nStep 2: Mark inline scriptures...")
content = mark_inline_scriptures(content)
inline_count = content.count('{{inline-scripture}}')
print(f"  Marked {inline_count} inline scriptures")

print(f"\nSaving to: {output_file}")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed length: {len(content)}")
print("\nDone! Check the fixed file and then:")
print(f"  cp {input_file} {input_file}.backup")
print(f"  mv {output_file} {input_file}")
print("  python3 generate_romans_website_v2.py")
