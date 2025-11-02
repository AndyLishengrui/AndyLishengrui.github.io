#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从一对一.txt中提取每节的说明文字（讲解内容）
"""

import json
import re
import os

def extract_section_content(text, section_num):
    """提取指定节的说明文字"""
    # 查找"得救 X"标记
    pattern = rf'得救 {section_num}\n(.*?)(?=得救 \d+|\n[a-zA-Z]|\Z)'
    match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        return None
    
    content = match.group(1).strip()
    
    # 移除经文部分（包括引用和版本）
    # 经文通常在段落末尾，格式为：经文内容\n引用（版本）
    lines = content.split('\n')
    clean_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        # 跳过经文引用行（包含书卷名称和版本）
        if re.search(r'[a-zA-Z\u4e00-\u9fa5]+\s+\d+[:：]\d+.*?[（\(][^）\)]+[）\)]', line):
            skip_next = True
            continue
        
        # 跳过纯数字开头的经文内容
        if skip_next and re.match(r'^\d+\s+', line):
            continue
        
        skip_next = False
        
        # 跳过空行
        if line.strip():
            clean_lines.append(line)
    
    # 合并文本，保留段落结构
    result = '\n'.join(clean_lines).strip()
    
    # 进一步清理：移除可能的经文片段
    result = re.sub(r'\d+\s+"[^"]+?".*?[（\(][^）\)]+[）\)]', '', result)
    
    return result if result else None

def main():
    # 读取原始文本
    txt_path = '/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一.txt'
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取第一课的内容
    start = content.find('新起点\n得救')
    end = content.find('第二课', start) if '第二课' in content else content.find('课二', start)
    if end == -1:
        end = content.find('新主人\n顺服', start)
        if end > 0:
            end = content.find('\n\n', end + 100)
    
    course1_content = content[start:end] if end > 0 else content[start:start+6000]
    
    print("=" * 60)
    print("提取第一课每节的说明文字...")
    print("=" * 60)
    
    # 提取每节的说明文字
    section_descriptions = {}
    for section_num in range(1, 15):
        desc = extract_section_content(course1_content, section_num)
        if desc:
            section_descriptions[section_num] = desc
            print(f"\n第{section_num}节:")
            print(f"  长度: {len(desc)} 字符")
            print(f"  预览: {desc[:80]}...")
        else:
            print(f"\n第{section_num}节: 未找到说明文字")
    
    # 更新JSON文件
    data_dir = '/Users/andyshengruilee/Documents/website/web2Lord/one2one/data/answers'
    updated_count = 0
    
    print("\n" + "=" * 60)
    print("更新JSON文件...")
    print("=" * 60)
    
    for section_num, description in section_descriptions.items():
        json_filename = f'one2one_C1_S{section_num}.json'
        json_path = os.path.join(data_dir, json_filename)
        
        if not os.path.exists(json_path):
            print(f"⚠️  第{section_num}节: JSON文件不存在")
            continue
        
        # 读取JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 添加description字段
        data['description'] = description
        
        # 保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 第{section_num}节: 已添加说明文字 ({len(description)}字符)")
        updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成！更新了 {updated_count} 个JSON文件")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
