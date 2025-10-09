#!/usr/bin/env python3
"""
重命名文件脚本：将全局节号改为课内节号
例如：one2one_C2_S15.html → one2one_C2_S1.html
"""

import os
import re
import shutil

# 课程结构定义
COURSE_STRUCTURE = {
    1: {'start': 1, 'sections': 14},   # 第1课：第1-14节
    2: {'start': 15, 'sections': 8},   # 第2课：第15-22节 → 第1-8节
    3: {'start': 23, 'sections': 9},   # 第3课：第23-31节 → 第1-9节
    4: {'start': 32, 'sections': 10},  # 第4课：第32-41节 → 第1-10节
    5: {'start': 42, 'sections': 11},  # 第5课：第42-52节 → 第1-11节
    6: {'start': 53, 'sections': 8},   # 第6课：第53-60节 → 第1-8节
    7: {'start': 61, 'sections': 2},   # 第7课：第61-62节 → 第1-2节
}

def calculate_local_section(course_num, global_section):
    """计算课内节号"""
    course_info = COURSE_STRUCTURE[course_num]
    local_section = global_section - course_info['start'] + 1
    return local_section

def get_rename_mapping():
    """生成重命名映射"""
    mapping = {}
    
    for course_num in range(1, 8):
        course_info = COURSE_STRUCTURE[course_num]
        start = course_info['start']
        sections = course_info['sections']
        
        for i in range(sections):
            global_section = start + i
            local_section = i + 1
            
            old_html = f'one2one_C{course_num}_S{global_section}.html'
            new_html = f'one2one_C{course_num}_S{local_section}.html'
            
            old_json = f'one2one_C{course_num}_S{global_section}.json'
            new_json = f'one2one_C{course_num}_S{local_section}.json'
            
            mapping[old_html] = new_html
            mapping[old_json] = new_json
    
    return mapping

def rename_files(mapping):
    """重命名文件"""
    print("=" * 60)
    print("重命名HTML和JSON文件")
    print("=" * 60)
    
    # 重命名HTML文件
    html_count = 0
    for old_name, new_name in mapping.items():
        if old_name.endswith('.html'):
            if os.path.exists(old_name):
                # 先重命名为临时文件名，避免冲突
                temp_name = old_name + '.tmp'
                shutil.move(old_name, temp_name)
                mapping[old_name] = {'temp': temp_name, 'new': new_name}
                html_count += 1
                print(f"✓ 准备重命名: {old_name} → {new_name}")
    
    # 重命名JSON文件
    json_count = 0
    for old_name, new_name in mapping.items():
        if old_name.endswith('.json'):
            old_path = os.path.join('data', 'answers', old_name)
            new_path = os.path.join('data', 'answers', new_name)
            if os.path.exists(old_path):
                temp_path = old_path + '.tmp'
                shutil.move(old_path, temp_path)
                mapping[old_name] = {'temp': temp_path, 'new': new_path}
                json_count += 1
                print(f"✓ 准备重命名: {old_path} → {new_path}")
    
    # 执行最终重命名
    for old_name, value in mapping.items():
        if isinstance(value, dict):
            temp_name = value['temp']
            new_name = value['new']
            shutil.move(temp_name, new_name)
    
    print(f"\n✅ HTML文件: {html_count} 个")
    print(f"✅ JSON文件: {json_count} 个")
    return mapping

def update_file_content(file_path, old_name, new_name):
    """更新文件内容中的引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有引用
        if old_name in content:
            content = content.replace(old_name, new_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ 更新文件失败 {file_path}: {e}")
        return False

def update_all_references(mapping):
    """更新所有文件中的引用"""
    print("\n" + "=" * 60)
    print("更新文件引用")
    print("=" * 60)
    
    # 获取所有需要更新的HTML文件
    html_files = ['index.html']
    for course_num in range(1, 8):
        course_info = COURSE_STRUCTURE[course_num]
        sections = course_info['sections']
        for local_section in range(1, sections + 1):
            html_file = f'one2one_C{course_num}_S{local_section}.html'
            if os.path.exists(html_file):
                html_files.append(html_file)
    
    # 更新每个HTML文件
    update_count = 0
    for html_file in html_files:
        file_updated = False
        for old_name, new_name in mapping.items():
            if old_name.endswith('.html'):
                if update_file_content(html_file, old_name, new_name):
                    file_updated = True
        
        if file_updated:
            update_count += 1
            print(f"✓ 更新: {html_file}")
    
    print(f"\n✅ 共更新 {update_count} 个文件")

def main():
    # 切换到courses目录
    os.chdir('courses')
    if not os.path.exists('one2one_C1_S1.html'):
        print("❌ 找不到课程文件")
        return
    
    # 生成重命名映射
    mapping = get_rename_mapping()
    
    # 重命名文件
    rename_files(mapping)
    
    # 更新所有引用
    final_mapping = {}
    for old_name, value in mapping.items():
        if isinstance(value, dict):
            new_name = os.path.basename(value['new'])
            final_mapping[old_name] = new_name
        else:
            final_mapping[old_name] = value
    
    update_all_references(final_mapping)
    
    print("\n" + "=" * 60)
    print("✅ 重命名完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
