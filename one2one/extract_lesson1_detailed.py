#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Word文档中提取第一课得救的完整内容
"""

from docx import Document
import json

def extract_lesson1_content(docx_path):
    """提取第一课的完整内容"""
    
    doc = Document(docx_path)
    
    lesson1 = {
        'title': '新起点 得救',
        'sections': []
    }
    
    in_lesson1 = False
    current_section = None
    section_content = []
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        if not text:
            continue
        
        # 识别第一课开始
        if '新起点 得救' in text or ')新起点 得救' in text:
            in_lesson1 = True
            lesson1['intro_verse'] = ''
            continue
        
        # 识别第二课开始(停止提取)
        if '新主人 主权' in text and in_lesson1:
            # 保存最后一个section
            if current_section and section_content:
                lesson1['sections'].append({
                    'section_name': current_section,
                    'content': section_content
                })
            break
        
        if in_lesson1:
            # 识别主要章节标题
            if para.style.name == 'Heading 2':
                # 保存上一个section
                if current_section and section_content:
                    lesson1['sections'].append({
                        'section_name': current_section,
                        'content': section_content
                    })
                current_section = text
                section_content = []
            elif para.style.name == 'Heading 3' or para.style.name == 'Heading 4':
                # 子标题
                section_content.append({
                    'type': 'subtitle',
                    'text': text,
                    'style': para.style.name
                })
            elif para.style.name == '经文':
                # 经文
                section_content.append({
                    'type': 'verse',
                    'text': text
                })
            elif para.style.name == '一对一正文' or para.style.name == 'Normal':
                # 正文
                section_content.append({
                    'type': 'text',
                    'text': text
                })
            else:
                # 其他内容
                section_content.append({
                    'type': 'other',
                    'text': text,
                    'style': para.style.name
                })
    
    return lesson1

def print_lesson1_structure(lesson1):
    """打印第一课的结构"""
    print(f"\n标题: {lesson1['title']}")
    print(f"章节数: {len(lesson1['sections'])}")
    print("\n" + "="*80)
    
    for i, section in enumerate(lesson1['sections'], 1):
        print(f"\n【章节 {i}】: {section['section_name']}")
        print("-"*80)
        
        for j, item in enumerate(section['content'][:5]):  # 只显示前5个内容项
            if item['type'] == 'subtitle':
                print(f"  [{item['type']}] {item['text'][:60]}")
            elif item['type'] == 'verse':
                print(f"  [经文] {item['text'][:60]}...")
            elif item['type'] == 'text':
                print(f"  [正文] {item['text'][:60]}...")
        
        if len(section['content']) > 5:
            print(f"  ... (还有 {len(section['content']) - 5} 项内容)")

def main():
    docx_path = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一20251011Andy排版.docx"
    
    print("=" * 80)
    print("开始提取第一课内容...")
    print("=" * 80)
    
    lesson1 = extract_lesson1_content(docx_path)
    
    # 保存为JSON
    output_file = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/lesson1_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(lesson1, f, ensure_ascii=False, indent=2)
    
    print(f"\n内容已保存到: {output_file}")
    
    # 打印结构
    print_lesson1_structure(lesson1)
    
    # 打印完整内容到文本文件
    text_output = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/lesson1_full_text.txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write(f"第一课: {lesson1['title']}\n")
        f.write("="*80 + "\n\n")
        
        for i, section in enumerate(lesson1['sections'], 1):
            f.write(f"\n【章节 {i}】{section['section_name']}\n")
            f.write("-"*80 + "\n")
            
            for item in section['content']:
                if item['type'] == 'subtitle':
                    f.write(f"\n## {item['text']}\n")
                elif item['type'] == 'verse':
                    f.write(f"\n经文: {item['text']}\n")
                elif item['type'] == 'text':
                    f.write(f"{item['text']}\n\n")
                else:
                    f.write(f"{item['text']}\n")
    
    print(f"\n完整文本已保存到: {text_output}")

if __name__ == "__main__":
    main()
