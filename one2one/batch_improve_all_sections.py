#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量改进所有一对一课程章节
参考第一课第一节的成功模式，为所有62个章节：
1. 修复JSON数据（提取正确的经文内容）
2. 添加和合本作为默认答案
3. 更新HTML页面（统一样式、功能）
"""

import json
import re
import os
from pathlib import Path

# 课程结构（从一对一.txt提取）
COURSE_STRUCTURE = {
    1: {"title": "新起点 得救", "sections": 14},
    2: {"title": "新主人 主权", "sections": 11},
    3: {"title": "新方向 悔改", "sections": 12},
    4: {"title": "新生命 洗礼", "sections": 9},
    5: {"title": "新操练 灵修", "sections": 9},
    6: {"title": "新关系 教会", "sections": 5},
    7: {"title": "新使命 带门徒", "sections": 2}
}

def parse_txt_file():
    """
    解析一对一.txt文件，提取所有章节的内容和经文
    """
    with open('一对一.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    
    # 匹配章节标记的模式（如"得救 1"）
    course_names = {
        "得救": 1,
        "主权": 2,
        "悔改": 3,
        "洗礼": 4,
        "灵修": 5,
        "教会": 6,
        "带门徒": 7
    }
    
    # 分割成课程块
    for course_name, course_num in course_names.items():
        pattern = rf'{course_name} (\d+)'
        matches = list(re.finditer(pattern, content))
        
        for i, match in enumerate(matches):
            section_num = int(match.group(1))
            start = match.end()
            
            # 找到下一个章节的开始位置
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                # 找下一个课程的开始
                next_course_found = False
                for next_name in list(course_names.keys())[list(course_names.keys()).index(course_name)+1:]:
                    next_pattern = rf'{next_name} \d+'
                    next_match = re.search(next_pattern, content[start:])
                    if next_match:
                        end = start + next_match.start()
                        next_course_found = True
                        break
                if not next_course_found:
                    end = len(content)
            
            section_text = content[start:end].strip()
            
            # 提取经文引用
            verse_pattern = r'([\u4e00-\u9fa5]+书?\s+\d+:\d+(?:[,-]\d+)?)\s*（([^）]+)）'
            verses = []
            for verse_match in re.finditer(verse_pattern, section_text):
                ref = verse_match.group(1).strip()
                version = verse_match.group(2).strip()
                
                # 提取经文文本（假设在引用之前）
                verse_start = verse_match.start()
                # 往前找到经文开始（通常是数字开始）
                text_start = verse_start
                for j in range(verse_start - 1, max(0, verse_start - 500), -1):
                    if section_text[j] in '\n\r' and j + 1 < verse_start:
                        # 找到换行后的数字或引号
                        remaining = section_text[j+1:verse_start].strip()
                        if remaining and (remaining[0].isdigit() or remaining[0] in ['"', "'"]):
                            text_start = j + 1
                            break
                
                verse_text = section_text[text_start:verse_start].strip()
                # 清理文本（移除编号）
                verse_text = re.sub(r'^\d+[\s\."\']+', '', verse_text)
                verse_text = verse_text.strip('"\'""')
                
                verses.append({
                    'reference': ref,
                    'version': version,
                    'text': verse_text
                })
            
            # 提取问题文本（在第一个经文之前的内容）
            if verses:
                first_verse_pos = section_text.find(verses[0]['text'])
                if first_verse_pos > 0:
                    question_text = section_text[:first_verse_pos].strip()
                else:
                    question_text = section_text[:200].strip()
            else:
                question_text = section_text[:200].strip()
            
            # 清理问题文本
            question_text = re.sub(r'\n+', ' ', question_text)
            question_text = re.sub(r'\s+', ' ', question_text)
            
            key = f"C{course_num}_S{section_num}"
            sections[key] = {
                'course_num': course_num,
                'course_title': COURSE_STRUCTURE[course_num]['title'],
                'section_num': section_num,
                'question_text': question_text,
                'verses': verses,
                'full_text': section_text
            }
    
    return sections

def get_section_title(full_text):
    """从章节文本中提取标题"""
    lines = full_text.split('\n')
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) < 50:
            # 可能是标题
            if '：' in line or '?' in line or '？' in line:
                return line
    return "待定"

def create_json_data(section_info):
    """创建JSON答案数据"""
    json_data = {
        "course_num": section_info['course_num'],
        "course_title": section_info['course_title'],
        "section_num": section_info['section_num'],
        "section_title": get_section_title(section_info['full_text']),
        "answers": {}
    }
    
    for idx, verse in enumerate(section_info['verses'], 1):
        key = f"q{idx}_{verse['reference']}"
        json_data['answers'][key] = {
            "reference": verse['reference'],
            "text": verse['text'],  # 原始版本作为默认
            "version": verse['version'],
            "text_alt": "",  # 待添加和合本或其他版本
            "version_alt": "",
            "has_data": True if verse['text'] else False
        }
    
    return json_data

def save_json_file(json_data, course_num, section_num):
    """保存JSON文件"""
    filename = f"data/answers/one2one_C{course_num}_S{section_num}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    return filename

def update_all_sections():
    """更新所有章节的JSON数据"""
    print("📖 开始解析一对一.txt...")
    sections = parse_txt_file()
    
    print(f"✅ 找到 {len(sections)} 个章节\n")
    
    updated_count = 0
    for key in sorted(sections.keys()):
        section_info = sections[key]
        course_num = section_info['course_num']
        section_num = section_info['section_num']
        
        try:
            # 创建JSON数据
            json_data = create_json_data(section_info)
            
            # 保存JSON文件
            filename = save_json_file(json_data, course_num, section_num)
            
            print(f"✅ {key}: {section_info['course_title']} - 第{section_num}节")
            print(f"   标题: {json_data['section_title']}")
            print(f"   经文数: {len(section_info['verses'])}")
            print(f"   文件: {filename}\n")
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ {key}: 处理失败 - {e}\n")
    
    print(f"\n{'='*60}")
    print(f"🎉 完成！成功更新 {updated_count}/{len(sections)} 个章节")
    print(f"{'='*60}")
    
    return sections

if __name__ == '__main__':
    # 确保目录存在
    Path('data/answers').mkdir(parents=True, exist_ok=True)
    
    # 更新所有章节
    sections = update_all_sections()
    
    print("\n💡 提示：")
    print("1. JSON文件已更新，但经文内容需要人工校对")
    print("2. 建议使用Bible API获取和合本经文")
    print("3. HTML页面将在下一步统一更新")
