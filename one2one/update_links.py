#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有链接为新的目录结构
"""

import os
import re
import glob

def update_index_html():
    """更新首页中的链接"""
    index_file = 'index.html'
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有课程页面链接：one2one_C*_S*.html -> courses/one2one_C*_S*.html
    content = re.sub(
        r'href="(one2one_C\d+_S\d+\.html)"',
        r'href="courses/\1"',
        content
    )
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 更新 {index_file}")

def update_course_html_files():
    """更新courses目录下所有HTML文件中的链接"""
    course_files = glob.glob('courses/one2one_C*_S*.html')
    
    for filename in sorted(course_files):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # 1. 更新面包屑中的首页链接：index.html -> ../index.html
        if 'href="index.html"' in content:
            content = content.replace('href="index.html"', 'href="../index.html"')
            modified = True
        
        # 2. 更新上一节/下一节链接：one2one_C*_S*.html -> one2one_C*_S*.html（同目录，无需修改）
        # 这些链接已经是相对路径，不需要修改
        
        # 3. 更新返回首页的链接
        if '<a href="index.html"' in content:
            content = content.replace('<a href="index.html"', '<a href="../index.html"')
            modified = True
        
        if modified:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {os.path.basename(filename)}")

def main():
    print("=" * 60)
    print("更新链接为新目录结构")
    print("=" * 60)
    
    # 步骤1：更新首页链接
    print("\n更新首页链接...")
    update_index_html()
    
    # 步骤2：更新课程页面链接
    print("\n更新课程页面链接...")
    update_course_html_files()
    
    print("\n" + "=" * 60)
    print("✅ 所有链接更新完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
