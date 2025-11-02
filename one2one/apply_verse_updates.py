#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用verse_updates.json到各个JSON文件
"""

import json
import os

# 读取更新数据
with open('verse_updates.json', 'r', encoding='utf-8') as f:
    verse_updates = json.load(f)

data_dir = 'data/answers'
updated_count = 0
created_count = 0

print("=" * 60)
print("开始应用经文更新...")
print("=" * 60)

for filename, update_data in verse_updates.items():
    filepath = os.path.join(data_dir, filename)
    section_num = filename.split('_S')[1].replace('.json', '')
    
    # 读取现有JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️  第{section_num}节: 无法读取JSON - {e}")
        continue
    
    # 检查是否需要创建新的answers结构
    if '__create_new__' in update_data:
        # 创建新的answers
        new_answers = {}
        for key, value in update_data.items():
            if key != '__create_new__':
                new_answers[key] = value
        data['answers'] = new_answers
        created_count += 1
        print(f"✅ 第{section_num}节: 创建新answers ({len(new_answers)}个经文)")
    else:
        # 更新现有answers
        if 'answers' not in data:
            data['answers'] = {}
        
        verse_count = 0
        for q_id, verse_info in update_data.items():
            if q_id in data['answers']:
                data['answers'][q_id]['text'] = verse_info['text']
                data['answers'][q_id]['version'] = verse_info['version']
                data['answers'][q_id]['has_data'] = True
                verse_count += 1
        
        if verse_count > 0:
            print(f"✅ 第{section_num}节: 更新了 {verse_count} 个经文")
            updated_count += 1
        else:
            print(f"⚠️  第{section_num}节: 没有找到匹配的key")
            if data['answers']:
                print(f"   现有keys: {list(data['answers'].keys())[:3]}...")
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"✅ 完成！")
print(f"   更新: {updated_count} 个文件")
print(f"   创建: {created_count} 个文件")
print(f"{'='*60}")
