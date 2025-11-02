#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成第一课的合并JSON文件（带和合本标准答案）
"""

import json
import os

# 第一课所有经文的和合本答案（手动添加）
STANDARD_ANSWERS_HEHEBEN = {
    # Section 1
    "约翰福音 3:16": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。",
    
    # Section 2
    "以赛亚书 59:1,2": "耶和华的膀臂并非缩短，不能拯救，耳朵并非发沉，不能听见，但你们的罪孽使你们与神隔绝；你们的罪恶使他掩面不听你们。",
    "马太福音 5:21,22": "你们听见有吩咐古人的话，说：'不可杀人'；又说：'凡杀人的难免受审判。'只是我告诉你们，凡向弟兄动怒的，难免受审断；凡骂弟兄是拉加的，难免公会的审断；凡骂弟兄是魔利的，难免地狱的火。",
    "马太福音 5:27,28": "你们听见有话说：'不可奸淫。'只是我告诉你们，凡看见妇女就动淫念的，这人心里已经与她犯奸淫了。",
    "罗马书 3:23": "因为世人都犯了罪，亏缺了神的荣耀；",
    "罗马书 6:23": "因为罪的工价乃是死；惟有神的恩赐，在我们的主基督耶稣里，乃是永生。",
    
    # Section 3
    "罗马书 5:8": "惟有基督在我们还作罪人的时候为我们死，神的爱就在此向我们显明了。",
    "希伯来书 9:22": "按着律法，凡物差不多都是用血洁净的；若不流血，罪就不得赦免了。",
    "哥林多后书 5:21": "神使那无罪的，替我们成为罪，好叫我们在他里面成为神的义。",
    "加拉太书 3:13": "基督既为我们受了咒诅，就赎出我们脱离律法的咒诅；因为经上记着：'凡挂在木头上都是被咒诅的。'",
    
    # Section 4
    "以弗所书 2:1": "你们死在过犯罪恶之中，他叫你们活过来。",
    "以弗所书 2:4,5": "然而，神既有丰富的怜悯，因他爱我们的大爱，当我们死在过犯中的时候，便叫我们与基督一同活过来。你们得救是本乎恩。",
    
    # Section 5
    "罗马书 10:9": "你若口里认耶稣为主，心里信神叫他从死里复活，就必得救。",
    "以弗所书 2:8,9": "你们得救是本乎恩，也因着信；这并不是出于自己，乃是神所赐的；也不是出于行为，免得有人自夸。",
    
    # Section 6
    "哥林多后书 5:17": "若有人在基督里，他就是新造的人，旧事已过，都变成新的了。"
}

def load_course_structure():
    """加载课程结构"""
    with open('course_1_structure.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_answer_entry(reference, heheben_text, alt_text=None, alt_version=None):
    """创建答案条目"""
    entry = {
        "reference": reference,
        "text": heheben_text,  # 标准答案：和合本
        "version": "和合本",
        "has_data": True
    }
    
    # 如果有其他版本，添加为参考答案
    if alt_text and alt_version:
        entry["text_alt"] = alt_text
        entry["version_alt"] = alt_version
    
    return entry

def generate_merged_json():
    """生成合并的JSON文件"""
    course_data = load_course_structure()
    
    merged_data = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "sections": {}
    }
    
    for section in course_data['sections']:
        section_num = section['section_number']
        section_data = {
            "section_num": section_num,
            "section_title": section['title'],
            "answers": {}
        }
        
        question_num = 1
        
        # 处理verses字段（第2-5节）
        if 'verses' in section and section['verses']:
            for verse in section['verses']:
                ref = verse['reference']
                alt_text = verse['content']
                alt_version = verse['version']
                
                # 获取和合本标准答案
                heheben_text = STANDARD_ANSWERS_HEHEBEN.get(ref, alt_text)
                
                # 创建答案键
                answer_key = f"q{question_num}_{ref}"
                section_data["answers"][answer_key] = create_answer_entry(
                    ref, heheben_text, alt_text, alt_version
                )
                question_num += 1
        
        # 处理单个verse字段（第1节和第6节）
        if 'verse' in section and section['verse']:
            verse = section['verse']
            ref = verse['reference']
            original_text = verse['content']
            original_version = verse['version']
            
            # 获取和合本标准答案
            heheben_text = STANDARD_ANSWERS_HEHEBEN.get(ref, original_text)
            
            # 创建答案键
            answer_key = f"q{question_num}_{ref}"
            
            # 如果原文就是和合本，不需要alt
            if original_version == "和合本":
                section_data["answers"][answer_key] = create_answer_entry(
                    ref, heheben_text, None, None
                )
            else:
                section_data["answers"][answer_key] = create_answer_entry(
                    ref, heheben_text, original_text, original_version
                )
        
        # 添加到sections
        merged_data["sections"][str(section_num)] = section_data
    
    # 保存到文件
    output_dir = 'data/answers'
    os.makedirs(output_dir, exist_ok=True)
    output_file = f'{output_dir}/one2one_C1.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ 已生成: {output_file}')
    
    # 统计信息
    total_answers = sum(len(section["answers"]) for section in merged_data["sections"].values())
    print(f'📊 统计：共 {len(merged_data["sections"])} 个节，{total_answers} 个答案')
    
    # 显示每节的答案数量
    for section_num, section_data in merged_data["sections"].items():
        answer_count = len(section_data["answers"])
        print(f'   Section {section_num}: {answer_count} 个答案')

if __name__ == '__main__':
    generate_merged_json()
