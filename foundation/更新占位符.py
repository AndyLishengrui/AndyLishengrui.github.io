#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件中的占位符文本
根据JSON答案数据，更新HTML中textarea的placeholder属性
"""

import json
import os
import re
from pathlib import Path

def get_answer_data(lesson_id, section_id):
    """获取指定课程节的答案数据"""
    json_file = f"data/answers/foundation_L{lesson_id}_S{section_id}.json"
    json_path = Path(__file__).parent / json_file
    
    if not json_path.exists():
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 构建答案查找字典
    answers = {}
    for key, answer in data['answers'].items():
        answers[answer['reference']] = answer['has_data']
    
    return answers

def update_html_placeholders(html_file):
    """更新HTML文件中的占位符"""
    # 从文件名提取课程和节信息
    filename = os.path.basename(html_file)
    match = re.match(r'foundation_L(\d+)_S(\d+)\.html', filename)
    if not match:
        return False
    
    lesson_id = int(match.group(1))
    section_id = int(match.group(2))
    
    # 获取答案数据
    answers = get_answer_data(lesson_id, section_id)
    if not answers:
        print(f"  ⚠️  未找到答案数据: {filename}")
        return False
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有带有data-reference的textarea
    pattern = r'(<textarea[^>]*data-reference="([^"]+)"[^>]*placeholder=")[^"]*("[^>]*>)'
    
    def replace_placeholder(match):
        prefix = match.group(1)
        reference = match.group(2)
        suffix = match.group(3)
        
        # 根据答案数据决定占位符文本
        if reference in answers and answers[reference]:
            placeholder = "请填写经文内容..."
        else:
            placeholder = "暂无标准答案"
        
        return f'{prefix}{placeholder}{suffix}'
    
    new_content = re.sub(pattern, replace_placeholder, content)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent  # foundation目录
    
    # 只处理第1-3课
    html_files = []
    for i in range(1, 4):  # 第1-3课
        html_files.extend(
            foundation_dir.glob(f'foundation_L{i}_S*.html')
        )
    
    html_files.sort()
    
    print("开始更新第1-3课HTML占位符...")
    print(f"找到 {len(html_files)} 个HTML文件需要处理\n")
    
    updated_count = 0
    for html_file in html_files:
        print(f"处理: {html_file.name}")
        if update_html_placeholders(html_file):
            print(f"  ✅ 已更新占位符")
            updated_count += 1
        else:
            print(f"  ➡️  无需更新")
        print()
    
    print(f"\n完成！共更新了 {updated_count} 个HTML文件")

if __name__ == '__main__':
    main()