#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为建立根基课程生成标准答案数据文件
"""

import json
import os

# 书卷映射（仅新约）
BOOK_MAPPING = {
    '太': 'matthew',
    '可': 'mark',
    '路': 'luke',
    '约': 'john',
    '徒': 'acts',
    '罗': 'romans',
    '林前': '1corinthians',
    '林后': '2corinthians',
    '加': 'galatians',
    '弗': 'ephesians',
    '腓': 'philippians',
    '西': 'colossians',
    '帖前': '1thessalonians',
    '帖后': '2thessalonians',
    '提前': '1timothy',
    '提后': '2timothy',
    '多': 'titus',
    '门': 'philemon'
}

# 加载所有书卷数据
books_data = {}

def load_all_books():
    """加载所有可用的书卷数据"""
    for book_name, book_id in BOOK_MAPPING.items():
        try:
            with open(f'data/{book_id}.json', 'r', encoding='utf-8') as f:
                book_data = json.load(f)
                books_data[book_name] = {}
                for verse in book_data['verses']:
                    key = f"{verse['chapter']}:{verse['verse']}"
                    books_data[book_name][key] = verse['zh']
                print(f"✓ 已加载 {book_name} ({book_id})")
        except FileNotFoundError:
            print(f"✗ 未找到 {book_name} 数据")

def parse_reference(ref):
    """解析经文引用，支持范围和多节"""
    import re
    
    # 例如: "创 1:10", "创 1:1-3", "赛 59:1,2", "罗 3:9-20,23"
    match = re.match(r'^([\u4e00-\u9fa5]+)\s*(\d+):(.*)', ref)
    if not match:
        return []
    
    book_name = match.group(1)
    chapter = int(match.group(2))
    verse_part = match.group(3)
    
    verses = []
    
    # 处理逗号分隔的多个部分
    parts = [p.strip() for p in verse_part.split(',')]
    
    for part in parts:
        if '-' in part:
            # 范围: "9-20"
            start, end = part.split('-')
            start = int(start.strip())
            end = int(end.strip())
            for v in range(start, end + 1):
                verses.append({'book': book_name, 'chapter': chapter, 'verse': v})
        else:
            # 单节: "23"
            verses.append({'book': book_name, 'chapter': chapter, 'verse': int(part)})
    
    return verses

def get_verse_text(book_name, chapter, verse):
    """获取经文文本"""
    if book_name not in books_data:
        return None
    
    key = f"{chapter}:{verse}"
    return books_data[book_name].get(key)

def get_reference_text(ref):
    """获取引用的完整经文文本"""
    verses = parse_reference(ref)
    if not verses:
        return None
    
    texts = []
    for v in verses:
        text = get_verse_text(v['book'], v['chapter'], v['verse'])
        if text:
            texts.append(text)
    
    return ' '.join(texts) if texts else None

def generate_answer_files():
    """为每一节生成答案数据文件"""
    
    # 读取课程数据
    with open('data/foundation_course.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    # 创建答案数据目录
    os.makedirs('data/answers', exist_ok=True)
    
    # 合并重复的课程
    unique_lessons = {}
    for lesson in course_data['lessons']:
        lesson_id = lesson['id']
        if lesson_id not in unique_lessons:
            unique_lessons[lesson_id] = lesson
        else:
            unique_lessons[lesson_id]['sections'].extend(lesson['sections'])
    
    lessons = sorted(unique_lessons.values(), key=lambda x: x['id'])
    
    print(f"\n开始生成答案数据文件...")
    print(f"共 {len(lessons)} 课\n")
    
    total_files = 0
    
    for lesson in lessons:
        lesson_id = lesson['id']
        lesson_title = lesson['title']
        
        print(f"第{lesson_id}课: {lesson_title}")
        
        for section_idx, section in enumerate(lesson['sections']):
            section_num = section_idx + 1
            answer_data = {
                'lesson_id': lesson_id,
                'lesson_title': lesson_title,
                'section_num': section_num,
                'section_title': section['title'],
                'answers': {}
            }
            
            # 为每个问题生成答案
            for q in section['questions']:
                question_id = q['id']
                references = q.get('references', [])
                
                if references:
                    for ref in references:
                        verse_text = get_reference_text(ref)
                        key = f"q{question_id}_{ref}"
                        
                        if verse_text:
                            answer_data['answers'][key] = {
                                'reference': ref,
                                'text': verse_text,
                                'has_data': True
                            }
                        else:
                            answer_data['answers'][key] = {
                                'reference': ref,
                                'text': '',
                                'has_data': False,
                                'note': '暂无此书卷数据（仅支持新约）'
                            }
            
            # 保存答案文件
            filename = f"data/answers/foundation_L{lesson_id}_S{section_num}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(answer_data, f, ensure_ascii=False, indent=2)
            
            total_files += 1
            answer_count = sum(1 for a in answer_data['answers'].values() if a.get('has_data'))
            print(f"  ✓ 第{section_num}节: {answer_count} 个标准答案")
    
    print(f"\n✓ 共生成 {total_files} 个答案数据文件")

if __name__ == "__main__":
    print("正在加载圣经数据...")
    load_all_books()
    print("\n" + "="*50)
    generate_answer_files()
    print("\n✓ 所有答案数据文件生成完成！")
