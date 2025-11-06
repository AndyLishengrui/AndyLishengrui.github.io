#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析罗马书八部曲的结构
"""

def analyze_structure(file_path):
    """分析文档结构"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找主要部分
    parts = []
    chapters = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # 查找部(第一部、第二部等)
        if '第' in line and '部' in line and len(line) < 20:
            parts.append((i, line))
        
        # 查找章节标记
        if line.startswith(('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ')) and len(line) < 30:
            chapters.append((i, line))
    
    print("=" * 80)
    print("找到的'部':")
    print("=" * 80)
    for line_num, text in parts[:20]:
        print(f"行 {line_num:4d}: {text}")
    
    print("\n" + "=" * 80)
    print("找到的章节标题(前30个):")
    print("=" * 80)
    for line_num, text in chapters[:30]:
        print(f"行 {line_num:4d}: {text}")
    
    print(f"\n总共找到 {len(parts)} 个'部'")
    print(f"总共找到 {len(chapters)} 个章节标题")
    print(f"总行数: {len(lines)}")

if __name__ == '__main__':
    analyze_structure('BooksofRoman/romans_content.txt')
