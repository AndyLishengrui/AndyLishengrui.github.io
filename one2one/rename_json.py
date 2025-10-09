#!/usr/bin/env python3
"""
重命名JSON文件脚本
"""

import os
import shutil

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

def rename_json_files():
    """重命名JSON文件"""
    answers_dir = 'data/answers'
    
    print("=" * 60)
    print("重命名JSON文件")
    print("=" * 60)
    
    renamed = []
    
    for course_num in range(2, 8):  # 第1课不需要重命名
        course_info = COURSE_STRUCTURE[course_num]
        start = course_info['start']
        sections = course_info['sections']
        
        for i in range(sections):
            global_section = start + i
            local_section = i + 1
            
            old_name = f'one2one_C{course_num}_S{global_section}.json'
            new_name = f'one2one_C{course_num}_S{local_section}.json'
            
            old_path = os.path.join(answers_dir, old_name)
            new_path = os.path.join(answers_dir, new_name)
            
            if os.path.exists(old_path):
                shutil.move(old_path, new_path)
                renamed.append((old_name, new_name))
                print(f"✓ {old_name} → {new_name}")
    
    print(f"\n✅ 共重命名 {len(renamed)} 个JSON文件")

if __name__ == '__main__':
    rename_json_files()
