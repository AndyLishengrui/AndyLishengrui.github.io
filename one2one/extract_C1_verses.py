#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从原始文本提取第一课所有经文，并更新JSON文件
"""

import json
import re
import os

def extract_verse_content(text, ref_pattern):
    """从文本中提取指定经文的内容"""
    # 尝试多种模式匹配
    patterns = [
        # 模式1: 直接引用格式 "经文内容\n引用（版本）"
        rf'([^"]*?)\n{ref_pattern}[（\(]([^）\)]+)[）\)]',
        # 模式2: 引用在前 "引用（版本）\n经文内容"
        rf'{ref_pattern}[（\(]([^）\)]+)[）\)]\n([^"]*?)(?=\n[a-zA-Z\u4e00-\u9fa5]|\n得救)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
        if matches:
            return matches
    
    return None

def clean_verse_text(text):
    """清理经文文本，去除多余空格和换行"""
    # 去除多余的空白字符
    text = ' '.join(text.split())
    # 去除引号
    text = text.replace('"', '').replace('"', '').replace('"', '')
    return text.strip()

def extract_course1_verses():
    """提取第一课所有经文"""
    
    # 读取原始文本
    txt_path = '/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一.txt'
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取第一课内容（从"新起点"到下一课）
    start = content.find('新起点\n得救')
    # 查找第二课的开始标记
    end = content.find('第二课', start) if '第二课' in content else content.find('课二', start)
    if end == -1:
        end = content.find('新主人\n顺服', start)  # 第一课的最后部分
        if end > 0:
            end = content.find('\n\n', end + 100)  # 找到第一课结束
    
    course1_content = content[start:end] if end > 0 else content[start:start+5000]
    
    print(f"第一课内容长度: {len(course1_content)} 字符")
    print("=" * 60)
    
    # 定义每节的经文映射
    section_verses = {
        'one2one_C1_S1': {
            'q1_约翰福音 3:16': ('约翰福音 3:16', '和合本'),
        },
        'one2one_C1_S2': {
            'q1_以赛亚书 59:1,2': ('以赛亚书 59:1,2', '新译本'),
        },
        'one2one_C1_S3': {
            'q1_马太福音 5:21,22': ('马太福音 5:21,22', '当代译本'),
            'q2_马太福音 5:27,28': ('马太福音 5:27,28', '当代译本'),
        },
        'one2one_C1_S4': {
            'q1_罗马书 3:23': ('罗马书 3:23', '标准译本'),
            'q2_罗马书 6:23': ('罗马书 6:23', '当代译本'),
        },
        'one2one_C1_S5': {
            'q1_罗马书 5:8': ('罗马书 5:8', '标准译本'),
        },
        'one2one_C1_S6': {
            'q1_希伯来书 9:26-28': ('希伯来书 9:26-28', '当代译本'),
        },
        'one2one_C1_S7': {
            'q1_哥林多后书 5:21': ('哥林多后书 5:21', '标准译本'),
            'q2_加拉太书 3:13': ('加拉太书 3:13', '标准译本'),
        },
        'one2one_C1_S8': {
            'q1_以弗所书 1:7': ('以弗所书 1:7', '标准译本'),
            'q2_以弗所书 2:13': ('以弗所书 2:13', '当代译本'),
        },
        'one2one_C1_S9': {
            # 这节可能没有填空题
        },
        'one2one_C1_S10': {
            'q1_罗马书 10:9,10': ('罗马书 10:9,10', '和修版'),
        },
        'one2one_C1_S11': {
            'q1_以弗所书 2:8,9': ('以弗所书 2:8,9', '和修版'),
        },
        'one2one_C1_S12': {
            # 祷告部分，可能没有填空题
        },
        'one2one_C1_S13': {
            'q1_哥林多后书 5:17': ('哥林多后书 5:17', '和合本'),
        },
        'one2one_C1_S14': {
            'q1_使徒行传 2:36': ('使徒行传 2:36', '和修版'),
        },
    }
    
    # 提取每节的经文
    extracted_verses = {}
    
    for section_id, verses in section_verses.items():
        section_num = int(section_id.split('_S')[1])
        print(f"\n处理第{section_num}节...")
        
        extracted_verses[section_id] = {}
        
        if not verses:
            print(f"  ⚠️ 第{section_num}节没有定义经文")
            continue
        
        for q_id, (reference, version) in verses.items():
            # 在文本中查找这段经文
            ref_clean = reference.replace(' ', '').replace(',', '[,，]').replace('-', '[-]')
            
            # 尝试提取经文
            patterns = [
                # 模式1: 经文内容在前，引用在后
                rf'([^"\n]+?)\n{ref_clean}[（\(]({version})[）\)]',
                # 模式2: 引用在前，经文内容在后  
                rf'{ref_clean}[（\(]({version})[）\)]\n([^"\n]+?)(?=\n\n|\n[得救课])',
            ]
            
            found = False
            for pattern in patterns:
                matches = re.findall(pattern, course1_content, re.DOTALL)
                if matches:
                    if len(matches[0]) == 2:
                        # 提取经文文本
                        if pattern.startswith('([^'):
                            verse_text = matches[0][0]
                        else:
                            verse_text = matches[0][1]
                        
                        verse_text = clean_verse_text(verse_text)
                        
                        if verse_text and len(verse_text) > 10:
                            extracted_verses[section_id][q_id] = {
                                'reference': reference,
                                'text': verse_text,
                                'version': version
                            }
                            print(f"  ✅ {reference}: {verse_text[:50]}...")
                            found = True
                            break
            
            if not found:
                print(f"  ❌ 未找到 {reference}")
                # 尝试手动搜索
                simple_ref = reference.split()[0]
                if simple_ref in course1_content:
                    idx = course1_content.find(simple_ref)
                    context = course1_content[max(0, idx-50):idx+200]
                    print(f"     上下文: ...{context}...")
    
    return extracted_verses

def update_json_files(extracted_verses):
    """更新JSON文件"""
    data_dir = '/Users/andyshengruilee/Documents/website/web2Lord/one2one/data/answers'
    updated_count = 0
    
    for section_id, verses in extracted_verses.items():
        json_path = os.path.join(data_dir, f'{section_id}.json')
        
        if not os.path.exists(json_path):
            print(f"⚠️ JSON文件不存在: {json_path}")
            continue
        
        # 读取现有JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # 更新answers
        if 'answers' not in json_data:
            json_data['answers'] = {}
        
        updated = False
        for q_id, verse_info in verses.items():
            if q_id in json_data['answers']:
                # 更新经文内容
                json_data['answers'][q_id]['text'] = verse_info['text']
                json_data['answers'][q_id]['version'] = verse_info['version']
                json_data['answers'][q_id]['has_data'] = True
                updated = True
        
        if updated:
            # 保存更新后的JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            section_num = int(section_id.split('_S')[1])
            verse_count = len(verses)
            print(f"✅ 已更新第{section_num}节 ({verse_count}个经文)")
            updated_count += 1
    
    return updated_count

def main():
    print("=" * 60)
    print("开始提取第一课经文...")
    print("=" * 60)
    
    # 提取经文
    extracted_verses = extract_course1_verses()
    
    print("\n" + "=" * 60)
    print("开始更新JSON文件...")
    print("=" * 60)
    
    # 更新JSON文件
    updated_count = update_json_files(extracted_verses)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！更新了 {updated_count} 个JSON文件")
    print("=" * 60)

if __name__ == '__main__':
    main()
