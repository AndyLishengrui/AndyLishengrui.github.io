#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从一对一.txt文件中提取经文和答案，生成JSON格式的答案数据文件
格式要求：
1. 经文章节在前，经文内容在后
2. 优先提供和合本答案
3. 如果原文不是和合本，则补充和合本作为主答案
"""

import json
import os

def create_answer_json_files():
    """创建答案JSON文件"""
    
    # 创建答案数据存储目录
    os.makedirs('data/answers', exist_ok=True)
    
    # 第1课第1节：得救 1 - 问题：罪使我们与神隔绝
    section_1_1 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 1,
        "section_title": "问题：罪使我们与神隔绝",
        "answers": {
            "q1_以赛亚书 59:1,2": {
                "reference": "以赛亚书 59:1,2",
                "text": "耶和华的膀臂并非缩短，不能拯救；耳朵并非发沉，不能听见。但你们的罪孽使你们与神隔绝，你们的罪恶使他掩面不听你们。",
                "version": "和合本",
                "text_alt": "看哪！耶和华的手不是缩短了，以致不能拯救；他的耳朵不是不灵，不能听见；而是你们的罪孽使你们与你们的神隔绝；你们的罪恶使他掩面不顾你们，不听你们的祷告。",
                "version_alt": "新译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第2节：得救 2 - 罪的定义
    section_1_2 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 2,
        "section_title": "罪的定义",
        "answers": {
            "q1_马太福音 5:21,22": {
                "reference": "马太福音 5:21,22",
                "text": "你们听见有吩咐古人的话，说：'不可杀人'，又说：'凡杀人的，难免受审判。'只是我告诉你们：凡向弟兄动怒的，难免受审判；凡骂弟兄是拉加的，难免公会的审断；凡骂弟兄是魔利的，难免地狱的火。",
                "version": "和合本",
                "text_alt": "你们听过吩咐古人的话，'不可杀人，杀人的要受审判。'但我告诉你们，凡无缘无故向弟兄发怒的，要受审判；凡骂弟兄是白痴的，要受公会的审判；凡骂弟兄是笨蛋的，难逃地狱的火。",
                "version_alt": "当代译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第3节：得救 3 - 罪的后果
    section_1_3 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 3,
        "section_title": "罪的后果",
        "answers": {
            "q1_马太福音 5:27,28": {
                "reference": "马太福音 5:27,28",
                "text": "你们听见有话说：'不可奸淫。'只是我告诉你们：凡看见妇女就动淫念的，这人心里已经与她犯奸淫了。",
                "version": "和合本",
                "text_alt": "你们听过这样的话，'不可通奸。'但我告诉你们，凡看见妇女就动淫念的，他在心里已经犯了通奸罪。",
                "version_alt": "当代译本",
                "has_data": True
            },
            "q2_罗马书 3:23": {
                "reference": "罗马书 3:23",
                "text": "因为世人都犯了罪，亏缺了神的荣耀；",
                "version": "和合本",
                "text_alt": "要知道，每个人都犯了罪，亏缺了神的荣耀。",
                "version_alt": "标准译本",
                "has_data": True
            },
            "q3_罗马书 6:23": {
                "reference": "罗马书 6:23",
                "text": "因为罪的工价乃是死；惟有神的恩赐，在我们的主基督耶稣里，乃是永生。",
                "version": "和合本",
                "text_alt": "因为罪的代价就是死亡，而上帝借着主基督耶稣赐下的礼物则是永生。",
                "version_alt": "当代译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第4节：得救 4 - 解决方法：牺牲与代罪
    section_1_4 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 4,
        "section_title": "解决方法：牺牲与代罪",
        "answers": {
            "q1_罗马书 5:8": {
                "reference": "罗马书 5:8",
                "text": "惟有基督在我们还作罪人的时候为我们死，神的爱就在此向我们显明了。",
                "version": "和合本",
                "text_alt": "但是，当我们还是罪人的时候，基督就替我们死了。神的爱就在此向我们显明了。",
                "version_alt": "标准译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第5节：得救 5
    section_1_5 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 5,
        "section_title": "基督的献祭",
        "answers": {
            "q1_希伯来书 9:26-28": {
                "reference": "希伯来书 9:26-28",
                "text": "如果这样，他从创世以来，就必多次受苦了；但如今在这末世显现一次，把自己献为祭，好除掉罪。按着定命，人人都有一死，死后且有审判；像这样，基督既然一次被献，担当了多人的罪，将来要向那等候他的人第二次显现，并与罪无关，乃是为拯救他们。",
                "version": "和合本",
                "text_alt": "不然的话，自创世以来他必定要一死而再死，不知受苦多少次了。但在这世代的末期，他只一次把自己献上，便除去了人的罪。按着定命，人人都有一死，而且死后还有审判；基督也是这样，曾经一次献上自己，承担了世人的罪；然而，他还要再来，那时不再是为赎罪而来，乃是为了使那些渴望他再来的人得到完全的救恩。",
                "version_alt": "当代译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第6节：得救 6
    section_1_6 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 6,
        "section_title": "代罪与替换",
        "answers": {
            "q1_哥林多后书 5:21": {
                "reference": "哥林多后书 5:21",
                "text": "神使那无罪的，替我们成为罪，好叫我们在他里面成为神的义。",
                "version": "和合本",
                "text_alt": "神使那位没有罪的替我们成为罪，好使我们在他里面成为神的义。",
                "version_alt": "标准译本",
                "has_data": True
            },
            "q2_加拉太书 3:13": {
                "reference": "加拉太书 3:13",
                "text": "基督既为我们受了咒诅，就赎出我们脱离律法的咒诅，因为经上记着：'凡挂在木头上都是被咒诅的。'",
                "version": "和合本",
                "text_alt": "基督替我们成了诅咒，从律法的诅咒中救赎了我们，因为经上记着：'凡是被挂在木头上的，都是被诅咒的。'",
                "version_alt": "标准译本",
                "has_data": True
            }
        }
    }
    
    # 第1课第7节：得救 7 - 结果：我们得救并与神和好
    section_1_7 = {
        "course_num": 1,
        "course_title": "新起点 得救",
        "section_num": 7,
        "section_title": "结果：我们得救并与神和好",
        "answers": {
            "q1_以弗所书 1:7": {
                "reference": "以弗所书 1:7",
                "text": "我们藉这爱子的血得蒙救赎，过犯得以赦免，乃是照他丰富的恩典。",
                "version": "和合本",
                "text_alt": "在他里面，我们藉着他的血，得蒙救赎、过犯得到赦免，都是出于神恩典的丰盛。",
                "version_alt": "标准译本",
                "has_data": True
            }
        }
    }
    
    # 保存文件
    sections = [
        (section_1_1, "one2one_C1_S1.json"),
        (section_1_2, "one2one_C1_S2.json"),
        (section_1_3, "one2one_C1_S3.json"),
        (section_1_4, "one2one_C1_S4.json"),
        (section_1_5, "one2one_C1_S5.json"),
        (section_1_6, "one2one_C1_S6.json"),
        (section_1_7, "one2one_C1_S7.json"),
    ]
    
    for section_data, filename in sections:
        output_path = f"data/answers/{filename}"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(section_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已生成 {output_path}")

if __name__ == '__main__':
    create_answer_json_files()
    print("\n✅ 所有答案数据文件已生成！")
    print("\n📋 格式说明：")
    print("  - 经文章节在前，经文内容在后")
    print("  - 优先提供和合本答案（text字段）")
    print("  - 其他译本作为备选（text_alt字段）")
    print("  - 支持多版本比对，取最高相似度")
