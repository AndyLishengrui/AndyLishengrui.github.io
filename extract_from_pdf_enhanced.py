#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从PDF直接提取一对一课程内容，去除页码，生成JSON和HTML
"""

import PyPDF2
import re
import json
import os

def extract_pdf_content(pdf_path):
    """从PDF提取文本内容"""
    print(f"正在读取PDF: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"总页数: {total_pages}")
        
        text_content = []
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            text_content.append(text)
            
            if (page_num + 1) % 10 == 0:
                print(f"  已处理 {page_num + 1}/{total_pages} 页...")
        
        print("PDF读取完成！")
        return '\n'.join(text_content)

def remove_page_numbers(text):
    """去除页码"""
    # 常见的页码模式
    patterns = [
        r'\n\s*\d+\s*\n',  # 单独一行的数字
        r'\n\s*-\s*\d+\s*-\s*\n',  # -数字- 格式
        r'\n\s*第\s*\d+\s*页\s*\n',  # 第X页
        r'\n\s*Page\s+\d+\s*\n',  # Page X
    ]
    
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, '\n', cleaned, flags=re.IGNORECASE)
    
    return cleaned

def clean_text(text):
    """清理文本格式"""
    # 去除多余空行
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # 去除行首行尾空格
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text

def extract_course_structure(text):
    """识别课程结构"""
    # 查找课程标记（例如："第一课"、"课一"等）
    course_pattern = r'(?:第\s*[一二三四五六]?\s*课|课\s*[一二三四五六])\s*[:：]?\s*([^\n]+)'
    courses = re.finditer(course_pattern, text, re.MULTILINE)
    
    structure = []
    for match in courses:
        course_title = match.group(1).strip()
        start_pos = match.start()
        structure.append({
            'title': course_title,
            'start': start_pos,
            'match': match.group(0)
        })
    
    return structure

def extract_sections(text, course_start, course_end):
    """提取一个课程内的所有节"""
    course_text = text[course_start:course_end]
    
    # 查找节标记（例如："得救 1"、"1."、"（1）"等）
    section_patterns = [
        r'得救\s+(\d+)',
        r'(\d+)\s*[\.、]',
        r'[（\(](\d+)[）\)]',
    ]
    
    sections = []
    for pattern in section_patterns:
        matches = re.finditer(pattern, course_text)
        for match in matches:
            section_num = match.group(1)
            start_pos = match.start()
            sections.append({
                'num': int(section_num),
                'start': start_pos + course_start,
                'match': match.group(0)
            })
    
    # 去重并排序
    sections = sorted(sections, key=lambda x: x['start'])
    unique_sections = []
    seen = set()
    for s in sections:
        if s['num'] not in seen:
            unique_sections.append(s)
            seen.add(s['num'])
    
    return unique_sections

def main():
    pdf_path = 'one2one/一对一大字版.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF文件不存在: {pdf_path}")
        return
    
    print("=" * 60)
    print("开始提取一对一课程PDF...")
    print("=" * 60)
    
    # 1. 提取PDF内容
    raw_text = extract_pdf_content(pdf_path)
    
    # 2. 去除页码
    print("\n去除页码...")
    text = remove_page_numbers(raw_text)
    
    # 3. 清理文本
    print("清理文本格式...")
    text = clean_text(text)
    
    # 4. 保存清理后的文本
    output_txt = 'one2one/一对一_from_pdf_cleaned.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✅ 已保存清理后的文本: {output_txt}")
    
    # 5. 识别课程结构
    print("\n识别课程结构...")
    courses = extract_course_structure(text)
    print(f"找到 {len(courses)} 个课程:")
    for i, course in enumerate(courses):
        print(f"  {i+1}. {course['title']}")
    
    # 6. 提取每个课程的节
    print("\n提取各课程的节...")
    for i, course in enumerate(courses):
        course_start = course['start']
        course_end = courses[i+1]['start'] if i+1 < len(courses) else len(text)
        
        sections = extract_sections(text, course_start, course_end)
        course['sections'] = sections
        
        print(f"  课程 {i+1}: {len(sections)} 节")
    
    # 7. 保存结构数据
    structure_file = 'one2one/course_structure_from_pdf.json'
    with open(structure_file, 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 课程结构已保存: {structure_file}")
    
    print("\n" + "=" * 60)
    print("✅ PDF提取完成！")
    print("=" * 60)
    print(f"\n输出文件:")
    print(f"  1. {output_txt} - 清理后的完整文本")
    print(f"  2. {structure_file} - 课程结构JSON")

if __name__ == '__main__':
    main()
