#!/usr/bin/env python3
"""
更新index.html中的课程链接
"""

import re

def update_index_html():
    """更新index.html中的链接"""
    
    # 定义需要替换的映射（第2-7课）
    replacements = [
        ('courses/one2one_C2_S15.html', 'courses/one2one_C2_S1.html'),
        ('courses/one2one_C3_S23.html', 'courses/one2one_C3_S1.html'),
        ('courses/one2one_C4_S32.html', 'courses/one2one_C4_S1.html'),
        ('courses/one2one_C5_S42.html', 'courses/one2one_C5_S1.html'),
        ('courses/one2one_C6_S53.html', 'courses/one2one_C6_S1.html'),
        ('courses/one2one_C7_S61.html', 'courses/one2one_C7_S1.html'),
    ]
    
    print("=" * 60)
    print("更新index.html中的课程链接")
    print("=" * 60)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_link, new_link in replacements:
        if old_link in content:
            content = content.replace(old_link, new_link)
            print(f"✓ {old_link} → {new_link}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ index.html更新完成")

if __name__ == '__main__':
    update_index_html()
