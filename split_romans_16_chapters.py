#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将romans_content.txt按照16个主题章节分割成独立文件
支持两种章节标题格式:
1. "数字 标题" (前12章)
2. "数字. 标题" (后续章节)
"""

import re
import os

def extract_16_chapters():
    """提取16个主要章节"""
    
    input_file = "BooksofRoman/romans_content.txt"
    output_dir = "BooksofRoman/chapters"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 定义16个主要章节的位置(基于搜索结果)
    # 格式: (行号-1, 标题)
    chapters = [
        (5, "1 序言"),  # 行6
        (17, "2 保罗与福音"),  # 行18
        (525, "3 保罗与罗马人"),  # 行526
        (600, "4 保罗与宣教"),  # 行601
        (710, "5 外邦人的罪"),  # 行711
        (815, "6 道德主义者的罪"),  # 行816
        (953, "7 犹太人的罪"),  # 行954
        (1068, "8 全人类的属灵处境"),  # 行1069
        (1138, "9 人如何称义?"),  # 行1139
        (1334, "10 称义的结果"),  # 行1335
        (1548, "11 圣洁与成圣"),  # 行1549
        (1823, "12 成圣与律法"),  # 行1824
        (2465, "13 与基督一同受苦得荣耀"),  # 行2466,格式"13."
        (2522, "14 永恒的荣耀"),  # 行2523
        (2535, "15 圣经中的末世观"),  # 行2536
        (2562, "16 基督徒的盼望"),  # 行2563
    ]
    
    # 添加文件结束标记
    chapters.append((len(lines), "END"))
    
    # 提取每个章节
    for i in range(len(chapters) - 1):
        start_line, title = chapters[i]
        end_line, _ = chapters[i + 1]
        
        # 提取章节编号
        chapter_num = i + 1
        
        # 提取内容
        content = ''.join(lines[start_line:end_line])
        
        # 保存到文件
        output_file = os.path.join(output_dir, f"chapter_{chapter_num:02d}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 章节 {chapter_num}: {title}")
        print(f"  行范围: {start_line+1}-{end_line}")
        print(f"  保存至: {output_file}")
        print(f"  行数: {end_line - start_line}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("开始分割罗马书16个章节")
    print("=" * 60)
    print()
    
    extract_16_chapters()
    
    print("=" * 60)
    print("✓ 分割完成!")
    print("=" * 60)
