#!/usr/bin/env python3
"""
更新课程HTML文件中的JSON引用路径
"""

import os
import re

# 课程结构定义
COURSE_STRUCTURE = {
    1: {'start': 1, 'sections': 14},
    2: {'start': 15, 'sections': 8},
    3: {'start': 23, 'sections': 9},
    4: {'start': 32, 'sections': 10},
    5: {'start': 42, 'sections': 11},
    6: {'start': 53, 'sections': 8},
    7: {'start': 61, 'sections': 2},
}

def update_json_references():
    """更新课程HTML文件中的JSON引用"""
    
    print("=" * 60)
    print("更新课程HTML中的JSON引用")
    print("=" * 60)
    
    courses_dir = 'courses'
    updated = 0
    
    for course_num in range(1, 8):
        course_info = COURSE_STRUCTURE[course_num]
        start = course_info['start']
        sections = course_info['sections']
        
        for i in range(sections):
            local_section = i + 1
            global_section = start + i
            
            html_file = os.path.join(courses_dir, f'one2one_C{course_num}_S{local_section}.html')
            
            if not os.path.exists(html_file):
                continue
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换JSON文件引用
            old_json_ref = f"data/answers/one2one_C{course_num}_S{global_section}.json"
            new_json_ref = f"../data/answers/one2one_C{course_num}_S{local_section}.json"
            
            if old_json_ref in content:
                content = content.replace(old_json_ref, new_json_ref)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ {os.path.basename(html_file)}: {old_json_ref} → {new_json_ref}")
                updated += 1
            elif f"data/answers/one2one_C{course_num}_S{local_section}.json" in content:
                # 需要添加 ../
                old_ref = f"data/answers/one2one_C{course_num}_S{local_section}.json"
                content = content.replace(old_ref, new_json_ref)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ {os.path.basename(html_file)}: 添加相对路径 ../")
                updated += 1
    
    print(f"\n✅ 共更新 {updated} 个文件")

if __name__ == '__main__':
    update_json_references()
