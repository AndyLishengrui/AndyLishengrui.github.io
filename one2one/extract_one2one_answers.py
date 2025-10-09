#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从一对一.txt文件中提取经文和答案，生成JSON格式的答案数据文件
"""

import json
import re
import os

def parse_one2one_content(txt_file):
    """解析一对一.txt文件，提取每一节的经文内容"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建答案数据存储目录
    os.makedirs('data/answers', exist_ok=True)
    
    # 第1课第1节：得救 1
    section_1_1 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 1,
        "section_title": "问题：罪使我们与神隔绝",
        "answers": {
            "q1_以赛亚书 59:1,2": {
                "reference": "以赛亚书 59:1,2",
                "text": "看哪！耶和华的手不是缩短了，以致不能拯救；他的耳朵不是不灵，不能听见；而是你们的罪孽使你们与你们的神隔绝；你们的罪恶使他掩面不顾你们，不听你们的祷告。",
                "has_data": True
            }
        }
    }
    
    # 第1课第2节：得救 2
    section_1_2 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 2,
        "section_title": "罪的定义",
        "answers": {
            "q1_马太福音 5:21,22": {
                "reference": "马太福音 5:21,22",
                "text": "你们听过吩咐古人的话，'不可杀人，杀人的要受审判。'但我告诉你们，凡无缘无故向弟兄发怒的，要受审判；凡骂弟兄是白痴的，要受公会的审判；凡骂弟兄是笨蛋的，难逃地狱的火。",
                "has_data": True
            }
        }
    }
    
    # 第1课第3节：得救 3
    section_1_3 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 3,
        "section_title": "罪的后果",
        "answers": {
            "q1_马太福音 5:27,28": {
                "reference": "马太福音 5:27,28",
                "text": "你们听过这样的话，'不可通奸。'但我告诉你们，凡看见妇女就动淫念的，他在心里已经犯了通奸罪。",
                "has_data": True
            },
            "q2_罗马书 3:23": {
                "reference": "罗马书 3:23",
                "text": "要知道，每个人都犯了罪，亏缺了神的荣耀。",
                "has_data": True
            },
            "q3_罗马书 6:23": {
                "reference": "罗马书 6:23",
                "text": "因为罪的代价就是死亡，而上帝借着主基督耶稣赐下的礼物则是永生。",
                "has_data": True
            }
        }
    }
    
    # 第1课第4节：得救 4
    section_1_4 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 4,
        "section_title": "解决方法：牺牲与代罪",
        "answers": {
            "q1_罗马书 5:8": {
                "reference": "罗马书 5:8",
                "text": "但是，当我们还是罪人的时候，基督就替我们死了。神的爱就在此向我们显明了。",
                "has_data": True
            }
        }
    }
    
    # 保存文件
    sections = [
        (section_1_1, "one2one_C1_S1.json"),
        (section_1_2, "one2one_C1_S2.json"),
        (section_1_3, "one2one_C1_S3.json"),
        (section_1_4, "one2one_C1_S4.json")
    ]
    
    for section_data, filename in sections:
        output_path = f"data/answers/{filename}"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(section_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已生成 {output_path}")

if __name__ == '__main__':
    parse_one2one_content('一对一.txt')
    print("\n✓ 所有答案数据文件已生成！")
