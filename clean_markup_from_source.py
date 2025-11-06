#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理源文档中的废弃标记
永久移除 {{inline-scripture}}, {{reference}} 等已废弃的标记
只保留:
- {{scripture}}...{{/scripture}} (整段经文块)
- {{scripture-ref}}...{{/scripture-ref}} (经文引用)
"""

import os
import re

def clean_deprecated_markup(content):
    """
    清理废弃的标记
    """
    original_content = content
    
    # 1. 移除 {{inline-scripture}} 标签
    content = re.sub(r'\{\{inline-scripture\}\}', '', content)
    content = re.sub(r'\{\{/inline-scripture\}\}', '', content)
    
    # 2. 移除 {{reference}} 标签(保留内容)
    content = re.sub(r'\{\{reference\}\}', '', content)
    content = re.sub(r'\{\{/reference\}\}', '', content)
    
    # 3. 清理可能的多余空格
    # 但保持段落结构不变
    
    changes = len(re.findall(r'\{\{(?:inline-scripture|/inline-scripture|reference|/reference)\}\}', original_content))
    
    return content, changes


def clean_chapter_file(input_file, output_file):
    """清理单个章节文件"""
    print(f"处理: {os.path.basename(input_file)}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned_content, changes = clean_deprecated_markup(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"  ✓ 移除了 {changes} 个废弃标记")
    print(f"  ✓ 已保存: {os.path.basename(output_file)}")
    
    return changes


def main():
    """主函数"""
    print("=" * 60)
    print("清理源文档中的废弃标记")
    print("=" * 60)
    print()
    
    input_dir = "BooksofRoman/chapters_final"
    
    total_changes = 0
    
    # 处理16个章节
    for i in range(1, 17):
        chapter_num = f"{i:02d}"
        chapter_file = f"{input_dir}/chapter_{chapter_num}.txt"
        
        if os.path.exists(chapter_file):
            changes = clean_chapter_file(chapter_file, chapter_file)
            total_changes += changes
        else:
            print(f"⚠ 警告: 找不到文件 {chapter_file}")
    
    print()
    print("=" * 60)
    print("✓ 清理完成!")
    print(f"✓ 总共移除了 {total_changes} 个废弃标记")
    print("✓ 保留的标记:")
    print("  - {{scripture}}...{{/scripture}} (整段经文)")
    print("  - {{scripture-ref}}...{{/scripture-ref}} (经文引用)")
    print("=" * 60)


if __name__ == "__main__":
    main()
