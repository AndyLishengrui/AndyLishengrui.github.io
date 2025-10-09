#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从PDF提取建立根基课程完整内容
"""

import pdfplumber
import json
import re

def extract_from_pdf():
    """从PDF提取课程内容"""
    
    pdf_path = "建立根基201605.pdf"
    
    print("开始从PDF提取内容...")
    print("="*70)
    
    # 读取PDF
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF总页数: {len(pdf.pages)}")
        
        # 提取所有文本
        all_text = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append(f"\n=== 第 {i+1} 页 ===\n")
                all_text.append(text)
        
        full_text = '\n'.join(all_text)
        
        # 保存为文本文件以便分析
        with open('建立根基_from_pdf.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"✓ PDF文本已提取到: 建立根基_from_pdf.txt")
        print(f"✓ 总字符数: {len(full_text)}")
        
        # 查找12课的标题
        print("\n查找课程标题...")
        lesson_titles = [
            "罪与得救",
            "主权与顺服", 
            "悔改与洗礼",
            "圣灵与属灵恩赐",
            "渴慕与神的话语",
            "门徒与带领",
            "属灵家庭与教会生活",
            "祷告与敬拜",
            "信心与盼望",
            "富足与慷慨",
            "传福音与世界宣教",
            "复活与审判"
        ]
        
        lines = full_text.split('\n')
        for i, title in enumerate(lesson_titles, 1):
            found_lines = []
            for line_num, line in enumerate(lines):
                if title in line and '目录' not in line:
                    found_lines.append((line_num, line.strip()[:80]))
            
            if found_lines:
                print(f"第{i}课 '{title}':")
                for ln, text in found_lines[:3]:  # 只显示前3个匹配
                    print(f"  行{ln}: {text}")

if __name__ == "__main__":
    extract_from_pdf()
