#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件中JavaScript的提示文字
"""

import os
import re
from pathlib import Path

def update_js_messages(html_file):
    """更新HTML文件中JavaScript的提示消息"""
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换JavaScript中的消息
    new_content = content.replace(
        "showToast('暂无标准答案')",
        "showToast('暂无答案数据')"
    )
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent
    
    # 只处理第1-3课
    html_files = []
    for i in range(1, 4):
        html_files.extend(
            foundation_dir.glob(f'foundation_L{i}_S*.html')
        )
    
    html_files.sort()
    
    print("开始更新第1-3课JavaScript提示消息...")
    print(f"找到 {len(html_files)} 个HTML文件需要处理\n")
    
    updated_count = 0
    for html_file in html_files:
        print(f"处理: {html_file.name}")
        if update_js_messages(html_file):
            print(f"  ✅ 已更新JS消息")
            updated_count += 1
        else:
            print(f"  ➡️  无需更新")
        print()
    
    print(f"\n完成！共更新了 {updated_count} 个HTML文件")

if __name__ == '__main__':
    main()