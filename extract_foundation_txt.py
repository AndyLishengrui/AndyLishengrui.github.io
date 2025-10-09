#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从建立根基.txt提取课程数据
"""

import json
import re
import chardet

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def read_file_with_encoding(file_path):
    """尝试多种编码读取文件"""
    encodings = ['utf-8', 'gbk', 'gb18030', 'gb2312', 'big5', 'utf-16', 'iso-8859-1']
    
    # 先检测编码
    detected = detect_encoding(file_path)
    if detected:
        encodings.insert(0, detected)
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
                # 检查是否有有效的中文内容
                if '课' in content or '第' in content:
                    print(f"成功使用编码: {encoding}")
                    return content
        except Exception as e:
            continue
    
    return None

def extract_courses(content):
    """从文本中提取课程结构"""
    courses = []
    course_titles = {}
    
    # 分割成行
    lines = content.split('\n')
    
    # 第一遍：从目录提取课程标题
    in_toc = False
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if line_stripped == '目录':
            in_toc = True
            continue
        if in_toc:
            # 匹配目录格式：1. 罪与得救 ··· 1
            toc_match = re.match(r'^(\d+)\.\s*(.+?)\s*[·\.\s]+\s*\d+$', line_stripped)
            if toc_match:
                course_num = int(toc_match.group(1))
                course_title = toc_match.group(2).strip()
                course_titles[course_num] = course_title
            elif line_stripped.startswith('前言') or line_stripped.startswith('序言'):
                in_toc = False
                break
    
    print(f"从目录中提取到 {len(course_titles)} 个课程标题:")
    for num, title in sorted(course_titles.items()):
        print(f"  {num}. {title}")
    
    # 第二遍：提取详细内容
    current_course = None
    current_section = None
    current_question = None
    in_personal_app = False
    collecting_content = False
    content_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # 检测课程开始（纯标题行，后面跟引用经文）
        if line_stripped in course_titles.values() and i + 1 < len(lines):
            # 保存上一个课程
            if current_course and current_section:
                if current_question:
                    current_section['questions'].append(current_question)
                    current_question = None
                current_course['sections'].append(current_section)
                current_section = None
            if current_course:
                courses.append(current_course)
            
            # 找到对应的课程编号
            course_num = None
            for num, title in course_titles.items():
                if title == line_stripped:
                    course_num = num
                    break
            
            current_course = {
                'id': course_num,
                'number': str(course_num),
                'title': line_stripped,
                'sections': [],
                'intro': []
            }
            
            # 收集引用经文作为介绍
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('第') and '一 节' not in lines[i]:
                if lines[i].strip():
                    current_course['intro'].append(lines[i].strip())
                i += 1
            continue
        
        # 检测节标题（格式：罪与得救 1第 一 节）
        section_match = re.search(r'第\s*([一二三四五])\s*节', line)
        if section_match and current_course:
            # 保存上一个节
            if current_section:
                if current_question:
                    current_section['questions'].append(current_question)
                    current_question = None
                current_course['sections'].append(current_section)
            
            section_num_chinese = section_match.group(1)
            section_num_map = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5}
            section_num = section_num_map.get(section_num_chinese, len(current_course['sections']) + 1)
            
            # 节标题在下一行或同一行
            section_title = ''
            remaining = line[section_match.end():].strip()
            if remaining and not remaining.startswith('_'):
                section_title = remaining
            elif i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line[0].isdigit() and not next_line.startswith('_'):
                    section_title = next_line
                    i += 1
            
            current_section = {
                'id': section_num,
                'number': section_num_chinese,
                'title': section_title,
                'questions': [],
                'content': []
            }
            current_question = None
            in_personal_app = False
            i += 1
            continue
        
        # 检测问题编号（行首数字+点）
        question_match = re.match(r'^(\d+)\.\s*(.+)$', line_stripped)
        if question_match and current_section and not in_personal_app:
            # 保存上一个问题
            if current_question:
                current_section['questions'].append(current_question)
            
            question_num = int(question_match.group(1))
            question_text = question_match.group(2).strip()
            
            current_question = {
                'id': question_num,
                'question': question_text,
                'blanks': [],
                'references': [],
                'answer_lines': 0
            }
            i += 1
            continue
        
        # 检测经文引用（创 1:10 格式）
        if current_question and not in_personal_app:
            # 匹配中文书名+章:节
            ref_match = re.match(r'^([一-龥\w]+)\s+(\d+):(\d+(?:[-,]\d+)*)(.*)$', line_stripped)
            if ref_match:
                book = ref_match.group(1)
                chapter = ref_match.group(2)
                verse = ref_match.group(3)
                rest = ref_match.group(4).strip()
                
                current_question['references'].append({
                    'book': book,
                    'chapter': chapter,
                    'verse': verse,
                    'full_text': line_stripped
                })
                i += 1
                continue
        
        # 检测填空行（下划线）
        if current_question and '_' * 10 in line:
            # 计算下划线数量
            blank_count = max(1, line.count('_') // 30)  # 每30个下划线算一行
            current_question['answer_lines'] += blank_count
            i += 1
            continue
        
        # 检测个人应用部分
        if '个人应用' in line_stripped:
            in_personal_app = True
            if current_section:
                # 收集个人应用的问题
                app_question = line_stripped.replace('个人应用：', '').replace('个人应用', '').strip()
                i += 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('第'):
                    app_question += ' ' + lines[i].strip()
                    if '_' * 10 in lines[i]:
                        break
                    i += 1
                current_section['personal_application'] = app_question
            continue
        
        # 收集节的内容文本
        if current_section and not current_question and line_stripped and not line_stripped.startswith('第'):
            current_section['content'].append(line_stripped)
        
        i += 1
    
    # 保存最后一个课程和节
    if current_course:
        if current_section:
            if current_question:
                current_section['questions'].append(current_question)
            current_course['sections'].append(current_section)
        courses.append(current_course)
    
    return courses

def main():
    input_file = '建立根基.txt'
    output_file = 'data/foundation_course.json'
    
    print(f"读取文件: {input_file}")
    content = read_file_with_encoding(input_file)
    
    if not content:
        print("无法读取文件，尝试所有编码都失败")
        return
    
    print(f"文件内容长度: {len(content)} 字符")
    print(f"前100个字符: {content[:100]}")
    
    # 提取课程
    print("\n开始提取课程...")
    courses = extract_courses(content)
    
    print(f"\n提取到 {len(courses)} 个课程")
    for course in courses:
        print(f"  第{course['number']}课: {course['title']} ({len(course['sections'])} 节)")
    
    # 保存为JSON
    data = {
        'title': '建立根基课程',
        'description': '12课系统圣经学习课程',
        'courses': courses
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    print(f"总共: {len(courses)} 个课程")

if __name__ == '__main__':
    main()
