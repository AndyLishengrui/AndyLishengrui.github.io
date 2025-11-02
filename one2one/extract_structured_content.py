#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Word文档中提取并整理一对一门徒训练的内容
"""

from docx import Document
import json
import re

def extract_structured_content(docx_path):
    """从Word文档中提取结构化内容"""
    
    doc = Document(docx_path)
    
    content = {
        'preface': {
            'title': '前言（慕容）',
            'paragraphs': []
        },
        'discipleship_steps': {
            'title': '开始作门徒（五步骤）',
            'intro_verse': '',
            'intro_text': '',
            'steps': []
        },
        'lesson1': {
            'title': '新起点 得救',
            'sections': []
        }
    }
    
    current_section = None
    current_data = []
    step_count = 0
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        if not text:
            continue
        
        # 识别前言部分
        if text == '前言（慕容）':
            current_section = 'preface'
            continue
        
        # 识别作门徒部分
        if text == '开始作门徒（五步骤）':
            current_section = 'discipleship_steps'
            continue
        
        # 识别第一课
        if text == ')新起点 得救' or text == '新起点 得救':
            current_section = 'lesson1'
            content['lesson1']['title'] = '新起点 得救'
            continue
        
        # 识别第二课开始(停止提取第一课)
        if '新主人 主权' in text:
            break
        
        # 根据当前章节保存内容
        if current_section == 'preface':
            content['preface']['paragraphs'].append(text)
        
        elif current_section == 'discipleship_steps':
            # 马可福音经文
            if '马可福音' in text or '来跟从我' in text:
                if '来跟从我' in text:
                    content['discipleship_steps']['intro_verse'] = text
            # 引言文字
            elif '当你开始跟随耶稣' in text:
                content['discipleship_steps']['intro_text'] = text
            # 步骤标题(以数字开头)
            elif re.match(r'^\d+\.', text):
                step_count += 1
                content['discipleship_steps']['steps'].append({
                    'number': step_count,
                    'title': text,
                    'verses': []
                })
            # 经文内容
            elif para.style.name == '经文' or '（' in text and '）' in text:
                if content['discipleship_steps']['steps']:
                    content['discipleship_steps']['steps'][-1]['verses'].append(text)
        
        elif current_section == 'lesson1':
            # 收集第一课的所有内容
            content['lesson1']['sections'].append({
                'style': para.style.name,
                'text': text
            })
    
    return content

def main():
    docx_path = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一20251011Andy排版.docx"
    
    print("=" * 80)
    print("开始提取Word文档结构化内容...")
    print("=" * 80)
    
    content = extract_structured_content(docx_path)
    
    # 保存为JSON文件
    output_file = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/structured_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"\n提取完成！结果已保存到: {output_file}")
    
    # 打印摘要
    print("\n" + "=" * 80)
    print("内容摘要:")
    print("=" * 80)
    print(f"\n前言: {len(content['preface']['paragraphs'])} 段")
    print(f"作门徒步骤: {len(content['discipleship_steps']['steps'])} 个步骤")
    print(f"第一课内容: {len(content['lesson1']['sections'])} 个段落")
    
    print("\n前言前3段预览:")
    for p in content['preface']['paragraphs'][:3]:
        print(f"  {p[:80]}...")
    
    print("\n作门徒步骤:")
    for step in content['discipleship_steps']['steps']:
        print(f"  {step['number']}. {step['title'][:60]}...")

if __name__ == "__main__":
    main()
