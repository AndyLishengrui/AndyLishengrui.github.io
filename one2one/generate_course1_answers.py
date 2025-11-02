#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据course_1_structure.json生成答案数据文件
"""

import json
import os

def create_answer_json(section, course_num):
    """为每个章节创建答案JSON文件"""
    section_num = section['section_number']
    
    answer_data = {
        "course_num": course_num,
        "course_title": "新起点 得救",
        "section_num": section_num,
        "section_title": section['title'],
        "answers": {}
    }
    
    # 处理多个经文
    if 'verses' in section:
        for idx, verse in enumerate(section['verses'], 1):
            answer_key = f"q1_{verse['reference']}"
            answer_data['answers'][answer_key] = {
                "reference": verse['reference'],
                "text": verse['content'],
                "version": verse['version'],
                "has_data": True
            }
    # 处理单个经文
    elif 'content' in section:
        answer_key = f"q1_{section['verse_reference']}"
        answer_data['answers'][answer_key] = {
            "reference": section['verse_reference'],
            "text": section['content'],
            "version": section['verse_version'],
            "has_data": True
        }
    
    # 处理最后的经文（如果有）
    if 'verse' in section:
        verse = section['verse']
        answer_key = f"q2_{verse['reference']}"
        answer_data['answers'][answer_key] = {
            "reference": verse['reference'],
            "text": verse['content'],
            "version": verse['version'],
            "has_data": True
        }
    
    return answer_data

def main():
    # 读取结构文件
    with open('course_1_structure.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    sections = course_data['sections']
    
    # 创建data/answers目录
    output_dir = 'data/answers'
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每个章节生成答案JSON
    for section in sections:
        section_num = section['section_number']
        answer_data = create_answer_json(section, 1)
        
        filename = f'{output_dir}/one2one_C1_S{section_num}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(answer_data, f, ensure_ascii=False, indent=2)
        
        print(f'✅ 已生成答案文件: {filename}')
        print(f'   包含 {len(answer_data["answers"])} 个答案')
    
    print(f'\n🎉 完成！共生成 {len(sections)} 个答案数据文件')

if __name__ == '__main__':
    main()
