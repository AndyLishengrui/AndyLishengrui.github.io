#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复第一课所有缺失的JSON数据
"""

import json
import os

# 手动定义每节需要的经文
verses_updates = {
    'one2one_C1_S3.json': {
        'q1_马太福音 5:27,28': {
            'text': '27 "你们听过这样的话，'不可通奸。' 28 但我告诉你们，凡看见妇女就动淫念的，他在心里已经犯了通奸罪。 "',
            'version': '当代译本'
        }
    },
    'one2one_C1_S4.json': {
        'q1_罗马书 5:8': {
            'text': '但是，当我们还是罪人的时候，基督就替我们死了。神的爱就在此向我们显明了。',
            'version': '标准译本'
        }
    },
    'one2one_C1_S6.json': {
        'q1_哥林多后书 5:21': {
            'text': '神使那位没有罪的替我们成为罪，好使我们在他里面成为神的义。',
            'version': '标准译本'
        },
        'q2_加拉太书 3:13': {
            'text': '基督替我们成了诅咒，从律法的诅咒中救赎了我们，因为经上记着："凡是被挂在木头上的，都是被诅咒的。"',
            'version': '标准译本'
        }
    },
    'one2one_C1_S7.json': {
        'create_new': {
            'q1_以弗所书 1:7': {
                'reference': '以弗所书 1:7',
                'text': '在他里面，我们藉着他的血，得蒙救赎、过犯得到赦免，都是出于神恩典的丰盛。',
                'version': '标准译本',
                'text_alt': '',
                'version_alt': '',
                'has_data': True
            },
            'q2_以弗所书 2:13': {
                'reference': '以弗所书 2:13',
                'text': '但你们这些从前远离神的人，现在靠着基督所流的血，已经重归神，可以亲近他了！',
                'version': '当代译本',
                'text_alt': '',
                'version_alt': '',
                'has_data': True
            }
        }
    },
    'one2one_C1_S8.json': {
        'q1_以弗所书 1:7': {
            'text': '在他里面，我们藉着他的血，得蒙救赎、过犯得到赦免，都是出于神恩典的丰盛。',
            'version': '标准译本'
        },
        'q2_以弗所书 2:13': {
            'text': '但你们这些从前远离神的人，现在靠着基督所流的血，已经重归神，可以亲近他了！',
            'version': '当代译本'
        }
    },
    'one2one_C1_S9.json': {
        'create_new': {}
    },
    'one2one_C1_S11.json': {
        'create_new': {
            'q1_以弗所书 2:8,9': {
                'reference': '以弗所书 2:8,9',
                'text': '8 你们得救是本乎恩，也因着信；这并不是出于自己，而是神所赐的； 9 也不是出于行为，免得有人自夸。',
                'version': '和修版',
                'text_alt': '',
                'version_alt': '',
                'has_data': True
            }
        }
    },
    'one2one_C1_S12.json': {
        'create_new': {}
    },
    'one2one_C1_S13.json': {
        'q1_哥林多后书 5:17': {
            'text': '若有人在基督里，他就是新造的人，旧事已过，都变成新的了。',
            'version': '和合本'
        }
    },
    'one2one_C1_S14.json': {
        'q1_使徒行传 2:36': {
            'text': '故此，以色列全家当确实知道，你们钉在十字架上的这位耶稣，神已经立他为主，为基督了。',
            'version': '和修版'
        }
    }
}

data_dir = 'data/answers'
updated_files = []
created_answers = []

print("=" * 60)
print("开始更新JSON文件...")
print("=" * 60)

for filename, update_data in verses_updates.items():
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
    if 'create_new' in update_data:
        # 完全替换answers
        data['answers'] = update_data['create_new']
        created_answers.append(section_num)
        print(f"✅ 第{section_num}节: 创建了新answers结构 ({len(update_data['create_new'])}个经文)")
    else:
        # 更新现有answers中的经文
        if 'answers' not in data:
            data['answers'] = {}
        
        updated_count = 0
        not_found = []
        for q_id, verse_info in update_data.items():
            if q_id in data['answers']:
                data['answers'][q_id]['text'] = verse_info['text']
                data['answers'][q_id]['version'] = verse_info['version']
                data['answers'][q_id]['has_data'] = True
                updated_count += 1
            else:
                not_found.append(q_id)
        
        if updated_count > 0:
            print(f"✅ 第{section_num}节: 更新了 {updated_count} 个经文")
        
        if not_found:
            print(f"⚠️  第{section_num}节: 未找到 {len(not_found)} 个key")
            print(f"   现有keys: {list(data['answers'].keys())}")
            print(f"   未找到: {not_found}")
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    updated_files.append(section_num)

print(f"\n{'='*60}")
print(f"✅ 完成！总共处理了 {len(updated_files)} 个文件")
if created_answers:
    print(f"   创建了新answers结构的节: {', '.join(created_answers)}")
print(f"{'='*60}")
