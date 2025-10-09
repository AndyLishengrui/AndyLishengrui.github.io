#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路加福音经文修正脚本
用于修正发现的经文错误，确保与中文和合本一致
"""

import json
import os
from datetime import datetime

def create_backup(filename):
    """创建备份文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = 'backup_original'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_filename = f"{backup_dir}/luke_backup_{timestamp}.json"
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已创建备份: {backup_filename}")
    return backup_filename

def load_luke_data():
    """加载路加福音数据"""
    with open('data/luke.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['verses']

def save_luke_data(verses_data):
    """保存路加福音数据"""
    # 重新加载完整数据结构
    with open('data/luke.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    # 更新verses部分
    full_data['verses'] = verses_data
    
    # 保存完整数据
    with open('data/luke.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

def find_verse(data, chapter, verse):
    """查找指定的经文"""
    for item in data:
        if item.get('chapter') == chapter and item.get('verse') == verse:
            return item
    return None

def update_verse(data, chapter, verse, new_zh_text):
    """更新经文的中文文本"""
    for item in data:
        if item.get('chapter') == chapter and item.get('verse') == verse:
            old_text = item.get('zh', '')
            item['zh'] = new_zh_text
            print(f"✏️  更新 路加福音 {chapter}:{verse}")
            print(f"   原文: {old_text[:50]}...")
            print(f"   新文: {new_zh_text[:50]}...")
            return True
    return False

def main():
    """主修正流程"""
    print("🔍 开始路加福音经文修正...")
    
    # 创建备份
    create_backup('data/luke.json')
    
    # 加载数据
    data = load_luke_data()
    
    # 修正项目列表 - 按照中文和合本标准
    corrections = [
        # 路加福音1:35 天使报喜
        {
            'chapter': 1,
            'verse': 35,
            'zh': '天使回答说："圣灵要临到你身上，至高者的能力要荫庇你，因此所要生的圣者必称为神的儿子。'
        },
        # 路加福音4:18 耶稣在会堂读经
        {
            'chapter': 4,
            'verse': 18,
            'zh': '主的灵在我身上，因为他用膏膏我，叫我传福音给贫穷的人；差遣我报告：被掳的得释放，瞎眼的得看见，叫那受压制的得自由，'
        },
        # 路加福音9:23 背十字架
        {
            'chapter': 9,
            'verse': 23,
            'zh': '耶稣又对众人说："若有人要跟从我，就当舍己，天天背起他的十字架来跟从我。'
        },
        # 路加福音19:10 人子来的目的
        {
            'chapter': 19,
            'verse': 10,
            'zh': '人子来，为要寻找、拯救失丧的人。"'
        },
        # 路加福音22:19 设立圣餐
        {
            'chapter': 22,
            'verse': 19,
            'zh': '又拿起饼来，祝谢了，就掰开，递给他们，说："这是我的身体，为你们舍的，你们也应当如此行，为的是记念我。"'
        },
        # 路加福音23:34 十字架上的祷告
        {
            'chapter': 23,
            'verse': 34,
            'zh': '当下耶稣说："父啊！赦免他们；因为他们所做的，他们不晓得。"兵丁就拈阄分他的衣服。'
        },
        # 路加福音11:2 主祷文修正
        {
            'chapter': 11,
            'verse': 2,
            'zh': '耶稣说："你们祷告的时候，要说：父啊，愿人都尊你的名为圣。愿你的国降临。"'
        },
    ]
    
    # 执行修正
    total_corrections = 0
    for correction in corrections:
        if update_verse(data, correction['chapter'], correction['verse'], correction['zh']):
            total_corrections += 1
    
    # 保存数据
    if total_corrections > 0:
        save_luke_data(data)
        print(f"✅ 已完成 {total_corrections} 项修正")
        print("💾 路加福音数据已更新")
    else:
        print("ℹ️  未发现需要修正的项目")

if __name__ == "__main__":
    main()