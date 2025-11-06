#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取罗马书八部曲的内容
"""

from docx import Document
import json
import re

def extract_romans_content(docx_path):
    """提取docx文件内容"""
    doc = Document(docx_path)
    
    # 存储所有段落文本
    all_text = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            all_text.append(text)
    
    return all_text

def save_to_file(content, output_path):
    """保存内容到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in content:
            f.write(line + '\n')

if __name__ == '__main__':
    docx_path = 'BooksofRoman/《罗马书》-天书八部合并版.docx'
    output_path = 'BooksofRoman/romans_content.txt'
    
    print("正在提取罗马书内容...")
    content = extract_romans_content(docx_path)
    
    print(f"提取了 {len(content)} 行内容")
    
    # 保存到文本文件
    save_to_file(content, output_path)
    print(f"内容已保存到: {output_path}")
    
    # 显示前50行预览
    print("\n前50行预览:")
    print("=" * 80)
    for i, line in enumerate(content[:50], 1):
        print(f"{i:3d}. {line}")
