#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按照罗马书圣经章节重新分割文件
基于经文引用(罗马书 1:1, 2:1, 3:1 等)来正确划分16个章节
"""

import re
import os

def analyze_scripture_references(file_path):
    """分析文件中罗马书经文引用的分布"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 匹配罗马书章节引用: 罗马书 X:Y 或 罗马书X:Y
    pattern = re.compile(r'罗马书\s*(\d+)[:：]\d+')
    
    chapter_lines = {}  # {章节号: [行号列表]}
    
    for line_num, line in enumerate(lines, 1):
        matches = pattern.findall(line)
        for chapter in matches:
            chapter_num = int(chapter)
            if chapter_num not in chapter_lines:
                chapter_lines[chapter_num] = []
            chapter_lines[chapter_num].append(line_num)
    
    return chapter_lines

def find_chapter_boundaries(file_path):
    """基于经文引用密度找出章节边界"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 分析经文引用分布
    chapter_refs = analyze_scripture_references(file_path)
    
    print("📊 罗马书各章经文引用统计:")
    for ch in sorted(chapter_refs.keys()):
        print(f"  第{ch}章: {len(chapter_refs[ch])}次引用")
        if len(chapter_refs[ch]) <= 5:
            print(f"    首次出现: 行 {chapter_refs[ch][0]}")
            print(f"    末次出现: 行 {chapter_refs[ch][-1]}")
    print()
    
    # 查找章节边界的策略:
    # 1. 找到每个章节首次大量出现的位置
    # 2. 考虑主题标题的位置
    # 3. 章节应该是连续的,互不重叠
    
    boundaries = {}  # {章节号: (起始行, 结束行)}
    
    # 先找到各章节首次密集出现的大致位置
    for chapter_num in range(1, 17):
        if chapter_num in chapter_refs and chapter_refs[chapter_num]:
            first_line = chapter_refs[chapter_num][0]
            # 向前搜索200行,找到最合适的起始点(通常是主题标题)
            search_start = max(1, first_line - 200)
            
            # 查找这个范围内的主题标题
            best_start = first_line
            for line_num in range(search_start, first_line):
                line = lines[line_num - 1].strip()
                # 检查是否是主题标题(数字. 标题)
                if re.match(r'^\d+\.\s+.+$', line):
                    best_start = line_num
            
            boundaries[chapter_num] = best_start
    
    print("🔍 检测到的章节起始位置:")
    for ch in sorted(boundaries.keys()):
        print(f"  第{ch}章: 行 {boundaries[ch]}")
        # 显示该行内容
        if boundaries[ch] <= len(lines):
            preview = lines[boundaries[ch] - 1].strip()[:80]
            print(f"    预览: {preview}...")
    print()
    
    return boundaries, lines

def split_by_chapters(input_file, output_dir):
    """按章节分割文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    boundaries, lines = find_chapter_boundaries(input_file)
    total_lines = len(lines)
    
    # 手动调整边界(基于分析结果)
    # 这需要根据实际输出调整
    adjusted_boundaries = {
        1: 1,      # 从头开始
        2: 700,    # 罗马书2章相关内容开始
        3: 1100,   # 罗马书3章相关内容开始
        4: 1400,   # 罗马书4章相关内容开始
        5: 1650,   # 罗马书5章相关内容开始
        6: 1900,   # 罗马书6章相关内容开始
        7: 2100,   # 罗马书7章相关内容开始
        8: 2300,   # 罗马书8章相关内容开始
        9: 2600,   # 罗马书9章相关内容开始
        10: 2750,  # 罗马书10章相关内容开始
        11: 2850,  # 罗马书11章相关内容开始
        12: 2950,  # 罗马书12章相关内容开始
        13: 3050,  # 罗马书13章相关内容开始
        14: 3120,  # 罗马书14章相关内容开始
        15: 3180,  # 罗马书15章相关内容开始
        16: 3240,  # 罗马书16章相关内容开始
    }
    
    # 使用检测到的边界(如果有的话)
    for ch, start_line in boundaries.items():
        if ch in adjusted_boundaries:
            adjusted_boundaries[ch] = start_line
    
    # 创建章节文件
    for chapter_num in range(1, 17):
        start_line = adjusted_boundaries.get(chapter_num, 1)
        end_line = adjusted_boundaries.get(chapter_num + 1, total_lines + 1)
        
        chapter_content = ''.join(lines[start_line - 1:end_line - 1])
        
        output_file = os.path.join(output_dir, f"chapter_{chapter_num:02d}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
        
        print(f"✓ 章节 {chapter_num}: 行 {start_line}-{end_line} ({end_line - start_line} 行)")
        print(f"  保存至: {output_file}")

if __name__ == "__main__":
    input_file = "BooksofRoman/romans_content.txt"
    output_dir = "BooksofRoman/chapters_by_scripture"
    
    print("=" * 60)
    print("按照罗马书圣经章节重新分割")
    print("=" * 60)
    print()
    
    # 先分析经文引用分布
    print("📖 分析经文引用分布...")
    chapter_refs = analyze_scripture_references(input_file)
    
    print()
    print("=" * 60)
    print("开始分割...")
    print("=" * 60)
    print()
    
    split_by_chapters(input_file, output_dir)
    
    print()
    print("=" * 60)
    print("✓ 分割完成!")
    print("=" * 60)
