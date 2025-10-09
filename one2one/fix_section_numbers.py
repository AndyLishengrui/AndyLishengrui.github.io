#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复脚本：
1. 将小节编号改为每课独立编号（第2课第1节，而不是第15节）
2. 读取one2one_C1_S1.html的CSS样式，添加到所有生成的HTML中
"""

import re
from pathlib import Path

# 课程结构
COURSE_STRUCTURE = {
    1: {"sections": 14, "start": 1},
    2: {"sections": 8, "start": 15},
    3: {"sections": 9, "start": 23},
    4: {"sections": 10, "start": 32},
    5: {"sections": 11, "start": 42},
    6: {"sections": 8, "start": 53},
    7: {"sections": 2, "start": 61}
}

def extract_css_from_template():
    """从根基课程提取CSS样式"""
    template_file = '/Users/andyshengruilee/Documents/website/integrated-site/foundation/foundation_L1_S1.html'
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取<style>标签内容
        match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if match:
            return match.group(1)
        return None
    except FileNotFoundError:
        print(f"❌ 模板文件 {template_file} 不存在")
        return None

def fix_html_file(file_path, course_num, local_section_num, css_content):
    """修复单个HTML文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换: <link rel="stylesheet" href="css/one2one_style.css">
    # 为: <style>...</style>
    if 'css/one2one_style.css' in content:
        content = content.replace(
            '<link rel="stylesheet" href="css/one2one_style.css">',
            f'<style>{css_content}</style>'
        )
    
    # 替换标题中的节号
    # 例如：第1课 第1节 而不是 第1课 第1节
    content = re.sub(
        r'<title>第\d+课 第(\d+)节',
        f'<title>第{course_num}课 第{local_section_num}节',
        content
    )
    
    # 替换面包屑中的节号
    content = re.sub(
        r'&gt; 第(\d+)节',
        f'&gt; 第{local_section_num}节',
        content
    )
    
    # 替换section-label中的节号
    content = re.sub(
        r'<span class="section-label">第 \d+ 节</span>',
        f'<span class="section-label">第 {local_section_num} 节</span>',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("=" * 60)
    print("修复小节编号和CSS样式")
    print("=" * 60)
    
    # 提取CSS
    print("\n提取CSS样式...")
    css_content = extract_css_from_template()
    if not css_content:
        print("❌ 无法提取CSS样式")
        return
    print("✓ CSS样式提取成功")
    
    # 修复所有HTML文件
    print("\n修复HTML文件...")
    fixed_count = 0
    
    for course_num in range(1, 8):
        course_info = COURSE_STRUCTURE[course_num]
        start_section = course_info['start']
        num_sections = course_info['sections']
        
        for i in range(num_sections):
            global_section_num = start_section + i
            local_section_num = i + 1  # 每课从1开始
            
            file_name = f"one2one_C{course_num}_S{global_section_num}.html"
            file_path = Path(__file__).parent / file_name
            
            if file_path.exists():
                fix_html_file(file_path, course_num, local_section_num, css_content)
                print(f"✓ {file_name} (第{course_num}课 第{local_section_num}节)")
                fixed_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共修复 {fixed_count} 个文件")
    print("=" * 60)

if __name__ == '__main__':
    main()
