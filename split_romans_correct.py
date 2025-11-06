#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确按照罗马书圣经章节划分文件
根据文件中"5 外邦人的罪"、"6 犹太人的罪"、"7 全人类的罪"等标记
以及主题后的罗马书经文引用来确定章节边界
"""

import os
import re

def split_by_scripture_chapters():
    """按罗马书圣经章节正确划分"""
    
    input_file = 'BooksofRoman/romans_content.txt'
    output_dir = 'BooksofRoman/chapters_correct'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=" * 80)
    print("正确的罗马书章节划分")
    print("=" * 80)
    
    # 根据实际文件结构,手动确定章节边界
    # 这些边界是基于对文件的仔细分析得出的
    chapter_boundaries = {
        1: (1, 742),        # 开头到"5 外邦人的罪"之前
        2: (743, 994),      # "5 外邦人的罪"(行743)到"7 犹太人的罪"(行995)之前  
        3: (995, 1267),     # "7 犹太人的罪"(行995)开始,到第4章主题出现前
        4: (1268, 1388),    # 亚伯拉罕因信称义相关主题
        5: (1389, 1608),    # 称义的结果相关主题
        6: (1609, 1893),    # 向罪死了相关主题
        7: (1894, 2241),    # 基督徒与律法的关系
        8: (2242, 2935),    # 根本性的转折到神保守信徒
        9: (2936, 3039),    # 以色列的不信
        10: (3040, 3119),   # 以色列拒绝福音
        11: (3120, 3199),   # 以色列的将来
        12: (3200, 3239),   # 活祭与更新
        13: (3240, 3264),   # 顺服掌权者
        14: (3265, 3282),   # 不绊倒软弱的人
        15: (3283, 3289),   # 彼此接纳
        16: (3290, 3427)    # 问安与祝福
    }
    
    # 分割并保存各章节
    for chapter_num in range(1, 17):
        start, end = chapter_boundaries[chapter_num]
        
        # 提取章节内容
        chapter_lines = lines[start-1:end]
        
        # 保存到文件
        output_file = os.path.join(output_dir, f'chapter_{chapter_num:02d}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(chapter_lines)
        
        # 计算行数和主题数
        line_count = len(chapter_lines)
        topic_count = sum(1 for line in chapter_lines if re.match(r'^\d+\.\s+', line.strip()))
        
        print(f"第{chapter_num:2d}章: 行{start:4d}-{end:4d} ({line_count:4d}行, {topic_count:2d}个主题) → {output_file}")
    
    print("\n" + "=" * 80)
    print("✓ 章节分割完成!")
    print(f"✓ 输出目录: {output_dir}")
    print("=" * 80)
    
    # 验证统计
    print("\n各章节内容概览:")
    for chapter_num in range(1, 17):
        output_file = os.path.join(output_dir, f'chapter_{chapter_num:02d}.txt')
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 统计该章引用罗马书各章的次数
            refs = re.findall(r'罗马书\s*(\d+)[:：]', content)
            if refs:
                from collections import Counter
                ref_counts = Counter(refs)
                main_ref = ref_counts.most_common(1)[0]
                print(f"  第{chapter_num:2d}章: 最多引用罗马书第{main_ref[0]}章({main_ref[1]}次)")

if __name__ == '__main__':
    split_by_scripture_chapters()
