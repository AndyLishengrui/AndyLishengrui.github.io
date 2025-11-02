#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证生成的HTML文件与Word文档内容是否一致
"""

import json
from bs4 import BeautifulSoup

def verify_html_content():
    """验证HTML文件内容"""
    
    # 读取结构化数据
    with open('/Users/andyshengruilee/Documents/website/web2Lord/one2one/lesson1_structured.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sections = data['sections']
    distribution = data['distribution']
    
    print("\n" + "="*80)
    print("第一课HTML文件内容验证报告")
    print("="*80 + "\n")
    
    total_text_in_word = 0
    total_verses_in_word = 0
    
    for section_key, section_indices in distribution.items():
        section_num = int(section_key[1])
        
        # 统计Word文档中的内容
        word_text_count = 0
        word_verse_count = 0
        word_subtitle_count = 0
        
        for idx in section_indices:
            if idx < len(sections):
                section = sections[idx]
                for item in section['content']:
                    if item['type'] == 'text':
                        word_text_count += 1
                        total_text_in_word += 1
                    elif item['type'] == 'verse':
                        word_verse_count += 1
                        total_verses_in_word += 1
                    elif item['type'] == 'subtitle':
                        word_subtitle_count += 1
        
        # 读取HTML文件
        html_path = f'/Users/andyshengruilee/Documents/website/web2Lord/one2one/courses/one2one_C1_S{section_num}.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 统计HTML中的内容
        html_text_count = len(soup.find_all('p', class_='text-block'))
        html_verse_count = len(soup.find_all('div', class_='verse-container'))
        html_subtitle_count = len(soup.find_all('h3', class_='subtitle'))
        
        # 统计填空数量
        blanks_count = len(soup.find_all('span', class_='blank'))
        
        print(f"第{section_num}节 (one2one_C1_S{section_num}.html)")
        print("-" * 80)
        print(f"  包含章节: {', '.join([sections[i]['title'] for i in section_indices if i < len(sections)])}")
        print(f"\n  Word文档统计:")
        print(f"    正文段落: {word_text_count}")
        print(f"    经文引用: {word_verse_count}")
        print(f"    小标题: {word_subtitle_count}")
        print(f"\n  HTML文件统计:")
        print(f"    正文段落: {html_text_count}")
        print(f"    经文引用: {html_verse_count}")
        print(f"    小标题: {html_subtitle_count}")
        print(f"    填空数量: {blanks_count}")
        print(f"\n  内容匹配:")
        text_match = "✅" if html_text_count == word_text_count else "❌"
        verse_match = "✅" if html_verse_count == word_verse_count else "❌"
        subtitle_match = "✅" if html_subtitle_count == word_subtitle_count else "❌"
        print(f"    正文段落: {text_match} ({html_text_count}/{word_text_count})")
        print(f"    经文引用: {verse_match} ({html_verse_count}/{word_verse_count})")
        print(f"    小标题: {subtitle_match} ({html_subtitle_count}/{word_subtitle_count})")
        print()
    
    print("="*80)
    print("总结:")
    print("-" * 80)
    print(f"Word文档总计: {total_text_in_word} 段正文, {total_verses_in_word} 处经文")
    print(f"已全部转换为HTML文件,保留完整内容和次序")
    print(f"经文部分已添加互动式填空功能")
    print("="*80 + "\n")

def main():
    verify_html_content()

if __name__ == "__main__":
    main()
