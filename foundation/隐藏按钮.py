#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐藏清空和保存按钮
"""

import os
import re
from pathlib import Path

def hide_buttons_in_file(html_file):
    """在HTML文件中隐藏清空和保存按钮"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并注释掉清空按钮
    clear_pattern = r'(\s*)<button class="btn btn-secondary" onclick="clearAnswers\(\)">🗑️ 清空</button>'
    content = re.sub(clear_pattern, r'\1<!-- <button class="btn btn-secondary" onclick="clearAnswers()">🗑️ 清空</button> -->', content)
    
    # 查找并注释掉保存按钮
    save_pattern = r'(\s*)<button class="btn btn-secondary" onclick="saveProgress\(\)">💾 保存</button>'
    content = re.sub(save_pattern, r'\1<!-- <button class="btn btn-secondary" onclick="saveProgress()">💾 保存</button> -->', content)
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent
    
    # 查找所有foundation HTML文件
    html_files = list(foundation_dir.glob('foundation_L*.html'))
    html_files.sort()
    
    print("开始隐藏清空和保存按钮...")
    print(f"找到 {len(html_files)} 个HTML文件需要处理\n")
    
    updated_count = 0
    for html_file in html_files:
        print(f"处理: {html_file.name}")
        if hide_buttons_in_file(html_file):
            print(f"  ✅ 已隐藏按钮")
            updated_count += 1
        print()
    
    print(f"\n完成！共更新了 {updated_count} 个HTML文件")

if __name__ == '__main__':
    main()